from dataclasses import dataclass
import pandas as pd
from app.context.output import *


@dataclass
class AnalystContext:

    df: pd.DataFrame

    inspection_output: InspectionOutput | None = None

    target_column: str | None = None


    cleaning_plan: CleaningPlan | None = None

    cleaning_output: CleaningOutput | None = None

    email_address: str | None = None
    openai_api_key: str | None = None
    # verification_output: VerificationOutput | None = None

    

    analysis_output: AnalysisOutput | None = None

    # visualization_output: VisualizationOutput | None = None