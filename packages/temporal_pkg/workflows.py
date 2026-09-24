"""Temporal workflows. Run: temporal server start-dev, then
python -m packages.temporal_pkg.worker"""
from __future__ import annotations
from datetime import timedelta
from temporalio import workflow
from temporalio.common import RetryPolicy

with workflow.unsafe.imports_passed_through():
    from .activities import (run_reconciliation, run_tax_snapshot,
                             check_trading_risk, redact_snapshot, legal_rag)

@workflow.defn
class DailyCloseWorkflow:
    @workflow.run
    async def run(self, business_date: str) -> dict:
        rec = await workflow.execute_activity(run_reconciliation, business_date,
                start_to_close_timeout=timedelta(minutes=10),
                retry_policy=RetryPolicy(maximum_attempts=3))
        risk = await workflow.execute_activity(check_trading_risk, business_date,
                start_to_close_timeout=timedelta(minutes=5))
        _ = await workflow.execute_activity(redact_snapshot, rec,
                start_to_close_timeout=timedelta(minutes=5))
        tax = await workflow.execute_activity(run_tax_snapshot, business_date,
                start_to_close_timeout=timedelta(minutes=10))
        return {"reconciliation": rec, "risk": risk, "tax": tax}

@workflow.defn
class LegalResearchWorkflow:
    @workflow.run
    async def run(self, query: str) -> dict:
        return await workflow.execute_activity(legal_rag, query,
                start_to_close_timeout=timedelta(minutes=15))
