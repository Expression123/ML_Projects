import asyncio
import pandas as pd
from dotenv import load_dotenv
load_dotenv()

from app.pipeline.pipeline import run_pipeline


async def main():

    df = pd.read_csv("app/data/credit_card_fraud_2026.csv")

    context = await run_pipeline(
        df=df,
        target_column="is_fraud"
    )

    print("Report generated.")
    print(context.report_output)


if __name__ == "__main__":
    asyncio.run(main())