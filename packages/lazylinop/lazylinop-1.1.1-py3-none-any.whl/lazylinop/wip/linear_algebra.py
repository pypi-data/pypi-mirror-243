"""
Module for linear algebra related LazyLinearOps (work in progress).
"""
import numpy as np
import scipy as sp
from lazylinop import *
import warnings
warnings.simplefilter(action='always')


try:
    import dask
    from dask.distributed import Client, LocalCluster, wait
except ImportError:
    print("Dask ImportError")


def alternant(x, f: list, use_numba: bool=False):
    """Constructs alternant matrix as a lazy linear operator A.
    The shape of the alternant lazy linear operator is (x.shape[0], len(f)).
    A.toarray() = |f[0](x[0]) f[1](x[0]) ... f[n](x[0])|
                  |f[0](x[1]) f[1](x[1]) ... f[n](x[1])|
                  |f[0](x[2]) f[1](x[2]) ... f[n](x[2])|
                  |    .          .              .     |
                  |    .          .              .     |
                  |    .          .              .     |
                  |    .          .              .     |
                  |f[0](x[m]) f[1](x[m]) ... f[n](x[m])|

    Args:
        x: 1d array
            Array of points
        f: list
            A list of lambda functions.
        use_numba: bool, optional
            If True, use prange from Numba (default is False)
            to compute batch in parallel.
            It is useful only and only if the batch size and
            the length of a are big enough.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            f expects at least one element.
        ValueError
            x expects 1d-array.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop.wip.linear_algebra import alternant
        >>> M = 5
        >>> N = 6
        >>> x = np.random.rand(M)
        >>> f = [lambda x, n=n: np.power(x, n) for n in range(N)]
        >>> X = np.random.rand(N, 3)
        >>> np.allclose(alternant(x, f) @ X, np.vander(x, N=N, increasing=True) @ X)
        True

    References:
        See also `Alternant matrix <https://en.wikipedia.org/wiki/Alternant_matrix>`_.
    """
    if len(f) < 1:
        raise ValueError("f expects at least one element.")

    if x.ndim != 1:
        raise ValueError("x expects 1d-array.")

    M, N = x.shape[0], len(f)

    def _matmat(x, f, X, adjoint):

        def _1d(x, f, X, adjoint):
            if X.ndim != 1:
                raise Exception("batch size must be equal to 1.")            
            y = np.empty(
                N if adjoint else M,
                dtype=np.complex_ if x.dtype.kind == 'c' or X.dtype.kind == 'c' else (x[0] * X[0]).dtype
            )
            if adjoint:
                # conjugate and transpose
                for i in range(N):
                    y[i] = np.array([f[i](x[j]) for j in range(M)]) @ X
            else:
                for i in range(M):
                    y[i] = np.array([f[j](x[i]) for j in range(N)]) @ X
            return y

        import numba as nb
        from numba import prange, set_num_threads, threading_layer
        nb.config.DISABLE_JIT = int(not use_numba)
        nb.config.THREADING_LAYER = 'omp'
        if not use_numba:
            nb.config.DISABLE_JIT = 1
        @nb.jit(nopython=True, parallel=True, cache=True)
        def _2d(x, f, X, adjoint):
            if X.ndim != 2:
                raise Exception("batch size must be greater than 1.")
            batch_size = X.shape[1]
            y = np.empty(
                (N if adjoint else M, batch_size),
                dtype=np.complex_ if x.dtype.kind == 'c' or X.dtype.kind == 'c' else (x[0] * X[0, 0]).dtype
            )
            if adjoint:
                # conjugate and transpose
                for b in prange(batch_size):
                    for i in range(N):
                        y[i, b] = np.array([f[i](x[j]) for j in range(M)]) @ X[:, b]
            else:
                for b in prange(batch_size):
                    for i in range(M):
                        y[i, b] = np.array([f[j](x[i]) for j in range(N)]) @ X[:, b]
            return y

        return _1d(x, f, X, adjoint) if X.ndim == 1 else _2d(x, f, X, adjoint)

    return LazyLinearOp(
        shape=(M, N),
        matmat=lambda X: _matmat(x, f, X, False),
        rmatmat=lambda X: _matmat(x, f, X, True)
    )


def companion(a):
    """Constructs a companion matrix as a lazy linear operator C.

    Args:
        a: np.ndarray
        1d array of polynomial coefficients (N, ).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            # of coefficients must be at least >= 2.
        ValueError
            The first coefficient a[0] must be != 0.0.

    References:
        See also `scipy.linalg.companion <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.companion.html>`_.
        See also `Companion matrix <https://en.wikipedia.org/wiki/Companion_matrix>`_.
    """
    if a.shape[0] < 2:
        raise ValueError("# of coefficients must be at least >= 2.")
    if a[0] == 0.0:
        raise ValueError("The first coefficient a[0] must be != 0.")

    def _matmat(a, x, H):
        if x.ndim == 1:
            x = x.reshape(x.shape[0], 1)
            batch_size = 1
            is_1d = True
        else:
            batch_size = x.shape[1]
            is_1d = False
        N = a.shape[0]
        if 'complex' in a.dtype.str:
            y = np.empty((N - 1, batch_size), dtype=np.complex_)
        else:
            y = np.empty((N - 1, batch_size), dtype=(a[0] * x[0]).dtype)
        if H:
            # conjugate and transpose
            for b in range(batch_size):
                y[:, b] = np.divide(np.multiply(a[1: ], x[0, b]), -a[0])
                np.add(y[:(N - 2), b], x[1:(N - 1), b], out=y[:(N - 2), b])
        else:
            for b in range(batch_size):
                y[0, b] = np.divide(a[1:], -a[0]) @ x[:, b]
                y[1:(N - 1), b] = x[:(N - 2), b]
        return y.ravel() if is_1d else y

    return LazyLinearOp(
        shape=(a.shape[0] - 1, a.shape[0] - 1),
        matmat=lambda x: _matmat(a, x, False),
        rmatmat=lambda x: _matmat(a, x, True)
    )


def fiedler(a: np.ndarray, use_numba: bool=False):
    """Constructs a symmetric Fiedler matrix as a lazy linear operator F.
    A symmetric Fiedler matrix has entry F[i, j] = np.absolute(a[i] - a[j]).

    Args:
        a: np.ndarray
            Sequence of numbers (shape is (n, )).
        use_numba: bool, optional
            If True, use prange from Numba (default is False)
            to compute batch in parallel.
            It is useful only and only if the batch size and
            the length of a are big enough.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            a is empty.

    References:
        See also `scipy.linalg.fiedler <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.fiedler.html>`_.
        See also `Pascal matrix <https://en.wikipedia.org/wiki/Pascal_matrix>`_.
    """
    if a.shape[0] == 0:
        raise ValueError("a is empty.")

    import numba as nb
    from numba import prange, set_num_threads, threading_layer
    nb.config.DISABLE_JIT = int(not use_numba)
    nb.config.THREADING_LAYER = 'omp'
    if not use_numba:
        nb.config.DISABLE_JIT = 1
    @nb.jit(nopython=True, parallel=True, cache=True)
    def _matmat(a, x):
        if x.ndim == 1:
            x = x.reshape(x.shape[0], 1)
            batch_size = 1
            is_1d = True
        else:
            batch_size = x.shape[1]
            is_1d = False
        n = a.shape[0]
        y = np.zeros((n, batch_size), dtype=(a[0] * x[0, 0]).dtype)
        # run in parallel thanks to Numba prange
        for b in prange(batch_size):
            for i in range(n):
                # (L + D + U) @ x where U = L^T
                # L is a lower triangular matrix such that L[i, i] = 0
                # and D is a diagonal matrix such that D[i, i] = 0.
                # L @ x + (x^T @ L)^T
                if i < (n - 1):
                    y[i, b] += np.absolute(np.subtract(a[i], a[(i + 1):])) @ x[(i + 1):, b]
                if i > 0:
                    y[i, b] += np.absolute(np.subtract(a[i], a[:i])) @ x[:i, b]
        return y.ravel() if is_1d else y

    return LazyLinearOp(
        shape=(a.shape[0], a.shape[0]),
        matmat=lambda x: _matmat(a, x),
        rmatmat=lambda x: _matmat(a, x)
    )


def helmert(n: int, full: bool=False, use_numba: bool=False):
    """Constructs a Helmert matrix n x n as a lazy linear operator H.
    |1/sqrt(n)      1/sqrt(n)      1/sqrt(n)      ... 1/sqrt(n)           |
    |1/sqrt(2)      -1/sqrt(2)     0              ... 0                   |
    |1/sqrt(6)      1/sqrt(6)      2/sqrt(6)      ... 0                   |
    |1/sqrt(n(n-1)) 1/sqrt(n(n-1)) 1/sqrt(n(n-1)) ... -(n-1)/sqrt(n(n-1)) |
    
    Args:
        n: int
            The size of the matrix (n, n).
        full: bool, optional
            If False (default) do not return the first row H[1:, :] @ x.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            n must be >= 2.

    Examples:
        >>> from lazylinop.wip.linear_algebra import helmert
        >>> import numpy as np
        >>> import scipy as sp
        >>> N = 100
        >>> X = np.random.rand(N, 10)
        >>> H = helmert(N)
        >>> np.allclose(H @ X, sp.linalg.helmert(N) @ X)
        True

    References:
        See also `scipy.linalg.helmert <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.helmert.html>`_.
        See also `R-project Helmert matrix <https://search.r-project.org/CRAN/refmans/fastmatrix/html/helmert.html>`_.
    """
    if n < 2:
        raise ValueError("n must be >= 2.")

    import numba as nb
    from numba import prange, set_num_threads, threading_layer
    nb.config.DISABLE_JIT = 0 if use_numba else 1
    nb.config.THREADING_LAYER = 'omp'

    def _matmat(n, full, x, H):
        def _1d(n, full, x, H):
            if x.ndim != 1:
                raise Exception("batch size must be equal to 1.")
            offset = 0 if full else 1
            invsqrtn = 1.0 / np.sqrt(n)
            if H:
                # transpose and conjugate
                y = np.zeros(n, dtype=x.dtype)
                # if full skip the first row
                if full:
                    y[:] = np.multiply(np.full(n, invsqrtn), x[0])
                for i in range(1, n):
                    invsqrt = 1.0 / np.sqrt((i + 1) * i)
                    y[:i] += np.multiply(np.full(i, invsqrt), x[i - offset])
                    y[i] -= x[i - offset] * (i * invsqrt)
            else:
                y = np.empty((n - offset), dtype=x.dtype)
                # if full skip the first row
                if full:
                    y[0] = np.full(n, invsqrtn) @ x
                for i in range(1, n):
                    invsqrt = 1.0 / np.sqrt((i + 1) * i)
                    # y[i - offset] = np.full(i, invsqrt) @ x[:i] - x[i] * (i * invsqrt)
                    y[i - offset] = np.sum(invsqrt * x[:i], axis=0) - x[i] * (i * invsqrt)
            return y

        def _2d(n, full, x, H):
            if x.ndim != 2:
                raise Exception("batch size must be greater than 1.")
            batch_size = x.shape[1]
            offset = 0 if full else 1
            invsqrtn = 1.0 / np.sqrt(n)

            def _no_bf(n, full, x, H):
                if H:
                    # transpose and conjugate
                    y = np.zeros((n, batch_size), dtype=x.dtype)
                    # if full skip the first row
                    if full:
                        y[:, :] = np.multiply(invsqrtn, x[0, :])
                    for i in range(1, n):
                        invsqrt = 1.0 / np.sqrt((i + 1) * i)
                        y[:i, :] += np.multiply(invsqrt, x[i - offset, :])
                        y[i, :] -= x[i - offset, :] * (i * invsqrt)
                else:
                    y = np.empty((n - offset, batch_size), dtype=x.dtype)
                    # if full skip the first row
                    if full:
                        y[0, :] = np.full(n, invsqrtn) @ x
                    for i in range(1, n):
                        invsqrt = 1.0 / np.sqrt(i ** 2 + i)
                        # y[i - offset, :] = np.full(i, invsqrt) @ x[:i, :] - x[i, :] * (i * invsqrt)
                        y[i - offset, :] = invsqrt * np.sum(x[:i, :], axis=0) - x[i, :] * (i * invsqrt)
                return y

            @nb.jit(nopython=True, parallel=True, cache=True)
            def _bf(n, full, x, H):
                if H:
                    # transpose and conjugate
                    y = np.zeros((n, batch_size), dtype=x.dtype)
                    for b in prange(batch_size):
                        # if full skip the first row
                        if full:
                            for i in range(n):
                                y[i, b] = invsqrtn * x[0, b]
                        for i in range(1, n):
                            invsqrt = 1.0 / np.sqrt((i + 1) * i)
                            for j in range(i):
                                y[j, b] += invsqrt * x[i - offset, b]
                            # y[:i, b] += np.multiply(np.full(i, invsqrt), x[i - offset, b])
                            y[i, b] -= x[i - offset, b] * (i * invsqrt)
                else:
                    y = np.empty((n - offset, batch_size), dtype=x.dtype)
                    for b in prange(batch_size):
                        # if full skip the first row
                        if full:
                            y[0, b] = 0.0
                            for i in range(n):
                                y[0, b] += invsqrtn * x[i, b]
                        for i in range(1, n):
                            invsqrt = 1.0 / np.sqrt(i ** 2 + i)
                            y[i - offset, b] = -x[i, b] * (i * invsqrt)
                            for j in range(i):
                                y[i - offset, b] += invsqrt * x[j, b]
                return y

            return _bf(n, full, x, H) if use_numba else _no_bf(n, full, x, H)

        return _1d(n, full, x, H) if x.ndim == 1 else _2d(n, full, x, H)

    return LazyLinearOp(
        shape=(n - 1 + int(full), n),
        matmat=lambda x: _matmat(n, full, x, False),
        rmatmat=lambda x: _matmat(n, full, x, True)
    )


