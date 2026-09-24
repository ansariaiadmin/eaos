"""Tax integration adapters. Deterministic, offline-testable, minor units."""
from __future__ import annotations

from abc import ABC, abstractmethod
from decimal import Decimal


class TaxAdapter(ABC):
    name = "base"
    @abstractmethod
    def compute(self, taxable_minor: int) -> dict: ...

from typing import ClassVar


class USFederalTaxAdapter(TaxAdapter):
    """2024 single-filer marginal brackets, integer minor units (1 minor = 1e-4)."""
    name = "us_federal"
    BRACKETS: ClassVar[list] = [(116_000_000, "0.10"), (471_500_000, "0.12"),
                (1_005_250_000, "0.22"), (1_919_500_000, "0.24"),
                (2_437_250_000, "0.32"), (6_093_500_000, "0.35"), (None, "0.37")]

    def compute(self, taxable_minor: int) -> dict:
        tax, remaining, prev = 0, Decimal(taxable_minor), Decimal(0)
        for upper, rate in self.BRACKETS:
            r = Decimal(rate)
            if upper is None:
                tax += int((remaining - prev) * r)
                break
            upper = Decimal(upper)
            if remaining > upper:
                tax += int((upper - prev) * r)
                prev = upper
            else:
                tax += int((remaining - prev) * r)
                break
        return {"jurisdiction": self.name, "tax_minor": tax}

class IRAnonymizedAdapter(TaxAdapter):
    name = "ir_anonymized"
    def compute(self, taxable_minor: int) -> dict:
        return {"jurisdiction": self.name, "tax_minor": int(Decimal(taxable_minor) * Decimal("0.15")),
                "note": "anonymized flat placeholder rate"}

ADAPTERS = {a.name: a for a in [USFederalTaxAdapter(), IRAnonymizedAdapter()]}
