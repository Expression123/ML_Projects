from agents import Agent
from app.tools.analysis_tools import *
from app.context.output import *
from app.prompts import prompts







analysis_agent = Agent(
    name="Analysis Agent",
    instructions=prompts.ANALYSIS_SYSTEM_PROMPT,
    model="gpt-4.1-mini",
    tools=[
        get_dataset_profile,
        # check_data_quality,
        get_numeric_statistics,
        get_categorical_statistics,
        get_correlation_analysis,
        analyze_target_distribution,
        analyze_feature_relationship,
        analyze_time_column,
        get_target_column,
        get_inspection_results,
        get_cleaning_output,
        
    ],
    output_type=AnalysisOutput,
)