def hilbert(n: int, use_numba: bool=False, bf: bool=False):
    """Constructs Hilbert matrix n x n as a lazy linear operator H (H[i, j] = 1 / (i + j + 1)).
    Of note Hilbert matrix is positive definite and symmetric H = L + D + L^T where L is a lower
    triangular matrix such that L[i, i] = 0.
    
    Args:
        n: int
            The size of the matrix (n, n).
        use_numba: bool, optional
            If True, use Numba (default is False).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            n must be >= 2.

    References:
        See also `scipy.linalg.hilbert <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.hilbert.html>`_.
        See also `Hilbert matrix <https://en.wikipedia.org/wiki/Hilbert_matrix>`_.
    """
    if n < 2:
        raise ValueError("n must be >= 2.")

    def _matmat(n, x):
        import numba as nb
        from numba import prange, set_num_threads, threading_layer
        nb.config.DISABLE_JIT = 0 if use_numba else 1
        nb.config.THREADING_LAYER = 'omp'

        @nb.jit(nopython=True, parallel=False, cache=True)
        def _1d(n, x):
            if x.ndim != 1:
                raise Exception("batch size must be equal to 1.")
            y = np.empty(n, dtype=x.dtype)
            for i in range(n):
                # (L + D + U) @ x where U = L^T
                # L is a lower triangular matrix such that L[i, i] = 0.
                # L @ x + D @ x + (x^T @ L)^T
                y[i] = np.divide(1.0, i + np.arange(n) + 1) @ x
            return y

        @nb.jit(nopython=True, parallel=False, cache=True)
        def _bf1d(n, x):
            if x.ndim != 1:
                raise Exception("batch size must be equal to 1.")
            y = np.zeros(n, dtype=x.dtype)
            for i in range(n):
                # (L + D + U) @ x where U = L^T
                # L is a lower triangular matrix such that L[i, i] = 0.
                # L @ x + D @ x + (x^T @ L)^T
                for j in range(x.shape[0]):
                    y[i] += x[j] / (i + j + 1)
            return y

        @nb.jit(nopython=True, parallel=True, cache=True)
        def _2d(n, x):
            if x.ndim != 2:
                raise Exception("batch size must be greater than 1.")
            batch_size = x.shape[1]
            y = np.empty((n, batch_size), dtype=x.dtype)
            for b in prange(batch_size):
                for i in range(n):
                    # (L + D + U) @ x where U = L^T
                    # L is a lower triangular matrix such that L[i, i] = 0.
                    # L @ x + D @ x + (x^T @ L)^T
                    y[i, b] = np.divide(1.0, i + np.arange(n) + 1) @ x[:, b]
            return y

        @nb.jit(nopython=True, parallel=True, cache=True)
        def _bf2d(n, x):
            if x.ndim != 2:
                raise Exception("batch size must be greater than 1.")
            batch_size = x.shape[1]
            y = np.zeros((n, batch_size), dtype=x.dtype)
            for b in prange(batch_size):
                for i in range(n):
                    # (L + D + U) @ x where U = L^T
                    # L is a lower triangular matrix such that L[i, i] = 0.
                    y[i, b] += x[i, b] / (i + i + 1)
                    for j in range(i + 1, x.shape[0]):
                        norm = 1 / (i + j + 1)
                        y[i, b] += x[j, b] * norm
                        y[j, b] += x[i, b] * norm
            return y

        if bf:
            return _bf1d(n, x) if x.ndim == 1 else _bf2d(n, x)
        else:
            return _1d(n, x) if x.ndim == 1 else _2d(n, x)

    return LazyLinearOp(
        shape=(n, n),
        matmat=lambda x: _matmat(n, x),
        rmatmat=lambda x: _matmat(n, x)
    )


def khatri_rao(A, B, column: bool=True, method: str='lazylinop'):
    """Constructs a Khatri-Rao product lazy linear operator K.
    Khatri-Rao product is a column-wize Kronecker product we denotes c*
    while the row-wize product is r*.
    If A and B are two matrices then (A c* B)^T = A^T r* B^T.
    Therefore, we easily get the adjoint of the row-wize Kronecker product.

    Args:
        A: first matrix
        B: second matrix
        column: bool, optional
        Compute Khatri-Rao product column-wize (True is default)
        If False, compute row-wize product
        method: str, optional
        If 'scipy' uses SciPy Khatri-Rao product

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            number of rows differs.
        ValueError
            number of columns differs.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop.wip.linear_algebra import khatri_rao
        >>> M1 = np.full((2, 2), 1)
        >>> M2 = np.eye(3, M=2, k=0)
        >>> x = np.random.rand(2)
        >>> K = khatri_rao(M1, M2)
        >>> S = sp.linalg.khatri_rao(M1, M2)
        >>> np.allclose(K @ x, S @ x)
        True

    References:
        See also `scipy.linalg.khatri_rao <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.khatri_rao.html>`_.
    """

    Ma, Na = A.shape[0], A.shape[1]
    Mb, Nb = B.shape[0], B.shape[1]

    if not column and Ma != Mb:
        raise ValueError("number of rows differs.")

    if column and Na != Nb:
        raise ValueError("number of columns differs.")

    if column:
        shape = (Ma * Mb, Na)
    else:
        shape = (Ma, Na * Nb)

    from lazylinop import diag

    # @dask.delayed
    def _1d(A, B, op, column):
        Ma, Na = A.shape[0], A.shape[1]
        Mb, Nb = B.shape[0], B.shape[1]
        if column:
            # we use (A c* B) @ x = vec(B @ diag(x) @ A^T)
            # and a ravel with order='F' (does not work with Numba)
            # return (B @ np.diag(op) @ A.T).ravel(order='F')
            return (eye(B.shape[0], n=B.shape[0], k=0) @ B @ diag(op) @ A.T).ravel(order='F')
        else:
            # for each row compute product of Kronecker product with a vector
            # reshape() supports contiguous array only (Numba message)
            # copy to get contiguous
            Y = np.full(Ma, 0.0 * (A[0, 0] + B[0, 0] + op[0]))
            for r in range(Ma):
                Y[r] = A[r, :] @ (B[r, :] @ op.reshape(A.shape[1], B.shape[1]).T).T
            return Y

    def _2d(A, B, op, column):
        Ma, Na = A.shape[0], A.shape[1]
        Mb, Nb = B.shape[0], B.shape[1]
        batch_size = op.shape[1]
        Y = np.full((Ma * Mb if column else Ma, batch_size), 0.0 * (A[0, 0] + B[0, 0] + op[0, 0]))
        if False:
            mm = []
            for i in range(batch_size):
                mm.append(dask.delayed(_1d)(A, B, op[:, i], column))
            results = dask.compute(mm)
            for i in range(batch_size):
                Y[:, i] = results[0][i]
        else:
            for i in range(batch_size):
                Y[:, i] = _1d(A, B, op[:, i], column)
        return Y

    if method == 'scipy':
        if isLazyLinearOp(A):
            A = eye(A.shape[0], n=A.shape[0], k=0) @ A
        if isLazyLinearOp(B):
            B = eye(B.shape[0], n=B.shape[0], k=0) @ B
        return LazyLinearOp(
            shape=shape,
            matmat=lambda x: sp.linalg.khatri_rao(A, B) @ x,
            rmatmat=lambda x : (
                _1d(A.T.conj(), B.T.conj(), x, not column) if x.ndim == 1
                else _2d(A.T.conj(), B.T.conj(), x, not column)
            )
        )
    else:
        # we use (A c* B)^T = A^T r* B^T to compute the adjoint.
        if True:
            return LazyLinearOp(
                shape=shape,
                matmat=lambda x: (
                    _1d(A, B, x, column) if x.ndim == 1
                    else _2d(A, B, x, column)
                ),
                rmatmat=lambda x : (
                    _1d(A.T.conj(), B.T.conj(), x, not column) if x.ndim == 1
                    else _2d(A.T.conj(), B.T.conj(), x, not column)
                )
            )
        else:
            return LazyLinearOp(
                shape=shape,
                matmat=lambda x: _1d(A, B, x, column),
                rmatmat=lambda x : _1d(A.T.conj(), B.T.conj(), x, not column)
            )


