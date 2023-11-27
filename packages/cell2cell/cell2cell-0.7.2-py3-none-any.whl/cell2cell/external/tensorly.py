import numpy as np
import tensorly as tl
import warnings
from tensorly.random import random_cp  # v0.7.0
from tensorly.base import unfold # v0.7.0
#from tensorly.decomposition._cp import initialize_cp # v0.8.0
from tensorly.tenalg.proximal import soft_thresholding # v0.7.0
from tensorly.cp_tensor import (
    CPTensor,
    unfolding_dot_khatri_rao,
    cp_norm,
    cp_normalize,
    validate_cp_rank,
)


def make_svd_non_negative(tensor, U, S, V, nntype):
    """ Use NNDSVD method to transform SVD results into a non-negative form. This
    method leads to more efficient solving with NNMF [1].

    Parameters
    ----------
    tensor : tensor being decomposed
    U, S, V: SVD factorization results
    nntype : {'nndsvd', 'nndsvda'}
        Whether to fill small values with 0.0 (nndsvd), or the tensor mean (nndsvda, default).

    [1]: Boutsidis & Gallopoulos. Pattern Recognition, 41(4): 1350-1362, 2008.
    """

    # NNDSVD initialization
    W = tl.zeros_like(U)
    H = tl.zeros_like(V)

    # The leading singular triplet is non-negative
    # so it can be used as is for initialization.
    W = tl.index_update(W, tl.index[:, 0], tl.sqrt(S[0]) * tl.abs(U[:, 0]))
    H = tl.index_update(H, tl.index[0, :], tl.sqrt(S[0]) * tl.abs(V[0, :]))

    for j in range(1, tl.shape(U)[1]):
        x, y = U[:, j], V[j, :]

        # extract positive and negative parts of column vectors
        x_p, y_p = tl.clip(x, a_min=0.0), tl.clip(y, a_min=0.0)
        x_n, y_n = tl.abs(tl.clip(x, a_max=0.0)), tl.abs(tl.clip(y, a_max=0.0))

        # and their norms
        x_p_nrm, y_p_nrm = tl.norm(x_p), tl.norm(y_p)
        x_n_nrm, y_n_nrm = tl.norm(x_n), tl.norm(y_n)

        m_p, m_n = x_p_nrm * y_p_nrm, x_n_nrm * y_n_nrm

        # choose update
        if m_p > m_n:
            u = x_p / x_p_nrm
            v = y_p / y_p_nrm
            sigma = m_p
        else:
            u = x_n / x_n_nrm
            v = y_n / y_n_nrm
            sigma = m_n

        lbd = tl.sqrt(S[j] * sigma)
        W = tl.index_update(W, tl.index[:, j], lbd * u)
        H = tl.index_update(H, tl.index[j, :], lbd * v)

    # After this point we no longer need H
    eps = tl.eps(tensor.dtype)

    if nntype == "nndsvd":
        W = soft_thresholding(W, eps)
    elif nntype == "nndsvda":
        avg = tl.mean(tensor)
        W = tl.where(W < eps, tl.ones(tl.shape(W), **tl.context(W)) * avg, W)
    else:
        raise ValueError(
            'Invalid nntype parameter: got %r instead of one of %r' %
            (nntype, ('nndsvd', 'nndsvda')))

    return W


