from __future__ import annotations
import numpy as np
from typing import List, Dict, Any

class InMemoryVectorStore:
    def __init__(self, dim: int = 384, max_corpus: int = 100000):
        self.dim = dim
        self.max_corpus = max_corpus
        self._vectors = np.empty((0, dim), dtype=np.float32)
        self._metas: List[Dict[str, Any]] = []

    @staticmethod
    def _normalize(v: np.ndarray) -> np.ndarray:
        n = np.linalg.norm(v, axis=1, keepdims=True) + 1e-12
        return v / n

    def add(self, vectors: np.ndarray, metas: List[Dict[str, Any]]):
        if vectors.ndim != 2 or vectors.shape[1] != self.dim:
            raise ValueError(f"vector dim mismatch: expected {self.dim}, got {vectors.shape}")
        if len(metas) != vectors.shape[0]:
            raise ValueError("vectors and metas length mismatch")
        self._vectors = np.vstack([self._vectors, vectors]).astype(np.float32)
        self._metas.extend(metas)
        if self._vectors.shape[0] > self.max_corpus:
            overflow = self._vectors.shape[0] - self.max_corpus
            self._vectors = self._vectors[overflow:, :]
            self._metas = self._metas[overflow:]

    def search(self, query_vec: np.ndarray, top_k: int = 5) -> List[Dict[str, Any]]:
        if self._vectors.shape[0] == 0:
            return []
        q = query_vec.astype(np.float32)
        if q.ndim == 1:
            q = q[None, :]
        A = self._normalize(self._vectors)
        b = self._normalize(q)
        sims = A @ b.T
        idx = np.argsort(-sims.ravel())[:top_k]
        results = []
        for i in idx:
            m = dict(self._metas[i])
            m["score"] = float(sims[i, 0])
            results.append(m)
        return results