def lehmer(n: int, use_numba: bool=False, bf: bool=False):
    """Constructs Lehmer matrix n x n as a lazy linear operator L (L[i, j] = min(i, j) / max(i, j)).
    Of note Lehmer matrix is symmetric.
    
    Args:
        n: int
            The size of the matrix (n, n).
        use_numba: bool, optional
            If True, use Numba (default is False).
        bf: bool, optional
            If True, use brute force nested loops (default is False)

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            n must be >= 2.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.linear_algebra import lehmer
        >>> N = 2
        >>> x = np.random.rand(N)
        >>> np.allclose(lehmer(N) @ X, np.array([[1, 1 / 2], [1 / 2, 1]]) @ X)
        True

    References:
        See also `Lehmer matrix <https://en.wikipedia.org/wiki/Lehmer_matrix>`_.
    """
    if n < 2:
        raise ValueError("n must be >= 2.")

    def _matmat(n, x):
        import numba as nb
        from numba import prange, set_num_threads, threading_layer
        nb.config.DISABLE_JIT = 0 if use_numba else 1
        nb.config.THREADING_LAYER = 'omp'

        # (L + D + U) @ x where U = L^T and D = Id
        # L is a lower triangular matrix such that L[i, i] = 0.
        # L @ x + x + (x^T @ L)^T

        @nb.jit(nopython=True, parallel=False, cache=True)
        def _1d(n, x):
            if x.ndim != 1:
                raise Exception("batch size must be equal to 1.")
            y = np.copy(x)
            for i in range(n):
                # seq = np.divide(min(i, i:n), max(i, i:n))
                seq = np.divide(i + 1, np.arange(i + 1, n + 1, 1))
                seq[0] = 0.0
                if i == 0:
                    y[i] += seq @ x[i:]
                else:
                    # y[i] += np.add(seq @ x[i:], x[:i] @ np.divide(min(i, 0:i) / max(i, 0:i))))
                    y[i] += np.add(seq @ x[i:], np.divide(np.arange(1, i + 1), i + 1) @ x[:i])
            return y

        @nb.jit(nopython=True, parallel=False, cache=True)
        def _bf1d(n, x):
            if x.ndim != 1:
                raise Exception("batch size must be equal to 1.")
            y = np.zeros(n, dtype=x.dtype)
            for i in range(n):
                for j in range(x.shape[0]):
                    y[i] += x[j] * min(i, j) / max(i, j)
            return y

        @nb.jit(nopython=True, parallel=True, cache=True)
        def _2d(n, x):
            if x.ndim != 2:
                raise Exception("batch size must be greater than 1.")
            batch_size = x.shape[1]
            y = np.empty((n, batch_size), dtype=x.dtype)
            for b in prange(batch_size):
                seq = np.divide(1, np.arange(1, n + 1))
                y[0, b] = seq @ x[:, b]
                for i in range(1, n - 1):
                    seq = np.divide(
                        np.append(np.arange(1, i + 1), np.full(n - i, i + 1)),
                        np.append(np.full(i, i + 1), np.arange(i + 1, n + 1))
                    )
                    y[i, b] = seq @ x[:, b]
                seq = np.divide(np.arange(1, n + 1), n)
                y[n - 1, b] = seq @ x[:, b]
            return y

        @nb.jit(nopython=True, parallel=True, cache=True)
        def _bf2d(n, x):
            if x.ndim != 2:
                raise Exception("batch size must be greater than 1.")
            batch_size = x.shape[1]
            y = np.zeros((n, batch_size), dtype=x.dtype)
            for b in prange(batch_size):
                for i in range(n):
                    y[i, b] += x[i, b]
                    for j in range(i + 1, x.shape[0]):
                        norm = min(i, j) / max(i, j)
                        y[i, b] += x[j, b] * norm
                        y[j, b] += x[i, b] * norm
            return y

        if bf:
            return _bf1d(n, x) if x.ndim == 1 else _bf2d(n, x)
        else:
            return _1d(n, x) if x.ndim == 1 else _2d(n, x)

    return LazyLinearOp(
        shape=(n, n),
        matmat=lambda x: _matmat(n, x),
        rmatmat=lambda x: _matmat(n, x)
    )


def leslie(f: np.ndarray, s: np.ndarray, use_numba: bool=False):
    """Constructs a Leslie matrix as a lazy linear operator L.

    Args:
        f: np.ndarray
            The fecundity coefficients (N, ).
        s: np.ndarray
            The survival coefficients (N, ).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            # of fecundity coefficients must be N and # of survival coefficients must be N - 1.

    References:
        See also `scipy.linalg.leslie <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.leslie.html>`_.
        See also `Leslie matrix <https://en.wikipedia.org/wiki/Leslie_matrix>`_.
    """
    if (f.shape[0] - 1) != s.shape[0]:
        raise ValueError("# of fecundity coefficients must be N and # of survival coefficients must be N - 1.")

    def _matmat(f, s, x, H):
        def _1d(f, s, x, H):
            if x.ndim != 1:
                raise Exception("batch size must be equal to 1.")
            N = f.shape[0]
            y = np.empty(N, dtype=((f[0] + s[0]) * x[0]).dtype)
            if H:
                # conjugate and transpose
                y[:] = np.multiply(f, x[0])
                np.add(y[:(N - 1)], np.multiply(s, x[1:N]), out=y[:(N - 1)])
            else:
                y[0] = f @ x
                y[1:N] = np.multiply(s, x[:(N - 1)])
            return y

        import numba as nb
        from numba import prange, set_num_threads, threading_layer
        nb.config.DISABLE_JIT = 0 if use_numba else 1
        nb.config.THREADING_LAYER = 'omp'
        @nb.jit(nopython=True, parallel=True, cache=True)
        def _2d(f, s, x, H):
            if x.ndim == 1:
                raise Exception("batch size must be > 1.")
            N = f.shape[0]
            batch_size = x.shape[1]
            y = np.empty((N, batch_size), dtype=((f[0] + s[0]) * x[0]).dtype)
            if H:
                # conjugate and transpose
                for b in prange(batch_size):
                    y[:, b] = np.multiply(f, x[0, b])
                    # np.add(y[:(N - 1), b], np.multiply(s, x[1:N, b]), out=y[:(N - 1), b])
                    y[:(N - 1), b] += np.multiply(s, x[1:, b])
            else:
                for b in prange(batch_size):
                    y[0, b] = f @ x[:, b]
                    y[1:, b] = np.multiply(s, x[:(N - 1), b])
            return y

        return _1d(f, s, x, H) if x.ndim == 1 else _2d(f, s, x, H)

    return LazyLinearOp(
        shape=(f.shape[0], f.shape[0]),
        matmat=lambda x: _matmat(f, s, x, False),
        rmatmat=lambda x: _matmat(f, s, x, True)
    )


def pascal(n: int, kind: str='symmetric', exact: bool=True):
    """Constructs Pascal matrix as a lazy linear operator P.
    It uses the formula S = exp(A) @ exp(B) where B = A^T is
    a matrix with entries only on the first subdiagonal.
    The entries are the sequence arange(1, n) (NumPy notation).
    Of note, A and B are nilpotent matrices A^n = B^n = 0.
    To compute S @ X we use the Taylor expansion
    S @ X = sum(A^k / k!, k=0 to n) @ sum(B^k / k!, k=0 to n) @ X.
    Because of A and B are nilpotent matrices, we just have
    to compute the first n terms of the expansion.

    Args:
        n: int
            The size of the Pascal matrix (n, n).
        kind: str, optional
            If 'lower' constructs lower Pascal matrix L.
            If 'upper' constructs upper Pascal matrix U.
            If 'symmetric' (default) constructs L @ U.
        exact: bool, optional
            If exact is False the matrix coefficients are not
            the exact ones. If exact is True (default) the matrix
            coefficients will be integers.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            kind is either 'symmetric', 'lower' or 'upper'.

    Examples:
        >>> from lazylinop.wip.linear_algebra import pascal
        >>> import numpy as np
        >>> import scipy as sp
        >>> N = 100
        >>> X = np.random.rand(N, 10)
        >>> P = pascal(N, kind='symmetric', exact=True)
        >>> np.allclose(P @ X, sp.linalg.pascal(N, kind='symmetric', exact=True) @ X)
        True

    References:
        See also `scipy.linalg.pascal <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.pascal.html>`_.
        See also `Pascal matrix <https://en.wikipedia.org/wiki/Pascal_matrix>`_.
    """
    if not kind in ['symmetric', 'lower', 'upper']:
        raise ValueError("kind is either 'symmetric', 'lower' or 'upper'.")

    def _matmat(n, x, kind):
        if x.ndim == 1:
            x = x.reshape(x.shape[0], 1)
            batch_size = 1
            is_1d = True
        else:
            batch_size = x.shape[1]
            is_1d = False
        # for large n entries of the Pascal matrix
        # become very big ! TODO something about it
        if n <= 160:
            y = np.empty((n, batch_size), dtype=x.dtype)
            Mx = np.empty(n, dtype=x.dtype)
        else:
            y = np.empty((n, batch_size), dtype=object)
            Mx = np.empty(n, dtype=object)
        if False and exact:
            # TODO
            pass
        else:
            scale = 1.0
            # L = exp(A)
            # U = exp(B)
            # S = L @ U
            # Of note, A and B=A^T matrices are nilpotents.
            # upper matrix U
            if kind == 'symmetric' or kind == 'upper':
                # it is better to use the seq trick for big value of n
                # instead of diag lazy linear operator ?
                # Du = diag(np.arange(1, n), k=1)
                seq = np.arange(1, n)
                for b in range(batch_size):
                    factor = 1.0
                    y[:, b] = x[:, b]
                    # np.copyto(Mx, Du @ x[:, b])
                    np.copyto(Mx, np.append(np.multiply(seq, x[1:, b]), [0.0]))
                    for i in range(1, n, 1):
                        factor /= i
                        np.add(y[:, b], np.multiply(factor, Mx), out=y[:, b])
                        # if b == 0:
                        #     print(i, y[0, b], factor, "*", Mx[0], "=", factor * Mx[0])
                        # np.copyto(Mx, Du @ Mx)
                        np.copyto(Mx, np.append(np.multiply(seq, Mx[1:]), [0.0]))
            # lower matrix L
            if kind == 'symmetric' or kind == 'lower':
                # it is better to use the seq trick for big value of n
                # instead of diag lazy linear operator ?
                # Dl = diag(np.arange(1, n), k=-1)
                seq = np.arange(1, n)
                for b in range(batch_size):
                    factor = 1.0
                    # if 'symmetric' is asked for, do not initialize
                    if kind == 'lower':
                        y[:, b] = x[:, b]
                        # np.copyto(Mx, Dl @ x[:, b])
                        np.copyto(Mx, np.append([0.0], np.multiply(seq, x[:(n - 1), b])))
                    else:
                        # np.copyto(Mx, Dl @ y[:, b])
                        np.copyto(Mx, np.append([0.0], np.multiply(seq, y[:(n - 1), b])))
                    for i in range(1, n, 1):
                        factor /= i
                        np.add(y[:, b], np.multiply(factor, Mx), out=y[:, b])
                        # np.copyto(Mx, Dl @ Mx)
                        np.copyto(Mx, np.append([0.0], np.multiply(seq, Mx[:(n - 1)])))
        return y.ravel() if is_1d else y

    if kind == 'lower':
        kindT = 'upper'
    elif kind == 'upper':
        kindT = 'lower'
    else:
        kindT = kind
        
    return LazyLinearOp(
        shape=(n, n),
        matmat=lambda x: _matmat(n, x, kind),
        rmatmat=lambda x: _matmat(n, x, kindT)
    )