def initialize_nn_cp(tensor, rank, init='svd', svd='numpy_svd', random_state=None,
                     normalize_factors=False, nntype='nndsvda'):
    r"""Initialize factors used in `parafac`.

    The type of initialization is set using `init`. If `init == 'random'` then
    initialize factor matrices using `random_state`. If `init == 'svd'` then
    initialize the `m`th factor matrix using the `rank` left singular vectors
    of the `m`th unfolding of the input tensor.

    Parameters
    ----------
    tensor : ndarray
    rank : int
    init : {'svd', 'random'}, optional
    svd : str, default is 'numpy_svd'
        function to use to compute the SVD, acceptable values in tensorly.SVD_FUNS
    nntype : {'nndsvd', 'nndsvda'}
        Whether to fill small values with 0.0 (nndsvd), or the tensor mean (nndsvda, default).

    Returns
    -------
    factors : CPTensor
        An initial cp tensor.

    """
    rng = tl.check_random_state(random_state)

    if init == 'random':
        kt = random_cp(tl.shape(tensor), rank, normalise_factors=False, random_state=rng, **tl.context(tensor))

    elif init == 'svd':
        try:
            svd_fun = tl.SVD_FUNS[svd]
        except KeyError:
            message = 'Got svd={}. However, for the current backend ({}), the possible choices are {}'.format(
                svd, tl.get_backend(), tl.SVD_FUNS)
            raise ValueError(message)

        factors = []
        for mode in range(tl.ndim(tensor)):
            U, S, V = svd_fun(unfold(tensor, mode), n_eigenvecs=rank)

            # Apply nnsvd to make non-negative
            U = make_svd_non_negative(tensor, U, S, V, nntype)

            if tensor.shape[mode] < rank:
                # TODO: this is a hack but it seems to do the job for now
                random_part = tl.tensor(rng.random_sample((U.shape[0], rank - tl.shape(tensor)[mode])),
                                        **tl.context(tensor))
                U = tl.concatenate([U, random_part], axis=1)

            factors.append(U[:, :rank])

        kt = CPTensor((None, factors))

    # If the initialisation is a precomputed decomposition, we double check its validity and return it
    elif isinstance(init, (tuple, list, CPTensor)):
        # TODO: Test this
        try:
            kt = CPTensor(init)
        except ValueError:
            raise ValueError(
                'If initialization method is a mapping, then it must '
                'be possible to convert it to a CPTensor instance'
            )
        return kt
    else:
        raise ValueError('Initialization method "{}" not recognized'.format(init))

    # Make decomposition feasible by taking the absolute value of all factor matrices
    kt.factors = [tl.abs(f) for f in kt[1]]

    if normalize_factors:
        kt = cp_normalize(kt)

    return kt


