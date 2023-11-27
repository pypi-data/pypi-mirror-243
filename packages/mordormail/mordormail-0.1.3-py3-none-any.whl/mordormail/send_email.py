import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from mordormail.EmailContentClass import EmailContentClass


def send_email(
    to: List[str],
    sender: str,
    smtp_host: smtplib.SMTP,
    ecc: EmailContentClass,
    cc: List[str] = None,
    bcc: List[str] = None,
):
    """Sends an email using smtp. Content has to be provided using an EmailContentClass."""
    if type(to) is not list:
        to = [to]

    if cc is None:
        cc = []

    if bcc is None:
        bcc = []

    recipients = list(filter(None, to + [cc] + [bcc]))
    to = list(filter(None, to))

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = ",".join(to)
    msg["Cc"] = ",".join(cc)

    msg["Subject"] = ecc.subject
    html_message = ecc.render_jinja_template()
    msg.attach(MIMEText(html_message, "html"))
    msg = ecc.add_attachments_to_mime_msg(msg)

    with smtp_host as server:
        server.sendmail(sender, recipients, msg.as_string())


if __name__ == "__main__":
    # Example Script
    ecc = EmailContentClass(
        msg="WOW! It works...",
        subject="Test Mail",
    )

    send_email(
        to=["tim.j.hudelmaier@gsk.com"],
        sender="noreply-sendmailtest@gsk.com",
        smtp_host=smtplib.SMTP("internal-smtp.gsk.com", 25),
        ecc=ecc,
    )
