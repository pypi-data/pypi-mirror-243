import numpy as np
import pandas as pd


def pagerank(A, init_vector=None, personalized_vector=None, source_axis=1, alpha=0.85, max_iter=1000, tol=1e-6):
    '''Computes the PageRank centrality of each node in a graph.

    Parameters
    ----------
    A : pandas.DataFrame
        Adjacency matrix of the graph. The shape of this matrix must be (N, N).

    init_vector : array-like, default=None
        Initial vector to use for the PageRank algorithm.
        The shape of this vector must be (N, 1). If not provided, the
        vector will be a vector of repeated values 1/N.

    personalized_vector : array-like, default=None
        Personalized vector to use for the PageRank algorithm.
        The shape of this vector must be (N, 1). If not provided, the
        vector will be a vector of repeated values 1/N.

    source_axis : int, default=1
        Axis representing the source nodes in the adjacency matrix.
        If 1, the source nodes are the columns of the adjacency matrix.
        If 0, the source nodes are the rows of the adjacency matrix.

    alpha : float, default=0.85
        Damping factor, between 0 and 1.

    max_iter : int, default=1000
        Maximum number of iterations to perform.

    tol : float, default=1e-6
        Tolerance to use for the convergence test.

    Returns
    -------
    x : array-like
        The pagerank of each node in the graph. The shape of this vector is (N, 1).

    Examples
    --------
    >>> A = pd.DataFrame([[0, 1, 0, 0, 0],
    ...                   [0, 0, 1, 1, 0],
    ...                   [0, 0, 0, 0, 0],
    ...                   [0, 0, 1, 0, 1],
    ...                   [1, 0, 0, 0, 0]],
    ...                  index=['A', 'B', 'C', 'D', 'E'],
    ...                  columns=['A', 'B', 'C', 'D', 'E'])
    >>> pagerank(A)
    array([[0.24194577],
           [0.24934796],
           [0.03      ],
           [0.24305423],
           [0.23565204]])
    '''
    assert isinstance(A, pd.DataFrame), "Adjacency matrix `A` must be a pandas.DataFrame"
    if source_axis == 1:
        pass
    elif source_axis == 0:
        A = A.T
    else:
        raise ValueError('`source_axis` must be 0 or 1')

    N = A.shape[0]
    out_degrees = A.sum(axis=0)  # axis=int(not bool(source_axis)) if transpose is not done before
    out_degrees = np.max([np.ones(out_degrees.shape), out_degrees], axis=0)

    # Normalize columns to sum up to 1
    A_norm = A.div(out_degrees, axis=1)  # axis=source_axis if transpose is not done before

    # Initial pagerank values
    if init_vector is None:
        x = np.repeat(1.0 / N, N).reshape(-1, 1)
    else:
        x = np.array(init_vector).reshape(-1, 1)
        x /= x.sum()

    # Initial personalize values
    if personalized_vector is None:
        p = np.repeat(1.0 / N, N).reshape(-1, 1)
    else:
        p = np.array(personalized_vector).reshape(-1, 1)
        p /= p.sum()

    # Perform iterations for PageRank
    for i in range(max_iter):
        prev_vector = x.copy()
        x = alpha * np.dot(A_norm, prev_vector) + (1 - alpha) * p

        err = np.abs(x - prev_vector).sum()
        if err < N * tol:
            return x
    raise ValueError('PageRank did not converge, try increasing `max_iter`or `tol`')


