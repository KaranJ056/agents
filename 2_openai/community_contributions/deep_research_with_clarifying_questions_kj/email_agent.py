import os
from typing import Dict

import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
from agents import Agent, function_tool
from agents.extensions.models.litellm_model import LitellmModel
from dotenv import load_dotenv

load_dotenv(override=True)

@function_tool
def send_email(subject: str, html_body: str) -> Dict[str, str]:
    """ Send an email with the given subject and HTML body """
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email("karan.j@crestskillserve.com") # put your verified sender here
    to_email = To("karanjoshi9809@gmail.com") # put your recipient here
    content = Content("text/html", html_body)
    mail = Mail(from_email, to_email, subject, content).get()
    response = sg.client.mail.send.post(request_body=mail)
    print("Email response", response.status_code)
    return {"status": "success"}

INSTRUCTIONS = """You are able to send a nicely formatted HTML email based on a detailed report.
You will be provided with a detailed report. You should use your tool to send one email, providing the report converted into clean, well presented HTML with an appropriate subject line."""

model = LitellmModel(
    model="gemini/gemini-2.5-flash-lite",
    api_key=os.getenv("GOOGLE_API_KEY")
)

email_agent = Agent(
    name="Email agent",
    instructions=INSTRUCTIONS,
    tools=[send_email],
    model=model,
)