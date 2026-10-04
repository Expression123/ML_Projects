from agents import Agent
from app.tools.cleaning_plan_tools import get_inspection_results, get_target_column
from app.context.output import *
from app.prompts import prompts







cleaning_plan_agent = Agent(
    name="Cleaning Plan Agent",
    instructions=prompts.CLEANING_PLAN_SYSTEM_PROMPT,
    model="gpt-4.1-mini",
    tools=[get_inspection_results, get_target_column],
        
    output_type=CleaningPlan
)