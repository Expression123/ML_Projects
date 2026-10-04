from agents import Agent
from app.tools.inspection_tools import *
from app.context.output import *
from app.prompts import prompts





inspection_agent = Agent(
    name="Inspection Agent",
    instructions=prompts.INSPECTION_SYSTEM_PROMPT,
    model="gpt-4o-mini",
    tools=[inspect_dataset,
           inspect_categorical_columns,
           inspect_outliers],
        
    output_type=InspectionOutput
)