def redheffer(n: int, use_numba: bool=False, bf: bool=False):
    """Constructs Redheffer matrix n x n as a lazy linear operator R.
    Redheffer matrix entry R[i, j] is 1 if i divides j, 0 otherwize.
    Redheffer matrix for n=5 looks like:
    |1 1 1 1 1|
    |1 1 0 1 0|
    |1 0 1 0 0|
    |1 0 0 1 0|
    |1 0 0 0 1|
    and its transpose looks like:
    |1 1 1 1 1|
    |1 1 0 0 0|
    |1 0 1 0 0|
    |1 1 0 1 0|
    |1 0 0 0 1|
    
    Args:
        n: int
            The size of the matrix (n, n).
        use_numba: bool, optional
            If True, use Numba (default is False).
        bf: bool, optional
            If True, use brute force nested loops (default is False).
            If True, brute force uses Numba.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            n must be >= 2.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.linear_algebra import redheffer
        >>> N = 3
        >>> x = np.random.rand(N)
        >>> np.allclose(redheffer(N) @ x, np.array([[1, 1, 1], [1, 1, 0], [1, 0, 1]]) @ x)
        True

    References:
        See also `Redheffer matrix <https://en.wikipedia.org/wiki/Redheffer_matrix>`_.
    """
    if n < 2:
        raise ValueError("n must be >= 2.")

    def _matmat(n, x, adjoint):
        import numba as nb
        from numba import prange, set_num_threads, threading_layer
        nb.config.DISABLE_JIT = 0 if use_numba or bf else 1
        nb.config.THREADING_LAYER = 'omp'

        # diagonal of Redheffer matrix is 1
        # first column as-well-as first row is 1

        @nb.jit(nopython=True, parallel=False, cache=True)
        def _1d(n, x):
            if x.ndim != 1:
                raise Exception("batch size must be equal to 1.")
            y = np.empty(n, dtype=x.dtype)
            y[0] = np.sum(x)
            if adjoint:
                y[1:] = x[0]
                for i in range(1, n):
                    y[np.arange(i, n, i + 1)] += x[i]
            else:
                for i in range(1, n):
                    y[i] = x[0] + np.sum(x[np.arange(i, n, i + 1)])
            return y

        @nb.jit(nopython=True, parallel=False, cache=True)
        def _bf1d(n, x):
            if x.ndim != 1:
                raise Exception("batch size must be equal to 1.")
            y = np.empty(n, dtype=x.dtype)
            if adjoint:
                for i in range(n):
                    y[i] = x[0]
                    y[0] += x[i]
                y[0] -= x[0]
                for i in range(1, n):
                    for j in range(i, n, i + 1):
                        y[j] += x[i]
            else:
                for i in range(n):
                    y[i] = x[0]
                    for j in range(i, n, i + 1):
                        y[i] += x[j]
                y[0] -= x[0]
            return y

        @nb.jit(nopython=True, parallel=True, cache=True)
        def _2d(n, x):
            if x.ndim != 2:
                raise Exception("batch size must be greater than 1.")
            batch_size = x.shape[1]
            y = np.zeros((n, batch_size), dtype=x.dtype)
            if adjoint:
                for b in prange(batch_size):
                    y[0, b] += np.sum(x[:, b])
                    y[1:, b] += x[0, b]
                    for i in range(1, n):
                        y[np.arange(i, n, i + 1), b] += x[i, b]
            else:
                for b in prange(batch_size):
                    y[0, b] += np.sum(x[:, b])
                    for i in range(1, n):
                        y[i, b] += x[0, b] + np.sum(x[np.arange(i, n, i + 1), b])
            return y

        @nb.jit(nopython=True, parallel=True, cache=True)
        def _bf2d(n, x):
            if x.ndim != 2:
                raise Exception("batch size must be greater than 1.")
            batch_size = x.shape[1]
            y = np.empty((n, batch_size), dtype=x.dtype)
            if adjoint:
                for b in prange(batch_size):
                    y[0, b] = x[0, b]
                    for i in range(1, n):
                        y[0, b] += x[i, b]
                        y[i, b] = x[0, b]
                    for i in range(1, n):
                        for j in range(i, n, i + 1):
                            y[j, b] += x[i, b]
            else:
                for b in prange(batch_size):
                    for i in range(n):
                        y[i, b] = x[0, b]
                        for j in range(i, n, i + 1):
                            y[i, b] += x[j, b]
                    y[0, b] -= x[0, b]
            return y

        if bf:
            return _bf1d(n, x) if x.ndim == 1 else _bf2d(n, x)
        else:
            return _1d(n, x) if x.ndim == 1 else _2d(n, x)

    return LazyLinearOp(
        shape=(n, n),
        matmat=lambda x: _matmat(n, x, False),
        rmatmat=lambda x: _matmat(n, x, True)
    )


def H(shape: tuple, F_to_C: bool = False):
    """Constructs a lazy linear operator Op such that Op @ x
    is F order flattened from C order flattened x array.
    C and F order definition comes from Numpy flatten function.
    If F order to C order is True swap shape[0] and shape[1].

    Args:
        shape: tuple, shape of the image
        C_to_F: bool, optional
        if True F order to C order, if False (default) C order to F order.
        if C order to F order swap shape[0] and shape[1].

    Returns:
        LazyLinearOperator

    Raises:
        Exception
            shape expects a tuple (X, Y).

    Examples:
        >>> from lazylinop.wip.linear_algebra import H
        >>> import numpy as np
        >>> img = np.reshape(np.arange(16), newshape=(4, 4))
        >>> Op = H(img.shape)
        >>> np.allclose(Op @ img.flatten(order='C'), img.flatten(order='F'))
        True
        >>> img = np.reshape(np.arange(12), newshape=(3, 4))
        >>> Op = H(img.shape)
        >>> np.allclose(Op @ img.flatten(order='C'), img.flatten(order='F'))
        True
        >>> img = np.reshape(np.arange(12), newshape=(4, 3))
        >>> Op = H(img.shape)
        >>> np.allclose(Op @ img.flatten(order='C'), img.flatten(order='F'))
        True
    """
    if shape[0] is None or shape[1] is None:
        raise Exception("shape expects a tuple (X, Y).")
    if F_to_C:
        newshape = (shape[1], shape[0])
    else:
        newshape = (shape[0], shape[1])
    def _matvec(x, shape):
        X, Y = shape[0], shape[1]
        mv = np.empty(X * Y, dtype=x.dtype)
        # get column c=0
        # P[r, r * Y] = 1 where r = 0 to X - 1
        # get column c=1
        # P[c * X + r, c + r * Y] = 1 where r = 0 to X - 1
        # ...
        for c in range(Y):
            mv[c * X + np.arange(X)] = x[np.arange(X) * Y + c].conj()
        return mv
    def _rmatvec(x, shape):
        Y, X = shape[0], shape[1]
        mv = np.empty(X * Y, dtype=x.dtype)
        for c in range(Y):
            mv[c * X + np.arange(X)] = x[np.arange(X) * Y + c].conj()
        return mv
    return LazyLinearOp(
        shape=(shape[0] * shape[1], shape[0] * shape[1]),
        matvec=lambda x: _matvec(x, newshape),
        rmatvec=lambda x: _rmatvec(x, newshape)
    )


def h_multiply(a):
    """Constructs a Hessenberg decomposition as a lazy linear operator H.
    It can be used to compute the product between Hessenberg matrix and a vector x.
    Hessenberg decomposition writes a = Q @ H @ Q^H.

    Args:
        a: np.ndarray or LazyLinearOp
        Compute Hessenberg decomposition of the matrix a of shape (M, N).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            Argument a expects a 2d array.
        ValueError
            # of rows and # of columns are differents.

    References:
        See also `scipy.linalg.hessenberg <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.hessenberg.html>`_.
        See also `Hessenberg decomposition <https://en.wikipedia.org/wiki/Hessenberg_matrix>`_.
    """
    if a.ndim != 2:
        raise ValueError("Argument a expects 2d array.")
    if a.shape[0] != a.shape[1]:
        return ValueError("# of rows and # of columns are differents.")

    def _matmat(a, x, adjoint):

        if isLazyLinearOp(x):
            # TODO: do better than that
            H = sp.linalg.hessenberg(np.eye(x.shape[0], M=x.shape[0], k=0) @ a)[what[mode]]
        else:
            H = sp.linalg.hessenberg(a, calc_q=False)

        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
            batch_size = 1
        else:
            is_1d = False
            batch_size = x.shape[1]

        y = np.empty((a.shape[0], batch_size), dtype=(a[0, 0] * x[0]).dtype)

        # Hessenberg matrix first sub-diagonal has non-zero entries
        if adjoint:
            for b in range(batch_size):
                y[0, b] = H[:2, 0] @ x[:2, b]
                if a.shape[0] >= 2:
                    y[1, b] = H[:3, 1] @ x[:3, b]
                if a.shape[0] > 2:
                    for i in range(2, a.shape[0]):
                        y[i, b] = H[:min(a.shape[0], i + 2), i] @ x[:min(a.shape[0], i + 2), b]
        else:
            for b in range(batch_size):
                y[0, b] = H[0, :] @ x[:, b]
                if a.shape[0] >= 2:
                    y[1, b] = H[1, :] @ x[:, b]
                if a.shape[0] > 2:
                    for i in range(2, a.shape[0]):
                        y[i, b] = H[i, (i - 1):] @ x[(i - 1):, b]
        return y.ravel() if is_1d else y

    return LazyLinearOp(
        shape=(a.shape[0], a.shape[0]),
        matmat=lambda x: _matmat(a, x, False),
        # rmatmat=lambda x: _matmat(a.T.conj(), x, False)
        rmatmat=lambda x: _matmat(a, x, True)
    )


