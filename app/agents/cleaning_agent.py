from agents import Agent
from app.tools.cleaning_tools import *
from app.context.output import *
from app.prompts import prompts







cleaning_agent = Agent(
    name="Cleaning Execution Agent",
    instructions=prompts.CLEANING_SYSTEM_PROMPT,
    model="gpt-4.1-mini",
    tools=[
        get_cleaning_plan,
        fill_missing_values,
        remove_duplicates,
        drop_missing_rows,
        clean_and_convert_column,
        detect_outliers,
    ],
    output_type=CleaningOutput,
)