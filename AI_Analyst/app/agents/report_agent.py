from agents import Agent
from app.tools.report_tools import *
from app.context.output import *
from app.prompts import prompts






def create_report_agent(mcp_server_files):

    return Agent(
        name="investigator",
        instructions=prompts.REPORT_SYSTEM_PROMPT,
        model="gpt-4.1-mini",
        mcp_servers=[mcp_server_files],
        output_type=ReportOutput,
        tools=[
            get_inspection_output,
            get_cleaning_plan,
            get_cleaning_output,
            get_analysis_output,
            send_html_email,
        ],
    )