def qr_multiply(a, mode: str='r'):
    """Constructs a QR decomposition as a lazy linear operator Op.
    Q is unitary/orthogonal matrix while R is upper triangular matrix.
    Op(a, mode='r') @ X is the result of the multiplication of X by R.
    Op(a, mode='q') @ X is the result of the multiplication of X by Q.
    The QR decomposition of matrix a writes a = Q @ R.
    
    Args:
        a: np.ndarray or LazyLinearOp
        Compute QR decomposition of the matrix a (shape is (M, N)).
        Shape of Q is (M, M) and shape of R is (M, N).
        mode: str, optional
        If 'r' (resp. 'q') returns R (resp. Q).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            Invalid shape.
        ValueError
            qr expects a 2d array.
        ValueError
            mode expects either 'q' or 'r'.

    References:
        See also `scipy.linalg.qr <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.qr.html>`_.
        See also `QR decomposition <https://en.wikipedia.org/wiki/QR_decomposition>`_.
    """
    if len(a.shape) != 2:
        raise ValueError("qr expects 2d array.")
    if mode != 'q' and mode != 'r':
        raise ValueError("mode expects either 'q' or 'r'.")

    def _matmat(a, x, H):

        if x.ndim == 1:
            x = x.reshape(x.shape[0], 1)
            batch_size = 1
            is_1d = True
        else:
            is_1d = False
            batch_size = x.shape[1]

        if isLazyLinearOp(a):
            # TODO: do better than that
            if mode == 'q':
                Q, _ = sp.linalg.qr(np.eye(a.shape[0], M=a.shape[0], k=0) @ a, mode='full')
            elif mode == 'r':
                R = sp.linalg.qr(np.eye(a.shape[0], M=a.shape[0], k=0) @ a, mode=mode)[0]
            else:
                raise ValueError("mode expects either 'q' or 'r'.")
        else:
            if mode == 'q':
                Q, _ = sp.linalg.qr(a, mode='full')
            elif mode == 'r':
                R = sp.linalg.qr(a, mode=mode)[0]
            else:
                raise ValueError("mode expects either 'q' or 'r'.")

        # TODO: parallel for-loop
        if H:
            # conjugate transpose
            if mode == 'q':
                y = np.empty((a.shape[0], batch_size), dtype=(a[0, 0] * x[0, 0]).dtype)
                np.copyto(Q, Q.T.conj())
                for b in range(batch_size):
                    y[:, b] = Q @ x[:, b]
            else:
                y = np.empty((a.shape[1], batch_size), dtype=(a[0, 0] * x[0, 0]).dtype)
                for b in range(batch_size):
                    for i in range(R.shape[1]):
                        y[i, b] = R[:(i + 1), i].conj() @ x[:(i + 1), b]
        else:
            y = np.empty((a.shape[0], batch_size), dtype=(a[0, 0] * x[0, 0]).dtype)
            if mode == 'q':
                for b in range(batch_size):
                    y[:, b] = Q @ x[:, b]
            else:
                for b in range(batch_size):
                    for i in range(R.shape[0]):
                        y[i, b] = R[i, i:] @ x[i:, b]

        return y.ravel() if is_1d else y

    shape = (a.shape[0], a.shape[0 if mode == 'q' else 1])

    return LazyLinearOp(
        shape=shape,
        matmat=lambda x: _matmat(a, x, False),
        rmatmat=lambda x: _matmat(a, x, True)
    )


def sylvester(cp, cq):
    """Constructs Sylvester matrix as a lazy linear operator S_p,q.
    If p has a degree m=2 and q has a degree n=3 Sylvester matrix looks like:
    |p_2 p_1 p_0  0   0 |
    | 0  p_2 p_1 p_0  0 |
    | 0   0  p_2 p_1 p_0|
    |q_3 q_2 q_1 q_0  0 |
    | 0  q_3 q_2 q_1 q_0|

    Args:
        cp: list
            List of coefficients (m + 1) of the first polynomial p.
        cq: list
            List of coefficients (n + 1) of the second polynomial q.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            List of coefficients should have at least one element.

    Examples:
        >>> import numpy as np
        >>> from lazylinop.wip.linear_algebra import sylvester
        >>> Op = sylvester(np.random.rand(3), np.random.rand(2))
        >>> check_op(Op)
        True

    References:
        See `Sylvester matrix <https://en.wikipedia.org/wiki/Sylvester_matrix>`_.
    """
    M = cp.shape[0]
    N = cq.shape[0]
    # Keep only the first dimension of the list of coefficients
    if cp.ndim > 1:
        cp = np.copy(cp[:1])
    if cq.ndim > 1:
        cq = np.copy(cq[:1])
    Md = M - 1
    Nd = N - 1
    if M == 0 or N == 0:
        raise ValueError("List of coefficients should have at least one element.")

    def _matmat(cp, cq, x):
        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
        else:
            is_1d = False
        batch_size = x.shape[1]
        y = np.empty((Md + Nd, batch_size), dtype=x.dtype)
        for b in range(batch_size):
            for n in range(Nd):
                y[n, b] = cp[::-1] @ x[n:(n + Md + 1), b]
            for m in range(Md):
                y[Nd + m, b] = cq[::-1] @ x[m:(m + Nd + 1), b]
        return y.ravel() if is_1d else y

    def _rmatmat(cp, cq, x):
        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
        else:
            is_1d = False
        batch_size = x.shape[1]
        y = np.zeros((Md + Nd, batch_size), dtype=x.dtype)
        for b in range(batch_size):
            for n in range(Nd):
                y[n:(n + Md + 1), b] += np.multiply(cp[::-1], x[n, b])
            for m in range(Md):
                y[m:(m + Nd + 1), b] += np.multiply(cq[::-1], x[Nd + m, b])
        return y.ravel() if is_1d else y

    return LazyLinearOp(
        shape=(Md + Nd, Md + Nd),
        matmat=lambda x: _matmat(cp, cq, x),
        rmatmat=lambda x: _rmatmat(cp, cq, x)
    )

def eigvals(a):
    """Constructs a diagonal matrix from the eigen values of
    matrix a as a lazy linear operator E.

    Args:
        a: np.ndarray or LazyLinearOp
        Matrix to diagonalize.

    Returns:
        LazyLinearOp
        
    Raises:

    Examples:

    References:
        See also `scipy.linalg.eigvals function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigvals.html>`_.
    """
    def _matmat(a, x):
        if x.ndim == 1:
            x = x.reshape(x.shape[0], 1)
            batch_size = 1
            is_1d = True
        else:
            batch_size = x.shape[1]
            is_1d = False
        if 'complex' in a.dtype.str:
            y = np.empty((a.shape[0], batch_size), dtype=np.complex_)
        else:
            y = np.empty((a.shape[0], batch_size), dtype=x.dtype)
        if isLazyLinearOp(a):
            # TODO: do better than that
            D = diag(sp.linalg.eigvals(np.eye(a.shape[0], M=a.shape[0], k=0) @ a), k=0)
        else:
            D = diag(sp.linalg.eigvals(a), k=0)
        # TODO: parallel computation
        for b in range(batch_size):
            y[:, b] = D @ x[:, b]
        return y.ravel() if is_1d else y

    return LazyLinearOp(
        shape=a.shape,
        matmat=lambda x: _matmat(a, x),
        rmatmat=lambda x: _matmat(a, x)
    )


def svd(a: np.ndarray):
    """Constructs a diagonal matrix from the singular values of
    matrix a as a lazy linear operator S.

    Args:
        a: np.ndarray or LazyLinearOp
        Matrix to compute SVD.

    Returns:
        LazyLinearOp
        
    Raises:

    Examples:

    References:
        See also `scipy.linalg.svd function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.svd.html>`_.
    """

    def _matmat(a, x):
        if x.ndim == 1:
            x = x.reshape(x.shape[0], 1)
            batch_size = 1
            is_1d = True
        else:
            batch_size = x.shape[1]
            is_1d = False
        L = min(a.shape[0], a.shape[1])
        if 'complex' in a.dtype.str:
            y = np.empty((L, batch_size), dtype=np.complex_)
        else:
            y = np.empty((L, batch_size), dtype=x.dtype)
        if isLazyLinearOp(a):
            # TODO: do better than that
            D = diag(
                sp.linalg.svd(
                    np.eye(a.shape[0], M=a.shape[0], k=0) @ a,
                    full_matrices=True, compute_uv=False
                ), k=0
            )
        else:
            D = diag(sp.linalg.svd(a, full_matrices=True, compute_uv=False), k=0)
        # TODO: parallel computation
        for b in range(batch_size):
            y[:, b] = D @ x[:, b]
        return y.ravel() if is_1d else y

    L = min(a.shape[0], a.shape[1])
    return LazyLinearOp(
        shape=(L, L),
        matmat=lambda x: _matmat(a, x),
        rmatmat=lambda x: _matmat(a, x)
    )


def cholesky_multiply(a, lower: bool=False):
    """Constructs a lower triangular matrix L from the
    Cholesky decomposition a = L @ L^H of matrix a as
    a lazy linear operator C.

    Args:
        a: np.ndarray or LazyLinearOp
        Matrix to compute Cholesky decomposition.
        lower: bool, optional
        If False (default) computes the upper-triangular
        Cholesky factorization.

    Returns:
        LazyLinearOp
        
    Raises:
        ValueError:
            a is not a square matrix.

    Examples:

    References:
        See also `scipy.linalg.cholesky function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.cholesky.html>`_.
    """
    if a.shape[0] != a.shape[1]:
        raise ValueError("a is not a square matrix.")

    def _matmat(a, x, lower, H):
        if x.ndim == 1:
            x = x.reshape(x.shape[0], 1)
            batch_size = 1
            is_1d = True
        else:
            batch_size = x.shape[1]
            is_1d = False
        if 'complex' in a.dtype.str:
            y = np.empty((a.shape[0], batch_size), dtype=np.complex_)
        else:
            y = np.empty((a.shape[0], batch_size), dtype=x.dtype)
        if isLazyLinearOp(a):
            # TODO: do better than that
            C = sp.linalg.cholesky(
                    np.eye(a.shape[0], M=a.shape[0], k=0) @ a,
                    lower=lower
                )
        else:
            C = sp.linalg.cholesky(a, lower=lower)
        # TODO: parallel computation
        if H:
            # conjugate transpose
            if lower:
                for b in range(batch_size):
                    for i in range(a.shape[1]):
                        y[i, b] = C[i:a.shape[0], i].conj() @ x[i:a.shape[0], b]
            else:
                for b in range(batch_size):
                    for i in range(a.shape[0]):
                        y[i, b] = C[:(i + 1), i].conj() @ x[:(i + 1), b]
        else:
            if lower:
                for b in range(batch_size):
                    for i in range(a.shape[0]):
                        y[i, b] = C[i, :(i + 1)] @ x[:(i + 1), b]
            else:
                for b in range(batch_size):
                    for i in range(a.shape[0]):
                        y[i, b] = C[i, i:a.shape[1]] @ x[i:a.shape[1], b]
        return y.ravel() if is_1d else y

    return LazyLinearOp(
        shape=a.shape,
        matmat=lambda x: _matmat(a, x, lower, False),
        rmatmat=lambda x: _matmat(a, x, lower, True)
    )


