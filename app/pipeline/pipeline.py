
from agents import Runner, RunConfig, OpenAIProvider
from openai import AsyncOpenAI
from agents.mcp import MCPServerStdio
from app.prompts import prompts
from app.context.context import AnalystContext

from app.agents.inspection_agent import inspection_agent
from app.agents.cleaning_agent import cleaning_agent
from app.agents.cleaning_plan_agent import cleaning_plan_agent
from app.agents.analysis_agent import analysis_agent
from app.agents.report_agent import create_report_agent

from app.mcp.file_system import files_params


# async def run_pipeline(df, target_column=None, email_address=None, openai_api_key=None):

#     # --------------------------------------------------
#     # Create shared context
#     # --------------------------------------------------

#     context = AnalystContext(
#         df=df,
#         target_column=target_column,
#         email_address=email_address,
#         openai_api_key=openai_api_key
#     )

#     print("\nStarting Data Analysis Pipeline...\n")

#     # --------------------------------------------------
#     # 1. Inspection
#     # --------------------------------------------------

#     print("Running Inspection Agent...")

#     inspection_result = await Runner.run(
#         inspection_agent,
#         prompts.INSPECTION_USER_PROMPT,
#         context=context
#     )

#     context.inspection_output = inspection_result.final_output

#     print("✓ Inspection completed\n")

#     # --------------------------------------------------
#     # 2. Cleaning Plan
#     # --------------------------------------------------

#     print("Running Cleaning Plan Agent...")

#     cleaning_plan_result = await Runner.run(
#         cleaning_plan_agent,
#         prompts.CLEANING_PLAN_USER_PROMPT,
#         context=context
#     )

#     context.cleaning_plan = cleaning_plan_result.final_output

#     print("✓ Cleaning plan completed\n")

#     # --------------------------------------------------
#     # 3. Cleaning
#     # --------------------------------------------------

#     print("Running Cleaning Agent...")

#     cleaning_result = await Runner.run(
#         cleaning_agent,
#         prompts.CLEANING_USER_PROMPT,
#         context=context
#     )

#     context.cleaning_output = cleaning_result.final_output

#     print("✓ Cleaning completed\n")

#     # --------------------------------------------------
#     # 4. Analysis
#     # --------------------------------------------------

#     print("Running Analysis Agent...")

#     analysis_result = await Runner.run(
#         analysis_agent,
#         prompts.ANALYSIS_USER_PROMPT,
#         context=context
#     )

#     context.analysis_output = analysis_result.final_output

#     print("✓ Analysis completed\n")

#     # --------------------------------------------------
#     # 5. Report
#     # --------------------------------------------------

#     print("Running Report Agent...")

#     async with MCPServerStdio(
#         params=files_params,
#         client_session_timeout_seconds=90
#     ) as mcp_server_files:

#         report_agent = create_report_agent(mcp_server_files)

#         report_result = await Runner.run(
#             report_agent,
#             prompts.REPORT_USER_PROMPT,
#             context=context
#         )

#     context.report_output = report_result.final_output

#     print("✓ Report completed\n")

#     print("===================================")
#     print("Pipeline completed successfully!")
#     print("===================================\n")

#     return context




async def run_pipeline(
    df,
    target_column=None,
    email_address=None,
    openai_api_key=None
):
    # --------------------------------------------------
    # Create shared context
    # --------------------------------------------------
    context = AnalystContext(
        df=df,
        target_column=target_column,
        email_address=email_address
    )

    # Create an OpenAI client specifically for this run
    openai_client = AsyncOpenAI(
        api_key=openai_api_key
    )

    model_provider = OpenAIProvider(
        openai_client=openai_client
    )

    run_config = RunConfig(
        model_provider=model_provider
    )

    print("\nStarting Data Analysis Pipeline...\n")

    # --------------------------------------------------
    # 1. Inspection
    # --------------------------------------------------
    print("Running Inspection Agent...")

    inspection_result = await Runner.run(
        inspection_agent,
        prompts.INSPECTION_USER_PROMPT,
        context=context,
        run_config=run_config
    )

    context.inspection_output = inspection_result.final_output
    print("✓ Inspection completed\n")

    # --------------------------------------------------
    # 2. Cleaning Plan
    # --------------------------------------------------
    print("Running Cleaning Plan Agent...")

    cleaning_plan_result = await Runner.run(
        cleaning_plan_agent,
        prompts.CLEANING_PLAN_USER_PROMPT,
        context=context,
        run_config=run_config
    )

    context.cleaning_plan = cleaning_plan_result.final_output
    print("✓ Cleaning plan completed\n")

    # --------------------------------------------------
    # 3. Cleaning
    # --------------------------------------------------
    print("Running Cleaning Agent...")

    cleaning_result = await Runner.run(
        cleaning_agent,
        prompts.CLEANING_USER_PROMPT,
        context=context,
        run_config=run_config
    )

    context.cleaning_output = cleaning_result.final_output
    print("✓ Cleaning completed\n")

    # --------------------------------------------------
    # 4. Analysis
    # --------------------------------------------------
    print("Running Analysis Agent...")

    analysis_result = await Runner.run(
        analysis_agent,
        prompts.ANALYSIS_USER_PROMPT,
        context=context,
        run_config=run_config
    )

    context.analysis_output = analysis_result.final_output
    print("✓ Analysis completed\n")

    # --------------------------------------------------
    # 5. Report
    # --------------------------------------------------
    print("Running Report Agent...")

    async with MCPServerStdio(
        params=files_params,
        client_session_timeout_seconds=90
    ) as mcp_server_files:

        report_agent = create_report_agent(mcp_server_files)

        report_result = await Runner.run(
            report_agent,
            prompts.REPORT_USER_PROMPT,
            context=context,
            run_config=run_config
        )

    context.report_output = report_result.final_output
    print("✓ Report completed\n")

    print("===================================")
    print("Pipeline completed successfully!")
    print("===================================\n")

    return context


