"""Planner — query → decomposition to tasks."""
from __future__ import annotations

import re


class Planner:
    """Decomposes a query into specialist tasks."""

    def __init__(self):
        # Keyword patterns for each specialist
        self.patterns = {
            "legal": [r"legal", r"gdpr", r"ccpa", r"sox", r"irs", r"compliance", r"law", r"قانون", r"حقوق", r"data.*minim"],
            "tax": [r"tax", r"irs", r"bracket", r"مالیات", r"taxable"],
            "trading": [r"trade", r"order", r"position", r"equity", r"معامله", r"خرید", r"فروش"],
            "voice": [r"voice", r"audio", r"stt", r"tts", r"صوت", r"صدا"],
        }

    def decompose(self, query: str, retry: bool = False) -> list[dict]:
        """Decompose query into tasks."""
        q_lower = query.lower()
        tasks = []

        # Detect specialists via keyword overlap
        for specialist, patterns in self.patterns.items():
            for pat in patterns:
                if re.search(pat, q_lower):
                    tasks.append({
                        "id": f"{specialist}-{len(tasks)+1}",
                        "type": specialist,
                        "query": query,
                        "params": self._extract_params(query, specialist),
                        "retry": retry,
                    })
                    break

        # If no specialist detected, create general tasks
        if not tasks:
            tasks.append({
                "id": "general-1",
                "type": "legal",  # default to legal for enterprise OS
                "query": query,
                "params": {"k": 3},
                "retry": retry,
            })

        # If query mentions multiple domains, ensure all are covered
        # e.g., "check trading tax implications" → trading + tax
        if len(tasks) == 1 and not retry:
            # Check if query has multiple intents
            extra = []
            for specialist in self.patterns:
                if specialist not in [t["type"] for t in tasks]:
                    for pat in self.patterns[specialist]:
                        if re.search(pat, q_lower):
                            extra.append(specialist)
                            break
            for spec in extra:
                tasks.append({
                    "id": f"{spec}-{len(tasks)+1}",
                    "type": spec,
                    "query": query,
                    "params": self._extract_params(query, spec),
                    "retry": retry,
                })

        return tasks

    def _extract_params(self, query: str, specialist: str) -> dict:
        """Extract specialist-specific params from query."""
        params = {}
        if specialist == "tax":
            # Try to extract taxable amount
            m = re.search(r"(\d+)", query)
            if m:
                params["taxable"] = int(m.group(1)) * 10_000  # minor units
            else:
                params["taxable"] = 500_000_000  # default 50k
            params["jurisdiction"] = "us_federal" if "us" in query.lower() or "federal" in query.lower() else "ir_anonymized"
        elif specialist == "trading":
            m = re.search(r"order.*?(\d+)", query.lower())
            params["order_value"] = float(m.group(1)) if m else 5000.0
            params["equity"] = 100000.0
            params["position"] = 0.0
        elif specialist == "legal":
            params["k"] = 3
        elif specialist == "voice":
            params["audio"] = query.encode("utf-8")
        return params
