import pandas as pd
from agents import function_tool, RunContextWrapper
from app.context.context import AnalystContext





@function_tool
def fill_missing_values(
    ctx: RunContextWrapper[AnalystContext],
    columns: list[str],
    method: str,
):
    """
    Fill missing values for multiple columns.
    """

    df = ctx.context.df
    report = []

    for column in columns:

        if column not in df.columns:
            continue

        missing = int(df[column].isna().sum())

        if missing == 0:
            continue

        if method == "mean":
            value = df[column].mean()

        elif method == "median":
            value = df[column].median()

        else:
            value = df[column].mode().iloc[0]

        df[column] = df[column].fillna(value)

        report.append({
            "column": column,
            "rows_modified": missing,
            "filled_with": str(value)
        })

    return report


@function_tool
def remove_duplicates(
    ctx: RunContextWrapper[AnalystContext],
):
    """
    Remove duplicate rows.
    """

    df = ctx.context.df

    before = len(df)

    df.drop_duplicates(inplace=True)

    after = len(df)

    return {
        "rows_removed": before - after
    }


@function_tool
def drop_missing_rows(
    ctx: RunContextWrapper[AnalystContext],
):
    """
    Drop rows containing missing values.
    """

    df = ctx.context.df

    before = len(df)

    df.dropna(inplace=True)

    after = len(df)

    return {
        "rows_removed": before - after
    }





from pydantic import BaseModel, ConfigDict


class ColumnConversion(BaseModel):
    model_config = ConfigDict(extra="forbid")

    column: str
    dtype: str


@function_tool
def clean_and_convert_column(
    ctx: RunContextWrapper[AnalystContext],
    column_name: str
) -> str:
    """
    Converts a numeric-like text column into a numeric dtype.

    Removes common formatting such as currency symbols, commas,
    and surrounding whitespace before conversion.
    """

    df = ctx.context.df

    if column_name not in df.columns:
        return f"Column '{column_name}' does not exist."

    original_dtype = str(df[column_name].dtype)

    cleaned = (
        df[column_name]
        .astype("string")
        .str.strip()
        .str.replace(r"[$₦€£¥]", "", regex=True)
        .str.replace(",", "", regex=False)
    )

    converted = pd.to_numeric(
        cleaned,
        errors="coerce"
    )

    df[column_name] = converted

    new_dtype = str(df[column_name].dtype)

    return (
        f"Column '{column_name}' converted successfully: "
        f"{original_dtype} → {new_dtype}."
    )

from agents import function_tool, RunContextWrapper

@function_tool
def get_cleaning_plan(
    ctx: RunContextWrapper[AnalystContext],
):
    """
    Returns the approved cleaning plan.
    """

    return ctx.context.cleaning_plan.model_dump()



@function_tool
def detect_outliers(
    ctx: RunContextWrapper[AnalystContext],
    columns: list[str],
):
    """
    Detects potential outliers using the IQR method.
    Does not modify the dataset.
    """

    df = ctx.context.df

    report = []

    for column in columns:

        if column not in df.columns:
            continue

        if not pd.api.types.is_numeric_dtype(df[column]):
            continue

        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = df[
            (df[column] < lower) |
            (df[column] > upper)
        ][column]

        report.append({
            "column": column,
            "lower_bound": float(lower),
            "upper_bound": float(upper),
            "outlier_count": int(len(outliers)),
            "suspected_values": outliers.tolist()
        })

    return report
