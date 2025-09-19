from __future__ import annotations
import numpy as np
import re
from typing import List, Dict, Any
from .vectorstore import InMemoryVectorStore

_token_re = re.compile(r"[A-Za-z0-9\u3040-\u30FF\u4E00-\u9FFF]+")

class TinyEmbedder:
    def __init__(self, dim: int = 384, seed: int = 42):
        self.dim = dim
        self.rng = np.random.RandomState(seed)

    def _tokens(self, text: str) -> List[str]:
        return _token_re.findall(text.lower())

    def encode(self, texts: List[str]) -> np.ndarray:
        vecs = []
        for t in texts:
            toks = self._tokens(t)
            if not toks:
                vecs.append(np.zeros(self.dim, dtype=np.float32))
                continue
            acc = np.zeros(self.dim, dtype=np.float32)
            for tok in toks:
                h = abs(hash(tok)) % self.dim
                acc[h] += 1.0
            acc /= max(len(toks), 1)
            vecs.append(acc)
        return np.vstack(vecs).astype(np.float32)

class RagService:
    def __init__(self, dim: int = 384, max_corpus: int = 100000):
        self.embedder = TinyEmbedder(dim=dim)
        self.store = InMemoryVectorStore(dim=dim, max_corpus=max_corpus)

    def ingest(self, items: List[Dict[str, Any]]):
        texts = [it["text"] for it in items]
        metas = []
        for it in items:
            m = dict(it.get("meta", {}))
            m["id"] = it["id"]
            m["preview"] = it["text"][:160]
            metas.append(m)
        vecs = self.embedder.encode(texts)
        self.store.add(vecs, metas)

    def query(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        qv = self.embedder.encode([query])[0]
        return self.store.search(qv, top_k=top_k)
