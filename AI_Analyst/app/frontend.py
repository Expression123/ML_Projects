import gradio as gr
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
from app.pipeline.pipeline import run_pipeline
import os


def load_dataset(file):
    if file is None:
        return None, gr.update(choices=[]), "Please upload a CSV file."

    try:
        df = pd.read_csv(file.name)

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
        return None, gr.update(choices=[]), f"Error loading dataset: {str(e)}"

async def analyze_dataset(file, target_column):

    if file is None:
        return "Please upload a CSV dataset first.", None, None

    try:
        df = pd.read_csv(file)

        if target_column == "None / I don't know":
            target_column = None

        context = await run_pipeline(
            df=df,
            target_column=target_column
        )

        report = context.report_output

        if report is None:
            return "The pipeline completed, but no report was generated.", None, None
        
    
        SANDBOX_PATH = os.path.abspath(os.path.join(os.getcwd(), "sandbox"))

        report_path = os.path.join(SANDBOX_PATH, report.report_file_path)


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
            "✅ Analysis completed successfully.",
            report_path
        )

    except Exception as e:
        return f"Analysis failed:\n\n{str(e)}", None, None


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

            analyze_button = gr.Button(
                "🚀 Analyze Dataset",
                variant="primary"
            )

            status = gr.Markdown(
                "Upload a CSV file to get started."
            )

        with gr.Column(scale=2):

            preview = gr.Dataframe(
                label="Dataset Preview",
                interactive=False
            )

            report = gr.Markdown(
                label="Analysis Report"
            )

            download_file = gr.File(label="Download Report")
        
    

    file_input.change(
        fn=load_dataset,
        inputs=file_input,
        outputs=[preview, target_dropdown, status]
    )

    analyze_button.click(
        fn=analyze_dataset,
        inputs=[file_input, target_dropdown],
        outputs=[report, status, download_file]
    )


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0")