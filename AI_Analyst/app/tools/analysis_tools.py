from agents import function_tool, RunContextWrapper

from app.context.context import AnalystContext



@function_tool
def get_dataset_profile(
    ctx: RunContextWrapper[AnalystContext]
):
    """
    Returns a high-level profile of the cleaned dataset.
    """

    df = ctx.context.df

    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "data_types": df.dtypes.astype(str).to_dict(),
        "missing_values": df.isna().sum().to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_usage": int(df.memory_usage(deep=True).sum())
    }





@function_tool
def get_numeric_statistics(
    ctx: RunContextWrapper[AnalystContext],
    columns: list[str] | None = None,
):
    """
    Returns descriptive statistics for selected numeric columns.
    If no columns are provided, analyzes all numeric columns.
    """

    df = ctx.context.df

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if columns is not None:
        selected_columns = [
            col for col in columns
            if col in numeric_columns
        ]
    else:
        selected_columns = numeric_columns

    if not selected_columns:
        return {
            "message": "No valid numeric columns selected."
        }

    return (
        df[selected_columns]
        .describe()
        .round(3)
        .to_dict()
    )



@function_tool
def get_categorical_statistics(
    ctx: RunContextWrapper[AnalystContext],
    columns: list[str] | None = None,
):
    """
    Returns frequency distributions for selected categorical columns.
    """

    df = ctx.context.df

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool"]
    ).columns.tolist()

    if columns is not None:
        selected_columns = [
            col for col in columns
            if col in categorical_columns
        ]
    else:
        selected_columns = categorical_columns

    if not selected_columns:
        return {
            "message": "No valid categorical columns selected."
        }

    result = {}

    for column in selected_columns:

        counts = df[column].value_counts(
            dropna=False
        )

        result[column] = {
            str(value): int(count)
            for value, count in counts.items()
        }

    return result


@function_tool
def get_correlation_analysis(
    ctx: RunContextWrapper[AnalystContext],
    columns: list[str] | None = None,
):
    """
    Returns correlations between selected numeric columns.
    """

    df = ctx.context.df

    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if columns is not None:
        selected_columns = [
            col for col in columns
            if col in numeric_columns
        ]
    else:
        selected_columns = numeric_columns

    if len(selected_columns) < 2:
        return {
            "message": "At least two numeric columns are required."
        }

    correlation = df[selected_columns].corr()

    return correlation.round(3).to_dict()


@function_tool
def analyze_target_distribution(
    ctx: RunContextWrapper[AnalystContext]
):
    """
    Analyzes the distribution of the target column.
    """

    df = ctx.context.df
    target = ctx.context.target_column

    if not target:
        return {
            "message": "No target column specified."
        }

    if target not in df.columns:
        return {
            "message": f"Target column '{target}' not found."
        }

    counts = df[target].value_counts(dropna=False)

    percentages = (
        df[target]
        .value_counts(normalize=True, dropna=False)
        .mul(100)
        .round(2)
    )

    return {
        "target": target,
        "unique_values": int(df[target].nunique()),
        "counts": {
            str(k): int(v)
            for k, v in counts.items()
        },
        "percentages": {
            str(k): float(v)
            for k, v in percentages.items()
        }
    }


@function_tool
def analyze_feature_relationship(
    ctx: RunContextWrapper[AnalystContext],
    column: str
):
    """
    Analyzes the relationship between a feature and the target.
    """

    df = ctx.context.df
    target = ctx.context.target_column

    if not target:
        return {
            "message": "No target column specified."
        }

    if column not in df.columns:
        return {
            "message": f"Column '{column}' not found."
        }

    if target not in df.columns:
        return {
            "message": f"Target '{target}' not found."
        }

    result = {
        "feature": column,
        "target": target
    }

    # Numeric feature
    if pd.api.types.is_numeric_dtype(df[column]):

        grouped = (
            df.groupby(target)[column]
            .agg(["count", "mean", "median", "min", "max"])
            .round(3)
        )

        result["analysis"] = grouped.to_dict()

    # Categorical feature
    else:

        result["analysis"] = (
            pd.crosstab(
                df[column],
                df[target],
                normalize="index"
            )
            .round(3)
            .to_dict()
        )

    return result


@function_tool
def analyze_time_column(
    ctx: RunContextWrapper[AnalystContext],
    column: str
):
    """
    Analyzes a datetime column for temporal patterns.
    """

    df = ctx.context.df

    if column not in df.columns:
        return {
            "message": f"Column '{column}' not found."
        }

    dates = pd.to_datetime(
        df[column],
        errors="coerce"
    )

    valid_dates = dates.dropna()

    if valid_dates.empty:
        return {
            "message": "Column does not contain valid datetime values."
        }

    return {
        "column": column,
        "min_date": str(valid_dates.min()),
        "max_date": str(valid_dates.max()),
        "date_range_days": int(
            (valid_dates.max() - valid_dates.min()).days
        ),
        "year_counts": {
            str(k): int(v)
            for k, v in valid_dates.dt.year.value_counts().sort_index().items()
        },
        "month_counts": {
            str(k): int(v)
            for k, v in valid_dates.dt.month.value_counts().sort_index().items()
        }
    }



@function_tool
def get_target_column(
    ctx: RunContextWrapper[AnalystContext],
):
    """Returns the target column."""
    return ctx.context.target_column


@function_tool
def get_inspection_results(
    ctx: RunContextWrapper[AnalystContext],
):
    """Returns the dataset inspection results."""
    return ctx.context.inspection_output.model_dump()


@function_tool
def get_cleaning_output(
    ctx: RunContextWrapper[AnalystContext],
):
    """Returns the cleaning results."""
    return ctx.context.cleaning_output.model_dump()