from app.context.context import AnalystContext
from agents import function_tool
from agents import RunContextWrapper


@function_tool
def get_inspection_results(
    ctx: RunContextWrapper[AnalystContext]
):
    """
    Returns the inspection results from the Inspection Agent.
    """

    return ctx.context.inspection_output.model_dump()


@function_tool
def get_target_column(
    ctx: RunContextWrapper[AnalystContext],
):
    """
    Returns the target column
    """

    return ctx.context.target_column
