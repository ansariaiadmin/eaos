"""Vector store lite — hash-based embeddings + cosine with fallback."""
from __future__ import annotations

import hashlib
import math
import re

DIM = 64

def _hash_token(token: str) -> int:
    """Deterministic hash to dim index."""
    h = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return int(h[:8], 16) % DIM

def embed(text: str) -> list[float]:
    """Simple hash embedding: bag-of-tokens hashed to DIM vector, L2 normalized."""
    vec = [0.0] * DIM
    tokens = re.findall(r"\w+", text.lower())
    if not tokens:
        return vec
    for tok in tokens:
        idx = _hash_token(tok)
        vec[idx] += 1.0
    # L2 normalize
    norm = math.sqrt(sum(v*v for v in vec))
    if norm > 0:
        vec = [v / norm for v in vec]
    return vec

def cosine(a: list[float], b: list[float]) -> float:
    """Cosine similarity — assumes normalized but compute generic."""
    if not a or not b:
        return 0.0
    dot = sum(x*y for x, y in zip(a, b))
    # Since embed normalizes, dot is cosine, but compute norms for safety
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(y*y for y in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

class VectorStoreLite:
    """In-memory vector store with hash embeddings."""

    def __init__(self, dim: int = DIM):
        self.dim = dim
        self.docs: list[dict] = []  # each {id, text, embedding}
        self._built = False

    def add_docs(self, docs: list[dict]):
        """Add docs with id and text."""
        for d in docs:
            emb = embed(d.get("text", ""))
            self.docs.append({
                "id": d.get("id"),
                "text": d.get("text", ""),
                "embedding": emb,
            })
        self._built = True

    def search(self, query: str, k: int = 3) -> list[dict]:
        """Search by cosine similarity."""
        if not self._built or not self.docs:
            return []
        q_emb = embed(query)
        scored: list[tuple[float, dict]] = []
        for doc in self.docs:
            score = cosine(q_emb, doc["embedding"])
            scored.append((score, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        # Return top k with score > 0.05 threshold, else top k anyway
        top = scored[:k]
        # Filter very low scores? Keep at least 1 if exists
        filtered = [ (s, d) for s, d in top if s > 0.05 ]
        if filtered:
            return [{"id": d["id"], "text": d["text"], "score": s, "method": "vector"} for s, d in filtered]
        # If no filtered, return top 1 if score > 0
        if top and top[0][0] > 0:
            return [{"id": top[0][1]["id"], "text": top[0][1]["text"], "score": top[0][0], "method": "vector"}]
        return []

    def clear(self):
        self.docs = []
        self._built = False
