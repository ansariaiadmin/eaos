"""Legal RAG agent: vector store lite (hash embeddings + cosine) + BM25 fallback, always local routing."""
from __future__ import annotations

import json
import math
import pathlib
import re

from packages.core.router import Router

from .vector_store import VectorStoreLite


class LegalRAGAgent:
    def __init__(self, kb_path="packages/legal/kb.json", use_vector=True):
        self.docs = json.loads(pathlib.Path(kb_path).read_text())["docs"]
        self.router = Router()
        self.use_vector = use_vector
        # Init vector store lite
        self.vstore = VectorStoreLite()
        try:
            self.vstore.add_docs(self.docs)
        except Exception as e:  # noqa: BLE001 - fallback to clear on any init error
            print(f"Vector store init failed, clearing: {e}")
            self.vstore.clear()

    def _search_lexical(self, query, k=3):
        """BM25-style lexical fallback."""
        toks = [t for t in re.findall(r"\w+", query.lower()) if len(t) > 2]
        N = len(self.docs)
        scored = []
        for d in self.docs:
            text = d["text"].lower()
            s = 0.0
            for q in toks:
                tf = text.count(q)
                if tf:
                    df = sum(q in x["text"].lower() for x in self.docs)
                    s += math.log((N - df + 0.5) / (df + 0.5) + 1) * tf * 2.2 / (tf + 1.2)
            scored.append((s, d))
        scored.sort(key=lambda x: -x[0])
        return [d for s, d in scored[:k] if s > 0] or [d for _, d in scored[:1]]

    def _search(self, query, k=3):
        """Hybrid search: vector first, fallback lexical."""
        if self.use_vector:
            try:
                v_hits = self.vstore.search(query, k=k)
                if v_hits:
                    # Convert vector hits to doc format
                    return [{"id": h["id"], "text": h["text"], "score": h["score"], "method": h["method"]} for h in v_hits]
            except Exception as e:  # noqa: BLE001 - fallback to lexical on any vector error
                print(f"Vector search failed, fallback lexical: {e}")
        # Fallback to lexical
        lex = self._search_lexical(query, k=k)
        return [{"id": d["id"], "text": d["text"], "score": 0.0, "method": "lexical"} for d in lex]

    def answer(self, query):
        route = self.router.route(query, task_type="legal")
        hits = self._search(query)
        # Ensure citations exist
        method = hits[0].get("method", "lexical") if hits else "none"
        return {"answer": f"Based on {len(hits)} retrieved sources (routed to {route['provider']}) using {method}.",
                "citations": [d["id"] for d in hits],
                "snippets": [d["text"] for d in hits],
                "route": route,
                "retrieval_method": hits[0].get("method", "lexical") if hits else "none",
                "scores": [d.get("score", 0.0) for d in hits]}