def lu_multiply(a, factor: str='l'):
    """Constructs a lower triangular matrix L or U from the
    LU decomposition a = L @ U of matrix a as a lazy linear operator Op.
    Shape of L is (M, min(M, N)) while shape of U is (min(M, N), N).

    Args:
        a: np.ndarray or LazyLinearOp
        Matrix (shape is (M, N)) to compute LU decomposition.
        factor: str, optional
        If 'l' (default) use L.
        If 'u' use U.

    Returns:
        LazyLinearOp
        
    Raises:

    Examples:

    References:
        See also `scipy.linalg.lu function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.lu.html>`_.
        See also `LU decomposition <https://en.wikipedia.org/wiki/LU_decomposition>`_.
    """

    def _matmat(a, x, factor, H):
        if x.ndim == 1:
            x = x.reshape(x.shape[0], 1)
            batch_size = 1
            is_1d = True
        else:
            batch_size = x.shape[1]
            is_1d = False

        new_dtype = np.complex_ if 'complex' in a.dtype.str else x.dtype

        if isLazyLinearOp(a):
            # TODO: do better than that
            # lu = sp.linalg.lu(
            #     np.eye(a.shape[0], M=a.shape[0], k=0) @ a
            # )
            P, L, U = sp.linalg.lu(
                np.eye(a.shape[0], M=a.shape[0], k=0) @ a
            )
        else:
            # lu = sp.linalg.lu(a)
            P, L, U = sp.linalg.lu(a)
        # print(lu[0])
        # print(P.shape)
        # print("")
        # print(lu[2])
        # print(L.shape)
        # print("")
        # print(lu[1])
        # print(U.shape)
        # print("-----")
        # print(len(lu))

        # TODO: parallel computation
        M, N = a.shape
        K = min(M, N)
        if H:
            # conjugate transpose
            y = np.empty((K if factor == 'l' else N, batch_size), dtype=new_dtype)
            if factor == 'l':
                # Shape of L^H is (K, M)
                for b in range(batch_size):
                    for i in range(K):
                        y[i, b] = L[i:M, i].conj() @ x[i:M, b]
            else:
                # Shape of U^H is (N, K)
                for b in range(batch_size):
                    for i in range(N):
                        y[i, b] = U[:(i + 1), i].conj() @ x[:(i + 1), b]
        else:
            y = np.empty((M if factor == 'l' else K, batch_size), dtype=new_dtype)
            if factor == 'l':
                # Shape of L is (M, K)
                for b in range(batch_size):
                    for i in range(M):
                        y[i, b] = L[i, :(i + 1)] @ x[:(i + 1), b]
            else:
                # Shape of U is (K, N)
                for b in range(batch_size):
                    for i in range(K):
                        y[i, b] = U[i, i:N] @ x[i:N, b]
        return y.ravel() if is_1d else y

    M, N = a.shape
    K = min(M, N)
    return LazyLinearOp(
        shape=(M if factor == 'l' else K, K if factor == 'l' else N),
        matmat=lambda x: _matmat(a, x, factor, False),
        rmatmat=lambda x: _matmat(a, x, factor, True)
    )


def inv(a: np.ndarray):
    """Constructs inverse of a matrix as a lazy linear operator P.

    Args:
        a: np.ndarray
        Matrix to invert

    Returns:
        LazyLinearOp
        
    Raises:

    Examples:

    References:
        See also `scipy.linalg.inv function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.inv.html>`_.
    """

    def _matmat(a, x):
        if x.ndim == 1:
            x = x.reshape(x.shape[0], 1)
            batch_size = 1
            is_1d = True
        else:
            batch_size = x.shape[1]
            is_1d = False
        if 'complex' in a.dtype.str:
            y = np.empty((x.shape[0], batch_size), dtype='complex128')
        else:
            y = np.empty((x.shape[0], batch_size), dtype=x.dtype)
        if isLazyLinearOp(a):
            # TODO: do better than that
            P = aslazylinearoperator(
                sp.linalg.inv(np.eye(a.shape[0], M=a.shape[1], k=0) @ a)
            )
        else:
            P = aslazylinearoperator(sp.linalg.inv(a))
        # TODO: parallel computation
        for b in range(batch_size):
            y[:, b] = P @ x[:, b]
        return y.ravel() if is_1d else y

    return LazyLinearOp(
        shape=a.shape,
        matmat=lambda x: _matmat(a, x),
        rmatmat=lambda x: _matmat(a.T.conj(), x)
    )


def pinv(a: np.ndarray, atol: float=0.0, rtol: float=None):
    """Constructs pseudo-inverse of a matrix as a lazy linear operator P.

    Args:
        a: np.ndarray
        Matrix to pseudo-invert
        atol: float, optional
        Absolute threshold term (default is 0.0).
        rtol: float, optional
        Relative threshold term (default is 0.0).
        See `scipy.linalg.pinv function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.pinv.html>`_ for more details.

    Returns:
        LazyLinearOp
        
    Raises:

    Examples:

    References:
        See also `scipy.linalg.pinv function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.pinv.html>`_.
        See also `Moore-Penrose pseudo-inverse <https://en.wikipedia.org/wiki/Moore%E2%80%93Penrose_inverse>`_.
    """

    def _matmat(a, x):
        if x.ndim == 1:
            x = x.reshape(x.shape[0], 1)
            batch_size = 1
            is_1d = True
        else:
            batch_size = x.shape[1]
            is_1d = False
        y = np.empty(
            (a.shape[1], batch_size),
            dtype=np.complex_ if 'complex' in a.dtype.str else x.dtype
        )
        if isLazyLinearOp(a):
            # TODO: do better than that
            P = aslazylinearoperator(
                sp.linalg.pinv(
                    np.eye(a.shape[0], M=a.shape[1], k=0) @ a,
                    atol, rtol
                )
            )
        else:
            P = aslazylinearoperator(sp.linalg.pinv(a, atol, rtol))
        # TODO: parallel computation
        for b in range(batch_size):
            y[:, b] = P @ x[:, b]
        return y.ravel() if is_1d else y

    # complex conjugation and transposition commute
    # with Moore-Penrose pseudo-inverse
    return LazyLinearOp(
        shape=(a.shape[1], a.shape[0]),
        matmat=lambda x: _matmat(a, x),
        rmatmat=lambda x: _matmat(a.T.conj(), x)
    )


def householder_matrix(v):
    """Constructs an Householder matrix lazy linear operator H
    from a non-zero unit column vector v.

    Args:
        v: 1d array
           non-zero vector (unit column vector)

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            The norm of vector v is zero.

    Examples:

    References:
        See also `Householder transformation <https://en.wikipedia.org/wiki/Householder_transformation>`_.
    """

    norm = np.sqrt(np.dot(v, v))
    if norm == 0.0:
        raise ValueError("The norm of vector v is zero.")

    def _matmat(v, x):
        if x.ndim == 1:
            is_1d = True
            x = x.reshape(x.shape[0], 1)
        else:
            is_1d = False
        L = x.shape[0]
        batch_size = x.shape[1]
        y = np.empty(x.shape, dtype=x.dtype)
        for i in range(batch_size):
            y[:, i] = np.subtract(v[:, i], np.multiply(2.0, v @ (v.T.conj() @ x[:, i])))
        if is_1d:
            return y.ravel()
        else:
            return y

    return LazyLinearOp(
        shape=(v.shape[0], v.shape[0]),
        matmat=lambda x: _matmat(np.multiply(1.0 / norm, v), x),
        rmatmat=lambda x: _matmat(np.multiply(1.0 / norm, v), x)
    )


def expm(L, scale: float=1.0, nmax: int=8, backend: str='scipy', use_numba: bool=False):
    """Constructs exponentiation of linear operator L as a lazy linear operator E(L).
    Of note, it is only an approximation E(L) @ X ~= sum((scale * L)^i / factorial(i), i=0 to nmax) @ X.

    Args:
        L: 2d array
            Linear operator.
        scale: float, optional
            Scale factor expm(scale * L) (default is 1).
        nmax: int, optional
            Stop the serie expansion after nmax (default is 8).
        backend: str, optional
            It can be 'scipy' (default) to use scipy.linalg.expm function.
            nmax parameter is useless if backend is 'scipy'.
            It can be 'serie' to use a serie expansion of expm(scale * L).
        use_numba: bool, optional
            If True, use prange from Numba (default is False)
            to compute batch in parallel.
            It is useful only and only if the batch size and
            the length of a are big enough.

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.
        ValueError
            backend value is either 'scipy' or 'serie'.
        ValueError
            If L is a 2d array, backend must be 'scipy'.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop import eye
        >>> from lazylinop.wip.linear_algebra import expm
        >>> scale = 0.01
        >>> coefficients = np.array([1.0, scale, 0.5 * scale ** 2])
        >>> N = 10
        >>> L = np.eye(N, n=N, k=0)
        >>> E1 = expm(L, scale=scale, nmax=4)
        >>> E2 = sp.linalg.expm(scale * L)
        >>> np.allclose(E1.toarray(), E2)
        >>> E3 = eye(N, n=N, k=0)
        >>> X = np.random.rand(N, 2 * N)
        >>> np.allclose(E2 @ X, E3 @ X)

    References:
        See also `scipy.linalg.expm function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.expm.html>`_.
        See also :py:func:`lazylinop.wip.polynomial.polyval`.
    """
    if backend == 'scipy':
        if isLazyLinearOp(L):#type(L) is np.ndarray:
            raise ValueError("If L is a 2d array, backend must be 'scipy'.")
        if use_numba:
            M = sp.linalg.expm(scale * L)
            import numba as nb
            from numba import prange, set_num_threads, threading_layer
            nb.config.DISABLE_JIT = 0 if use_numba else 1
            nb.config.THREADING_LAYER = 'omp'
            @nb.jit(nopython=True, parallel=True, cache=True)
            def _matmat(M, x):
                if x.ndim == 1:
                    is_1d = True
                    batch_size = 1
                    x = x.reshape(x.shape[0], 1)
                else:
                    is_1d = False
                batch_size = x.shape[1]
                if use_numba:
                    y = np.empty((M.shape[0], batch_size), dtype=x.dtype)
                    for b in prange(batch_size):
                        y[:, b] = M @ X[:, b]
                else:
                    y = M @ X
                return y.ravel() if is_1d else y
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: _matmat(M, X),
                rmatmat=lambda X: _matmat(M.T.conj(), X)
            )
        else:
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: sp.linalg.expm(scale * L) @ X,
                rmatmat=lambda X: sp.linalg.expm(scale * L.T.conj()) @ X
            )
    if backend == 'scipy':
        if isLazyLinearOp(L):#type(L) is np.ndarray:
            raise ValueError("If L is a 2d array, backend must be 'scipy'.")
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: sp.linalg.expm(scale * L) @ X,
            rmatmat=lambda X: sp.linalg.expm(scale * L.T.conj()) @ X
        )
    elif backend == 'serie':
        from lazylinop.wip.polynomial import polyval
        coefficients = np.empty(nmax + 1, dtype=np.float64)
        factor = 1.0
        factorial = 1.0
        for i in range(nmax + 1):
            coefficients[i] = factor / factorial
            factor *= scale
            factorial *= (i + 1)
        return polyval(coefficients, L)
    else:
        raise ValueError("backend value is either 'scipy' or 'serie'.")


