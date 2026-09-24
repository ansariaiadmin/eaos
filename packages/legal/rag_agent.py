"""Legal RAG agent: BM25-style retrieval + citations, always local routing."""
from __future__ import annotations
import json, pathlib, math, re
from packages.core.router import Router

class LegalRAGAgent:
    def __init__(self, kb_path="packages/legal/kb.json"):
        self.docs = json.loads(pathlib.Path(kb_path).read_text())["docs"]
        self.router = Router()

    def _search(self, query, k=3):
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

    def answer(self, query):
        route = self.router.route(query, task_type="legal")
        hits = self._search(query)
        return {"answer": "Based on %d retrieved sources (routed to %s)." % (len(hits), route["provider"]),
                "citations": [d["id"] for d in hits],
                "snippets": [d["text"] for d in hits],
                "route": route}
