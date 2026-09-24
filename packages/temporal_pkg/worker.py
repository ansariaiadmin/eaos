import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from . import activities, workflows


async def main():
    client = await Client.connect("localhost:7233")
    worker = Worker(client, task_queue="agent-os",
                    workflows=[workflows.DailyCloseWorkflow, workflows.LegalResearchWorkflow],
                    activities=[activities.run_reconciliation, activities.check_trading_risk,
                                activities.redact_snapshot, activities.run_tax_snapshot,
                                activities.legal_rag])
    async with worker:
        await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