def logm(L, scale: float=1.0, nmax: int=8, backend: str='scipy', use_numba: str=False):
    """Constructs logarithm of linear operator L as a lazy linear operator Log(L).
    Of note, it is only an approximation Log(L) @ X ~= sum((-1)^(n + 1) * (L - Id)^n / n, n=1 to nmax) @ X.

    Args:
        L: 2d array
        Linear operator.
        scale: float, optional
        Scale factor logm(scale * L) (default is 1).
        nmax: int, optional
        Stop the serie expansion after nmax (default is 8).
        backend: str, optional
        It can be 'scipy' (default) to use scipy.linalg.logm function.
        nmax parameter is useless if backend is 'scipy'.
        It can be 'serie' to use a serie expansion of logm(scale * L).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.
        ValueError
            backend value is either 'scipy' or 'serie'.
        ValueError
            nmax must be >= 1.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop import eye
        >>> from lazylinop.wip.linear_algebra import logm
        >>> scale = 0.01
        >>> N = 10
        >>> E1 = logm(eye(N, n=N, k=0), scale=scale, nmax=4, backend='scipy')
        >>> E2 = sp.linalg.logm(scale * np.eye(N, M=N, k=0))
        >>> X = np.random.rand(N, 2 * N)
        >>> np.allclose(E1 @ X, E2 @ X)

    References:
        See also `scipy.linalg.logm function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.logm.html>`_.
        See also `logarithm of a matrix <https://en.wikipedia.org/wiki/Logarithm_of_a_matrix>`_.
    """
    if True or backend == 'scipy':
        # backend has to be 'scipy' because 'serie' is not precise enough
        if isLazyLinearOp(L):
            L = np.eye(L.shape[0], M=L.shape[0]) @ L
        if use_numba:
            M = sp.linalg.logm(scale * L)
            import numba as nb
            from numba import prange, set_num_threads, threading_layer
            nb.config.DISABLE_JIT = 0 if use_numba else 1
            nb.config.THREADING_LAYER = 'omp'
            @nb.jit(nopython=True, parallel=True, cache=True)
            def _matmat(M, x):
                if x.ndim == 1:
                    is_1d = True
                    batch_size = 1
                    x = x.reshape(x.shape[0], 1)
                else:
                    is_1d = False
                batch_size = x.shape[1]
                if use_numba:
                    y = np.empty((M.shape[0], batch_size), dtype=x.dtype)
                    for b in prange(batch_size):
                        y[:, b] = M @ X[:, b]
                else:
                    y = M @ X
                return y.ravel() if is_1d else y
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: _matmat(M, X),
                rmatmat=lambda X: _matmat(M.T.conj(), X)
            )
        else:
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: sp.linalg.logm(scale * L) @ X,
                rmatmat=lambda X: sp.linalg.logm(scale * L.T.conj()) @ X
            )
    elif backend == 'serie':
        if nmax < 1:
            raise ValueError("nmax must be >= 1.")
        def _matmat(L, x):
            if L.shape[1] != x.shape[0]:
                raise ValueError("L @ x does not work because # of columns of L is not equal to the # of rows of x.")
            if x.ndim == 1:
                is_1d = True
                batch_size = 1
                x = x.reshape(x.shape[0], 1)
            else:
                is_1d = False
            batch_size = x.shape[1]
            Lx = np.empty(L.shape[0], dtype=x.dtype)
            # Taylor expansion
            # It uses the equation log(scale * L) ~= sum((-1)^(n + 1) * (scale * L - Id)^n / n, n=1 to nmax)
            y = np.subtract(np.multiply(scale, L @ x), x)
            if nmax > 2:
                # loop over the batch size
                for b in range(batch_size):
                    # compute (scale * L - Id) @ x
                    np.subtract(np.multiply(scale, L @ x[:, b]), x[:, b], out=Lx)
                    for n in range(2, nmax):
                        factor = (2 * (n % 2) - 1) / n
                        np.add(y[:, b], np.multiply(factor, Lx), out=y[:, b])
                        np.subtract(np.multiply(scale, L @ Lx), Lx, out=Lx)
            return y.ravel() if is_1d else y
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: _matmat(L, X),
            rmatmat=lambda X: _matmat(L.T.conj(), X)
        )
    else:
        raise ValueError("backend value is either 'scipy' or 'serie'.")


def cosm(L, scale: float=1.0, nmax: int=8, backend: str='scipy'):
    """Constructs a cosinus of linear operator L as a lazy linear operator C(L).
    It uses the equation expm(i * scale * L) = cos(scale * L) + i * sin(scale * L)
    where i^2 = -1 and returns real part.
    Of note, it is only an approximation (see nmax argument).

    Args:
        L: 2d array
        Linear operator.
        scale: float, optional
        Scale factor cosm(scale * L) (default is 1).
        nmax: int, optional
        Stop the serie expansion after nmax (default is 8).
        backend: str, optional
        It can be 'scipy' (default) to use scipy.linalg.cosm function.
        nmax parameter is useless if backend is 'scipy'.
        It can be 'serie' to use a serie expansion of cosm(scale * L).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.
        ValueError
            backend value is either 'scipy' or 'serie'.
        ValueError
            If L is a 2d array, backend must be 'scipy'.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop import eye
        >>> from lazylinop.wip.linear_algebra import cosm
        >>> scale = 0.01
        >>> coefficients = np.array([1.0, scale, 0.5 * scale ** 2])
        >>> N = 10
        >>> L = np.eye(N, n=N, k=0)
        >>> E1 = cosm(L, scale=scale, nmax=4)
        >>> E2 = sp.linalg.cosm(scale * L)
        >>> np.allclose(E1.toarray(), E2)
        >>> E3 = eye(N, n=N, k=0)
        >>> X = np.random.rand(N, 2 * N)
        >>> np.allclose(E2 @ X, E3 @ X)

    References:
        See also `scipy.linalg.cosm function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.cosm.html>`_.
        See also :py:func:`expm`.
        See also :py:func:`lazylinop.wip.polynomial.polyval`.
    """
    if backend == 'scipy':
        if isLazyLinearOp(L):#type(L) is np.ndarray:
            raise ValueError("If L is a 2d array, backend must be 'scipy'.")
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: sp.linalg.cosm(scale * L) @ X,
            rmatmat=lambda X: sp.linalg.cosm(scale * L.T.conj()) @ X
        )
    elif backend == 'serie':
        from lazylinop.wip.polynomial import polyval
        coefficients = np.empty(nmax + 1, dtype=np.float64)
        factor = 1.0
        sign = 1
        for i in range(nmax + 1):
            if (i % 2) == 0:
                coefficients[i] = sign * factor
                sign *= -1
            else:
                coefficients[i] = 0.0
            factor *= scale / (i + 1)
        return polyval(coefficients, L)
    else:
        raise ValueError("backend value is either 'scipy' or 'serie'.")


def sinm(L, scale: float=1.0, nmax: int=8, backend: str='scipy'):
    """Constructs a cosinus of linear operator L as a lazy linear operator C(L).
    It uses the equation expm(i * scale * L) = cos(scale * L) + i * sin(scale * L)
    where i^2 = -1 and returns imaginary part.
    Of note, it is only an approximation (see nmax argument).

    Args:
        L: 2d array
        Linear operator.
        scale: float, optional
        Scale factor sinm(scale * L) (default is 1).
        nmax: int, optional
        Stop the serie expansion after nmax (default is 8).
        backend: str, optional
        It can be 'scipy' (default) to use scipy.linalg.sinm function.
        nmax parameter is useless if backend is 'scipy'.
        It can be 'serie' to use a serie expansion of sinm(scale * L).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.
        ValueError
            backend value is either 'scipy' or 'serie'.
        ValueError
            If L is a 2d array, backend must be 'scipy'.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop import eye
        >>> from lazylinop.wip.linear_algebra import sinm
        >>> scale = 0.01
        >>> coefficients = np.array([1.0, scale, 0.5 * scale ** 2])
        >>> N = 10
        >>> L = np.eye(N, n=N, k=0)
        >>> E1 = sinm(L, scale=scale, nmax=4)
        >>> E2 = sp.linalg.sinm(scale * L)
        >>> np.allclose(E1.toarray(), E2)
        >>> E3 = eye(N, n=N, k=0)
        >>> X = np.random.rand(N, 2 * N)
        >>> np.allclose(E2 @ X, E3 @ X)

    References:
        See also `scipy.linalg.sinm function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.sinm.html>`_.
        See also :py:func:`expm`.
        See also :py:func:`lazylinop.wip.polynomial.polyval`.
    """
    if backend == 'scipy':
        if isLazyLinearOp(L):#type(L) is np.ndarray:
            raise ValueError("If L is a 2d array, backend must be 'scipy'.")
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: sp.linalg.sinm(scale * L) @ X,
            rmatmat=lambda X: sp.linalg.sinm(scale * L.T.conj()) @ X
        )
    elif backend == 'serie':
        from lazylinop.wip.polynomial import polyval
        coefficients = np.empty(nmax + 1, dtype=np.float64)
        factor = 1.0
        sign = 1
        for i in range(nmax + 1):
            if (i % 2) == 1:
                coefficients[i] = sign * factor
                sign *= -1
            else:
                coefficients[i] = 0.0
            factor *= scale / (i + 1)
        return polyval(coefficients, L)
    else:
        raise ValueError("backend value is either 'scipy' or 'serie'.")


def coshm(L, scale: float=1.0, nmax: int=8, backend: str='scipy', use_numba: bool=False):
    """Constructs an hyperbolic cosine of linear operator L as a lazy linear operator C(L).
    It uses the equation 2 * cosh(z) = exp(scale * L) + exp(-scale * L).
    Of note, it is only an approximation (see nmax argument).

    Args:
        L: 2d array
        Linear operator.
        scale: float, optional
        Scale factor cosh(scale * L) (default is 1).
        nmax: int, optional
        Stop the serie expansion after nmax (default is 8).
        backend: str, optional
        It can be 'scipy' (default) to use scipy.linalg.coshm function.
        nmax parameter is useless if backend is 'scipy'.
        It can be 'serie' to use a serie expansion of coshm(scale * L).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.
        ValueError
            backend value is either 'scipy' or 'serie'.
        ValueError
            nmax must be >= 1.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop import eye
        >>> from lazylinop.wip.linear_algebra import coshm
        >>> scale = 0.01
        >>> N = 10
        >>> L = np.eye(N, M=N, k=0)
        >>> E1 = coshm(L, scale=scale, nmax=32, backend='serie')
        >>> E2 = sp.linalg.coshm(scale * L)
        >>> E3 = coshm(eye(N, n=N, k=0), scale=scale, nmax=32, backend='serie')
        >>> X = np.random.rand(N, 2 * N)
        >>> np.allclose(E1 @ X, E2 @ X)
        True
        >>> np.allclose(E2 @ X, E3 @ X)
        True

    References:
        See also `scipy.linalg.coshm function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.coshm.html>`_.
    """
    if backend == 'scipy':
        if isLazyLinearOp(L):
            L = np.eye(L.shape[0], M=L.shape[0]) @ L
        if use_numba:
            C = sp.linalg.coshm(scale * L) @ X
            import numba as nb
            from numba import prange, set_num_threads, threading_layer
            nb.config.DISABLE_JIT = 0 if use_numba else 1
            nb.config.THREADING_LAYER = 'omp'
            @nb.jit(nopython=True, parallel=True, cache=True)
            def _matmat(C, x):
                if x.ndim == 1:
                    is_1d = True
                    x = x.reshape(x.shape[0], 1)
                else:
                    is_1d = False
                batch_size = x.shape[1]
                if use_numba:
                    y = np.empty((C.shape[0], batch_size), dtype=x.dtype)
                    for b in prange(batch_size):
                        y[:, b] = C @ X[:, b]
                else:
                    y = C @ X
                return y.ravel() if is_1d else y
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: _matmat(C, X),
                rmatmat=lambda X: _matmat(C.T.conj(), X)
            )
        else:
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: sp.linalg.coshm(scale * L) @ X,
                rmatmat=lambda X: sp.linalg.coshm(scale * L.T.conj()) @ X
            )
    elif backend == 'serie':
        if nmax < 1:
            raise ValueError("nmax must be >= 1.")
        def _matmat(L, x):
            if L.shape[1] != x.shape[0]:
                raise ValueError("L @ x does not work because # of columns of L is not equal to the # of rows of x.")
            if x.ndim == 1:
                is_1d = True
                x = x.reshape(x.shape[0], 1)
            else:
                is_1d = False
            batch_size = x.shape[1]
            y = np.copy(x)
            # Taylor expansion
            # exp(scale * L) ~= Id + scale * L + (scale * L) ** 2 / 2 + ...
            # exp(-scale * L) ~= Id - scale * L + (scale * L) ** 2 / 2 + ...
            # cosh(scale * L) ~= Id + (scale * L) ** 2 / 2 + ...
            if nmax > 1:
                Lx = np.empty(L.shape[0], dtype=x.dtype)
                # loop over the batch size
                for b in range(batch_size):
                    pfactor = scale
                    mfactor = -scale
                    np.copyto(Lx, L @ x[:, b])
                    for i in range(1, nmax):
                        if (i % 2) == 0:
                            np.add(y[:, b], np.multiply(0.5 * (pfactor + mfactor), Lx), out=y[:, b])
                        pfactor *= scale / (i + 1)
                        mfactor *= -scale / (i + 1)
                        np.copyto(Lx, L @ Lx)
            return y.ravel() if is_1d else y
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: _matmat(L, X),
            rmatmat=lambda X: _matmat(L.T.conj(), X)
        )
    else:
        raise ValueError("backend value is either 'scipy' or 'serie'.")