def non_negative_parafac(tensor, rank, n_iter_max=100, init='svd', svd='numpy_svd',
                         tol=10e-7, random_state=None, verbose=0, normalize_factors=False,
                         return_errors=False, mask=None, cvg_criterion='abs_rec_error', loss_function='standard',
                         fixed_modes=None):
    """
    Non-negative CP decomposition

    Uses multiplicative updates, see [2]_

    Parameters
    ----------
    tensor : ndarray
    rank   : int
            number of components
    n_iter_max : int
                 maximum number of iteration
    init : {'svd', 'random'}, optional
    svd : str, default is 'numpy_svd'
        function to use to compute the SVD, acceptable values in tensorly.SVD_FUNS
    tol : float, optional
          tolerance: the algorithm stops when the variation in
          the reconstruction error is less than the tolerance
    random_state : {None, int, np.random.RandomState}
    verbose : int, optional
        level of verbosity
    fixed_modes : list, default is None
        A list of modes for which the initial value is not modified.
        The last mode cannot be fixed due to error computation.
    loss_function : str, default is 'rayleigh'
        Loss function to use during the optimization.
        Options are {'rayleigh', 'standard', 'boolean-odds', 'poisson'}

    Returns
    -------
    factors : ndarray list
            list of positive factors of the CP decomposition
            element `i` is of shape ``(tensor.shape[i], rank)``

    References
    ----------
    .. [2] Amnon Shashua and Tamir Hazan,
       "Non-negative tensor factorization with applications to statistics and computer vision",
       In Proceedings of the International Conference on Machine Learning (ICML),
       pp 792-799, ICML, 2005
    """
    epsilon = tl.eps(tensor.dtype)
    rank = validate_cp_rank(tl.shape(tensor), rank=rank)

    if mask is not None and init == "svd":
        message = "Masking occurs after initialization. Therefore, random initialization is recommended."
        warnings.warn(message, Warning)

    weights, factors = initialize_nn_cp(tensor, rank, init=init, svd=svd,
                                        random_state=random_state,
                                        normalize_factors=normalize_factors)
    rec_errors = []
    norm_tensor = tl.norm(tensor, 2)

    if fixed_modes is None:
        fixed_modes = []

    if tl.ndim(tensor) - 1 in fixed_modes:
        warnings.warn(
            'You asked for fixing the last mode, which is not supported while tol is fixed.\n The last mode will not be fixed. Consider using tl.moveaxis()')
        fixed_modes.remove(tl.ndim(tensor) - 1)
    modes_list = [mode for mode in range(tl.ndim(tensor)) if mode not in fixed_modes]

    for iteration in range(n_iter_max):
        if verbose > 1:
            print("Starting iteration", iteration + 1)
        for mode in modes_list:
            if verbose > 1:
                print("Mode", mode, "of", tl.ndim(tensor))

            accum = 1
            # khatri_rao(factors).tl.dot(khatri_rao(factors))
            # simplifies to multiplications
            sub_indices = [i for i in range(len(factors)) if i != mode]
            for i, e in enumerate(sub_indices):
                if i:
                    accum *= tl.dot(tl.transpose(factors[e]), factors[e])
                else:
                    accum = tl.dot(tl.transpose(factors[e]), factors[e])

            if mask is not None:
                tensor = tensor * mask + tl.cp_to_tensor((None, factors), mask=1 - mask)

            mttkrp = unfolding_dot_khatri_rao(tensor, (None, factors), mode)

            numerator = tl.clip(mttkrp, a_min=epsilon, a_max=None)
            denominator = tl.dot(factors[mode], accum)
            denominator = tl.clip(denominator, a_min=epsilon, a_max=None)
            factor = factors[mode] * numerator / denominator

            factors[mode] = factor

        if normalize_factors:
            weights, factors = cp_normalize((weights, factors))

        log_pseudo = 1e-3
        if tol:
            if loss_function == 'standard':
                # ||tensor - rec||^2 = ||tensor||^2 + ||rec||^2 - 2*<tensor, rec>
                factors_norm = cp_norm((weights, factors))

                # mttkrp and factor for the last mode. This is equivalent to the
                # inner product <tensor, factorization>
                iprod = tl.sum(tl.sum(mttkrp * factor, axis=0))
                rec_error = (
                        tl.sqrt(tl.abs(norm_tensor ** 2 + factors_norm ** 2 - 2 * iprod))
                        / norm_tensor
                )
            elif loss_function == 'rayleigh':
                if mask is None:
                    mask = tl.ones(tensor.shape)
                tensor = tensor * mask
                rec = tl.cp_to_tensor((weights, factors)) * mask
                rec_error = (
                    tl.sum(2 * tl.log2(rec + log_pseudo) / tl.log2(tl.tensor([np.e])) + (tensor ** 2) / (2 * ((rec + log_pseudo) ** 2)))
                )
            elif loss_function == 'boolean-odds':
                if mask is None:
                    mask = tl.ones(tensor.shape)
                tensor = tensor * mask
                rec = tl.cp_to_tensor((weights, factors)) * mask
                rec_error = (
                    tl.sum(tl.log2(rec + 1) / tl.log2(tl.tensor([np.e])) - tensor * (tl.log2(rec + log_pseudo) / tl.log2(tl.tensor([np.e]))))
                )
            elif loss_function == 'poisson':
                if mask is None:
                    mask = tl.ones(tensor.shape)
                tensor = tensor * mask
                rec = tl.cp_to_tensor((weights, factors)) * mask
                rec_error = (
                    tl.sum(rec - tensor * (tl.log2(rec + log_pseudo) / tl.log2(tl.tensor([np.e]))))
                )
            elif loss_function == 'random':
                rec_error = (tl.sum([1 + 10**-np.random.randint(10)]))
            else:
                raise ValueError('Enter a valid `loss_function`')
            rec_errors.append(rec_error)
            if iteration >= 1:
                rec_error_decrease = rec_errors[-2] - rec_errors[-1]

                if verbose:
                    print("iteration {}, reconstraction error: {}, decrease = {}".format(iteration, rec_error,
                                                                                         rec_error_decrease))

                if cvg_criterion == 'abs_rec_error':
                    stop_flag = abs(rec_error_decrease) < tol
                elif cvg_criterion == 'rec_error':
                    stop_flag = rec_error_decrease < tol
                else:
                    raise TypeError("Unknown convergence criterion")

                if stop_flag:
                    if verbose:
                        print("PARAFAC converged after {} iterations".format(iteration))
                    break
            else:
                if verbose:
                    print('reconstruction error={}'.format(rec_errors[-1]))

    cp_tensor = CPTensor((weights, factors))

    if return_errors:
        return cp_tensor, rec_errors
    else:
        return cp_tensor