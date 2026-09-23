from agents import function_tool, RunContextWrapper
from app.context.context import AnalystContext




@function_tool
def inspect_dataset(ctx: RunContextWrapper[AnalystContext]):
    """
    Performs a complete inspection of the dataset and returns
    the information required to determine a cleaning plan.
    """

    df = ctx.context.df

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isnull().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_usage": int(df.memory_usage(deep=True).sum()),
        "sample_rows": df.head(5).to_dict(orient="records")
    }

@function_tool
def inspect_categorical_columns(
    ctx: RunContextWrapper[AnalystContext]
):
    """
    Returns unique values for categorical columns
    having a manageable number of distinct values.
    """

    df = ctx.context.df

    report = {}

    categorical = df.select_dtypes(include=["object", "category"])

    for column in categorical.columns:

        unique = df[column].dropna().unique()

        if len(unique) <= 20:

            report[column] = unique.tolist()

        else:

            report[column] = {
                "unique_count": int(len(unique))
            }

    return report

@function_tool
def inspect_outliers(
    ctx: RunContextWrapper[AnalystContext]
):
    """
    Detects outliers in all numeric columns using the IQR rule.
    """

    df = ctx.context.df

    report = {}

    numeric = df.select_dtypes(include="number")

    for column in numeric.columns:

        q1 = numeric[column].quantile(0.25)
        q3 = numeric[column].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        count = int(
            ((numeric[column] < lower) |
             (numeric[column] > upper)).sum()
        )

        report[column] = count

    return report