def sinhm(L, scale: float=1.0, nmax: int=8, backend: str='scipy', use_numba: bool=False):
    """Constructs an hyperbolic cosine of linear operator L as a lazy linear operator S(L).
    It uses the equation 2 * sinh(z) = exp(scale * L) - exp(-scale * L).
    Of note, it is only an approximation (see nmax argument).

    Args:
        L: 2d array
        Linear operator.
        scale: float, optional
        Scale factor cosh(scale * L) (default is 1).
        nmax: int, optional
        Stop the serie expansion after nmax (default is 8).
        backend: str, optional
        It can be 'scipy' (default) to use scipy.linalg.sinhm function.
        nmax parameter is useless if backend is 'scipy'.
        It can be 'serie' to use a serie expansion of sinhm(scale * L).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.
        ValueError
            backend value is either 'scipy' or 'serie'.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop import eye
        >>> from lazylinop.wip.linear_algebra import sinhm
        >>> scale = 0.01
        >>> N = 10
        >>> L = np.eye(N, M=N, k=0)
        >>> E1 = sinhm(L, scale=scale, nmax=32, backend='serie')
        >>> E2 = sp.linalg.sinhm(scale * L)
        >>> E3 = sinhm(eye(N, n=N, k=0), scale=scale, nmax=32, backend='serie')
        >>> X = np.random.rand(N, 2 * N)
        >>> np.allclose(E1 @ X, E2 @ X)
        True
        >>> np.allclose(E2 @ X, E3 @ X)
        True

    References:
        See also `scipy.linalg.sinhm function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.sinhm.html>`_.
    """
    if backend == 'scipy':
        if isLazyLinearOp(L):
            L = np.eye(L.shape[0], M=L.shape[0]) @ L
        if use_numba:
            S = sp.linalg.sinhm(scale * L) @ X
            import numba as nb
            from numba import prange, set_num_threads, threading_layer
            nb.config.DISABLE_JIT = 0 if use_numba else 1
            nb.config.THREADING_LAYER = 'omp'
            @nb.jit(nopython=True, parallel=True, cache=True)
            def _matmat(S, x):
                if x.ndim == 1:
                    is_1d = True
                    x = x.reshape(x.shape[0], 1)
                else:
                    is_1d = False
                batch_size = x.shape[1]
                if use_numba:
                    y = np.empty((S.shape[0], batch_size), dtype=x.dtype)
                    for b in prange(batch_size):
                        y[:, b] = S @ X[:, b]
                else:
                    y = S @ X
                return y.ravel() if is_1d else y
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: _matmat(S, X),
                rmatmat=lambda X: _matmat(S.T.conj(), X)
            )
        else:
            return LazyLinearOp(
                shape=L.shape,
                matmat=lambda X: sp.linalg.sinhm(scale * L) @ X,
                rmatmat=lambda X: sp.linalg.sinhm(scale * L.T.conj()) @ X
            )
    elif backend == 'serie':
        def _matmat(L, x):
            if L.shape[1] != x.shape[0]:
                raise ValueError("L @ x does not work because # of columns of L is not equal to the # of rows of x.")
            if x.ndim == 1:
                is_1d = True
                x = x.reshape(x.shape[0], 1)
            else:
                is_1d = False
            batch_size = x.shape[1]
            y = np.zeros((L.shape[0], batch_size), dtype=x.dtype)
            Lx = np.empty(L.shape[0], dtype=x.dtype)
            # loop over the batch size
            for b in range(batch_size):
                # Taylor expansion
                # exp(scale * L) ~= Id + scale * L + (scale * L) ** 2 / 2 + ...
                # exp(-scale * L) ~= Id - scale * L + (scale * L) ** 2 / 2 + ...
                # sinh(scale * L) ~= scale * L + ...
                pfactor = scale
                mfactor = -scale
                if nmax > 1:
                    np.copyto(Lx, L @ x[:, b])
                    for i in range(1, nmax):
                        if (i % 2) == 1:
                            np.add(y[:, b], np.multiply(0.5 * (pfactor - mfactor), Lx), out=y[:, b])
                        pfactor *= scale / (i + 1)
                        mfactor *= -scale / (i + 1)
                        np.copyto(Lx, L @ Lx)
            return y.ravel() if is_1d else y
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: _matmat(L, X),
            rmatmat=lambda X: _matmat(L.T.conj(), X)
        )
    else:
        raise ValueError("backend value is either 'scipy' or 'serie'.")


def sqrtm(L, scale: float=1.0, nmax: int=8, backend: str='scipy', use_numba: bool=False):
    """Constructs square root of linear operator L as a lazy linear operator R(L).
    It uses the equation L^1/2 = sum((-1)^n * (1/2 n) * (Id - L)^n, n=0 to inf).
    Of note, it is only an approximation (see nmax argument).

    Args:
        L: 2d array
        Linear operator.
        scale: float, optional
        Scale factor cosh(scale * L) (default is 1).
        nmax: int, optional
        Stop the serie expansion after nmax (default is 8).
        backend: str, optional
        It can be 'scipy' (default) to use scipy.linalg.sqrtm function.
        nmax parameter is useless if backend is 'scipy'.
        It can be 'serie' to use a serie expansion of sqrtm(scale * L).

    Returns:
        LazyLinearOp

    Raises:
        ValueError
            L @ x does not work because # of columns of L is not equal to the # of rows of x.
        ValueError
            backend value is either 'scipy' or 'serie'.
        ValueError
            If L is a 2d array, backend must be 'scipy'.

    Examples:
        >>> import numpy as np
        >>> import scipy as sp
        >>> from lazylinop import eye
        >>> from lazylinop.wip.linear_algebra import sqrtm
        >>> scale = 0.01
        >>> N = 10
        >>> L = np.eye(N, n=N, k=0)
        >>> E1 = sqrtm(L, scale=scale, nmax=4, backend='serie')
        >>> E2 = sp.linalg.sqrtm(scale * L)
        >>> np.allclose(E1.toarray(), E2)
        >>> E3 = eye(N, n=N, k=0)
        >>> X = np.random.rand(N, 2 * N)
        >>> np.allclose(E2 @ X, E3 @ X)

    References:
        See also `scipy.linalg.sqrtm function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.sqrtm.html>`_.
    """
    if True or backend == 'scipy':
        # backend has to be 'scipy' because 'serie' is not precise enough
        if isLazyLinearOp(L):
            R = sp.linalg.sqrtm(scale * np.eye(L.shape[0], M=L.shape[0]) @ L) @ X
        else:
            R = sp.linalg.sqrtm(scale * L) @ X
        import numba as nb
        from numba import prange, set_num_threads, threading_layer
        nb.config.DISABLE_JIT = 0 if use_numba else 1
        nb.config.THREADING_LAYER = 'omp'
        @nb.jit(nopython=True, parallel=True, cache=True)
        def _matmat(R, x):
            if x.ndim == 1:
                is_1d = True
                batch_size = 1
                x = x.reshape(x.shape[0], 1)
            else:
                is_1d = False
            batch_size = x.shape[1]
            if use_numba:
                y = np.empty((R.shape[0], batch_size), dtype=x.dtype)
                for b in prange(batch_size):
                    y[:, b] = R @ X[:, b]
            else:
                y = R @ X
            return y.ravel() if is_1d else y
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: _matmat(R, X),
            rmatmat=lambda X: _matmat(R.T.conj(), X)
        )
        # return LazyLinearOp(
        #     shape=L.shape,
        #     matmat=lambda X: sp.linalg.sqrtm(scale * L) @ X,
        #     rmatmat=lambda X: sp.linalg.sqrtm(scale * L.T.conj()) @ X
        # )
    elif backend == 'serie':
        def _matmat(L, x):
            if L.shape[1] != x.shape[0]:
                raise ValueError("L @ x does not work because # of columns of L is not equal to the # of rows of x.")
            if x.ndim == 1:
                is_1d = True
                batch_size = 1
                x = x.reshape(x.shape[0], 1)
            else:
                is_1d = False
            batch_size = x.shape[1]
            Lx = np.empty(L.shape[0], dtype=x.dtype)
            # Taylor expansion
            # It uses the equation (scale * L)^1/2 = sum((-1)^n * (1/2 n) * (Id - scale * L)^n, n=0 to inf)
            y = np.copy(x)
            if nmax > 1:
                # loop over the batch size
                for b in range(batch_size):
                    # compute (Id - scale * L) @ x
                    np.subtract(x[:, b], np.multiply(scale, L @ x[:, b]), out=Lx)
                    for n in range(1, nmax):
                        # factor = (1 - 2 * (n % 2)) * sp.special.comb(0.5, n)
                        factor = (1 - 2 * (n % 2)) * sp.special.binom(0.5, n)
                        np.add(y[:, b], np.multiply(factor, Lx), out=y[:, b])
                        np.subtract(Lx, np.multiply(scale, L @ Lx), out=Lx)
            return y.ravel() if is_1d else y
        return LazyLinearOp(
            shape=L.shape,
            matmat=lambda X: _matmat(L, X),
            rmatmat=lambda X: _matmat(L.T.conj(), X)
        )
    else:
        raise ValueError("backend value is either 'scipy' or 'serie'.")
