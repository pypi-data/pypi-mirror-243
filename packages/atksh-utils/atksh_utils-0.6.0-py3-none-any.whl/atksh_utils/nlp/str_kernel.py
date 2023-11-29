from typing import List

import numba as nb
import numpy as np
import numpy.typing as npt

__all__ = ["build_kernel"]


@nb.njit("f8(i8[:], i8[:], i8, f8)", fastmath=True, cache=True, inline="never")
def ssk_array(s: npt.NDArray, t: npt.NDArray, n: int, lam: float) -> float:
    lens = len(s)
    lent = len(t)
    k_prim = np.zeros((n, lens, lent), dtype=nb.float32)
    k_prim[0, :, :] = 1

    for i in range(1, n):
        for sj in range(i, lens):
            toret = 0.0
            for tk in range(i, lent):
                if s[sj - 1] == t[tk - 1]:
                    toret = lam * (toret + lam * k_prim[i - 1, sj - 1, tk - 1])
                else:
                    toret *= lam
                k_prim[i, sj, tk] = toret + lam * k_prim[i, sj - 1, tk]

    k = 0.0
    for i in range(n):
        for sj in range(i, lens):
            for tk in range(i, lent):
                if s[sj] == t[tk]:
                    k += lam * lam * k_prim[i, sj, tk]

    return k


@nb.njit("f8[:, :](i8[:, :], i8[:], i8, f8)", parallel=True, fastmath=True, cache=True)
def _build_kernel(
    tokens: npt.NDArray,
    lens: npt.NDArray,
    n: int,
    lam: float,
) -> npt.NDArray:
    b = len(tokens)
    idx_total = b * (b - 1) // 2 + b

    mat = np.zeros((b, b), dtype=nb.float64)
    idxes = [(i, j) for i in range(b) for j in range(i, b)]
    assert len(idxes) == idx_total

    for idx in nb.prange(idx_total):
        i, j = idxes[idx]
        tokens_i = tokens[i][: lens[i]]
        tokens_j = tokens[j][: lens[j]]
        tmp = ssk_array(tokens_i, tokens_j, n, lam)
        mat[i, j] = tmp
        mat[j, i] = tmp
    norm = np.diag(mat).reshape(b, 1)
    return np.divide(mat, np.sqrt(norm.T * norm))


def build_kernel(s: List[str], n: int, lam: float) -> npt.NDArray:
    """Build a Gram matrix with string subsequence kernel."""
    b = len(s)
    tokens = list()
    for i in range(b):
        tokens.append(np.array([ord(x) for x in s[i]], dtype=np.int64))
    lens = np.array([len(t) for t in tokens], dtype=np.int64)
    maxlen = np.max(lens)
    tokens = np.stack(
        [np.pad(t, (0, maxlen - len(t))) for t in tokens],  # pyre-ignore
        axis=0,
    )
    return _build_kernel(tokens, lens, n, lam)
