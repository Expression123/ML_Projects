
import gradio as gr
import pandas as pd
import os

from dotenv import load_dotenv

load_dotenv()

from app.pipeline.pipeline import run_pipeline


def load_dataset(file):

    if file is None:
        return (
            None,
            gr.update(choices=[]),
            "Please upload a CSV file."
        )

    try:
        df = pd.read_csv(file)

        columns = df.columns.tolist()

        return (
            df.head(10),
            gr.update(
                choices=["None / I don't know"] + columns,
                value="None / I don't know"
            ),
            f"Dataset loaded successfully: {len(df):,} rows × {len(df.columns)} columns."
        )

    except Exception as e:
        return (
            None,
            gr.update(choices=[]),
            f"Error loading dataset: {str(e)}"
        )


async def analyze_dataset(
    file,
    target_column,
    openai_api_key,
    email_address
):

    if file is None:
        return "Please upload a CSV dataset first.", None, None

    if not openai_api_key:
        return "Please enter your OpenAI API key.", None, None

    if not email_address:
        return "Please enter your email address.", None, None

    try:

        df = pd.read_csv(file)

        if target_column == "None / I don't know":
            target_column = None

        # Pass the user's API key for this analysis
        os.environ["OPENAI_API_KEY"] = openai_api_key

        context = await run_pipeline(
            df=df,
            target_column=target_column,
            email_address=email_address
        )

        report = context.report_output

        if report is None:
            return (
                "The pipeline completed, but no report was generated.",
                None,
                None
            )

        sandbox_path = os.path.abspath(
            os.path.join(os.getcwd(), "sandbox")
        )

        report_path = os.path.join(
            sandbox_path,
            report.report_file_path
        )

        if not os.path.exists(report_path):
            return (
                "Report was generated, but the saved file could not be found.",
                None,
                None
            )

        with open(report_path, "r", encoding="utf-8") as f:
            markdown_report = f.read()

        return (
            markdown_report,
            "✅ Analysis completed successfully. The report has also been sent to your email.",
            report_path
        )

    except Exception as e:

        return (
            f"Analysis failed:\n\n{str(e)}",
            None,
            None
        )


with gr.Blocks(
    title="Data Analyst AI",
    theme=gr.themes.Soft()
) as demo:

    gr.Markdown(
        """
        # 📊 Data Analyst AI

        Upload your dataset and let the AI inspect, clean, analyze,
        and generate a professional data analysis report.
        """
    )

    with gr.Row():

        # =========================
        # LEFT COLUMN
        # =========================

        with gr.Column(scale=1):

            file_input = gr.File(
                label="Upload Dataset",
                file_types=[".csv"],
                type="filepath"
            )

            target_dropdown = gr.Dropdown(
                label="Target Column",
                choices=[],
                value=None,
                interactive=True,
                info="Choose the target column, or select None if you don't know it."
            )

            openai_api_key = gr.Textbox(
                label="OpenAI API Key",
                placeholder="sk-...",
                type="password",
                info="Your API key is used for this analysis."
            )

            email_address = gr.Textbox(
                label="Email Address",
                placeholder="you@example.com",
                type="email",
                info="Your completed report will be sent to this email."
            )

            analyze_button = gr.Button(
                "🚀 Analyze Dataset",
                variant="primary"
            )

            status = gr.Markdown(
                "Upload a CSV file to get started."
            )

        # =========================
        # RIGHT COLUMN
        # =========================

        with gr.Column(scale=2):

            preview = gr.Dataframe(
                label="Dataset Preview",
                interactive=False
            )

            report = gr.Markdown(
                label="Analysis Report"
            )

            download_file = gr.File(
                label="Download Report"
            )

    # =========================
    # EVENTS
    # =========================

    file_input.change(
        fn=load_dataset,
        inputs=file_input,
        outputs=[
            preview,
            target_dropdown,
            status
        ]
    )

    analyze_button.click(
        fn=analyze_dataset,
        inputs=[
            file_input,
            target_dropdown,
            openai_api_key,
            email_address
        ],
        outputs=[
            report,
            status,
            download_file
        ]
    )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0"
    )
