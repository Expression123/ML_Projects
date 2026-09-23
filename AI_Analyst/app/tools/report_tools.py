
from agents import function_tool, RunContextWrapper
import os
import smtplib
from email.message import EmailMessage
from agents import function_tool
from app.context.context import AnalystContext



@function_tool
def get_inspection_output(
    ctx: RunContextWrapper[AnalystContext]
):
    """Returns the inspection results."""
    return ctx.context.inspection_output.model_dump()


@function_tool
def get_cleaning_plan(
    ctx: RunContextWrapper[AnalystContext]
):
    """Returns the cleaning plan."""
    return ctx.context.cleaning_plan.model_dump()


@function_tool
def get_cleaning_output(
    ctx: RunContextWrapper[AnalystContext]
):
    """Returns the cleaning execution results."""
    return ctx.context.cleaning_output.model_dump()


@function_tool
def get_analysis_output(
    ctx: RunContextWrapper[AnalystContext]
):
    """Returns the analysis results."""
    return ctx.context.analysis_output.model_dump()


@function_tool
def send_html_email(subject: str, html_body: str):
    """
    Sends an HTML report via email.
    """

    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))

    to_email = os.getenv("EMAIL_ADDRESS")

    msg = EmailMessage()

    msg["From"] = email_address
    msg["To"] = to_email
    msg["Subject"] = subject

    # Plain-text fallback
    msg.set_content("This email contains the data analysis report.")

    # Actual HTML report
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_address, email_password)
        server.send_message(msg)

    return {"status": "success"}





