



from pydantic import BaseModel, ConfigDict, Field
from typing import Dict, List
from enum import Enum
from typing import Literal



# inspection structured cleaningoutput



class InspectionFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    inspection: str
    findings: str
    issue_detected: bool
    action_required: bool

class ColumnDataType(BaseModel):
    model_config = ConfigDict(extra="forbid")

    column_name: str
    data_type: str


class DataProfile(BaseModel):
    model_config = ConfigDict(extra="forbid")

    rows: int
    columns: int
    column_names: List[str]
    data_types: List[ColumnDataType]


class InspectionOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    data_profile: DataProfile
    inspection_report: List[InspectionFinding]


# Cleaning Plan Structured Outputs


class CleaningTool(str, Enum):
    FILL_MISSING_VALUES = "fill_missing_values"
    DROP_MISSING_ROWS = "drop_missing_rows"
    REMOVE_DUPLICATES = "remove_duplicates"
    CLEAN_AND_CONVERT_COLUMN = "clean_and_convert_column"
    DETECT_OUTLIERS = "detect_outliers"
    


class CleaningAction(BaseModel):
    model_config = ConfigDict(extra="forbid")

    issue: str
    action: str
    columns_affected: List[str]
    tool_name: CleaningTool | None
    reason: str
    priority: str


class CleaningPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    cleaning_actions: List[CleaningAction]
    summary: str



# cleaning pydantic structured output

class ValueChange(BaseModel):
    model_config = ConfigDict(extra="forbid")

    original_value: str
    new_value: str


class CleaningOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    issue: str
    action: str
    tool_used: str
    columns_affected: List[str]
    rows_modified: int
    reason: str
    status: Literal["completed", "skipped", "failed"]


    value_changes: List[ValueChange] = []




# Analysis Structured Output


from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class AnalysisFinding(BaseModel):
    model_config = ConfigDict(extra="forbid")

    finding: str
    columns: List[str]
    importance: str
    evidence: str


class TargetAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    target_column: str
    distribution: str
    key_findings: List[str]


class RelationshipAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    columns: List[str]
    relationship: str
    strength: Optional[str] = None
    interpretation: str


class AnalysisOutput(BaseModel):

    model_config = ConfigDict(extra="forbid")

    summary: str

    selected_columns: List[str]

    findings: List[AnalysisFinding]

    target_analysis: Optional[TargetAnalysis] = None

    relationships: List[RelationshipAnalysis]

    recommendations: List[str]




# report pydantic output


class ReportOutput(BaseModel):
    title: str = Field(
        description="Title of the final data analysis report."
    )

    markdown_report: str = Field(
        description="Complete professional Markdown version of the final report. "
                    "This exact content will be saved as a .md file."
    )

    html_report: str = Field(
        description="Complete HTML version of the same final report. "
                    "This contains the same information and will be used as the email body."
    )

    report_file_path: str = Field(
        description="The exact Markdown report filename/path relative to the provided sandbox directory."
    )