def multiplex_pagerank(adj_matrices, beta=1., gamma=1., alphas=0.85, init_vector=None, personalized_vector=None,
                       source_axis=1, max_iter=1000, tol=1e-6):
    '''Computes the Multiplex PageRank centrality of each node
    in multiple layers of graphs. Algorithm described in [1].

    [1] https://doi.org/10.1371/journal.pone.0078293

    Parameters
    ----------
    adj_matrices : list of pandas.DataFrame
        Adjacency matrices representing multiple graphs with
        the same nodes. The shape of each matrix must be (N, N).

    beta : float, default=1.
        Multiplicative exponent, greater or equal to 0.
        Scenarios:

        - beta = gamma = 0: Regular PageRank in the last layer.
        - beta = 1, gamma = 0: Multiplicative Multiplex PageRank.
        - beta = 0, gamma = 1: Additive Multiplex PageRank.
        - beta = gamma = 1: Combined Multiplex PageRank.

    gamma : float, default=1.
        Additive exponent, greater or equal to 0.
        Scenarios:

        - beta = gamma = 0: Regular PageRank in the last layer.
        - beta = 1, gamma = 0: Multiplicative Multiplex PageRank.
        - beta = 0, gamma = 1: Additive Multiplex PageRank.
        - beta = gamma = 1: Combined Multiplex PageRank.

    alphas : float or list, default=0.85
        Damping factor, between 0 and 1. If a single float is provided,
        this value will be used for all adjacency matrices.
        If a list of floats is provided, the ith value will be
        used for the ith adjacency matrix.

    init_vector : array-like, default=None
        Initial vector to use for the PageRank algorithm.
        The shape of this vector must be (N, 1). If not provided, the
        vector will be a vector of repeated values 1/N.

    personalized_vector : array-like, default=None
        Personalized vector to use for the PageRank algorithm.
        The shape of this vector must be (N, 1). If not provided, the
        vector will be a vector of repeated values 1/N.

    source_axis : int, default=1
        Axis representing the source nodes in the adjacency matrix.
        If 1, the source nodes are the columns of the adjacency matrix.
        If 0, the source nodes are the rows of the adjacency matrix.

    max_iter : int, default=1000
        Maximum number of iterations to perform.

    tol : float, default=1e-6
        Tolerance to use for the convergence test.

    Returns
    -------
    MPR : array-like
        The Multiplex PageRank of each node. It is the
        vector X obtained in the N-th layer (last adjacency matrix).
        The shape of this vector is (N, 1).
    '''
    assert all(
        [A.shape == adj_matrices[0].shape for A in adj_matrices[1:]]), "All adjacency matrices must have the same shape"
    assert all([isinstance(A, pd.DataFrame) for A in adj_matrices]), "All adjacency matrices must be a pandas.DataFrame"
    if not isinstance(alphas, list):
        alphas = [alphas] * len(adj_matrices)

    Xs = []
    for i, A in enumerate(adj_matrices):
        # First layer
        if i == 0:
            x = pagerank(A=A,
                         init_vector=init_vector,
                         personalized_vector=personalized_vector,
                         source_axis=source_axis,
                         alpha=alphas[0],
                         max_iter=max_iter,
                         tol=tol
                         )
            Xs.append(x)
        # Following layers
        else:
            if source_axis == 1:
                pass
            elif source_axis == 0:
                A = A.T
            else:
                raise ValueError('`source_axis` must be 0 or 1')

            N = A.shape[0]
            G = []
            for j in range(A.shape[1]):
                Aj = A.values[:, j]
                Gj = np.dot(Aj, Xs[-1] ** beta)
                if Gj == 0:
                    Gj += 1
                G.append(Gj)
            G = np.array(G).reshape(-1)

            # Normalize columns to sum up to 1
            A_norm = A.div(G, axis=1)  # axis=source_axis if transpose is not done before

            # Initial pagerank values
            if init_vector is None:
                X = np.repeat(1.0 / N, N).reshape(-1, 1)
            else:
                X = np.array(init_vector).reshape(-1, 1)
                X /= X.sum()

            converged = False
            for j in range(max_iter):
                prev_vector = X.copy()
                X = alphas[i] * (Xs[-1] ** beta) * np.dot(A_norm, prev_vector) + (1 - alphas[i]) * (Xs[-1] ** gamma) / (
                            N * np.mean((Xs[-1] ** gamma)))

                err = np.abs(X - prev_vector).sum()
                if err < N * tol:
                    converged = True
                    break
            if converged:
                Xs.append(X)
            else:
                raise ValueError('PageRank did not converge, try increasing `max_iter`or `tol`')
    # Result from the last layer, after iterating through all of them
    MPR = Xs[-1]
    return MPR