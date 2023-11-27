import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import List

import jinja2


class EmailContentClass:
    """A class structuring the contents being sent via email. The class also handles
    rendering to html for better looking email messages. Templates for messages can be
    added to the /templates folder.
    """

    def __init__(
        self,
        msg: str,
        subject: str,
        attachments: List[str] = None,
        template_name: str = "default.html",
        template_vars: dict = None,
        tag: str = None,
        signature: str = "The MordorMail Utility",
    ):
        self.msg = msg
        self.subject = subject
        self.tag = tag
        self.attachments = attachments
        self.template_name = template_name
        self.template_vars = {} if template_vars is None else template_vars
        if self.template_vars.get("message", None):
            print("Provided message using template_vars. Overwriting msg attribute")
            self.msg = self.template_vars["message"]
        else:
            self.template_vars["message"] = msg
        if self.template_vars.get("signature", None):
            print(
                "Provided signature using template_vars. "
                "Overwriting signature attribute"
            )
            self.signature = self.template_vars["signature"]
        else:
            self.signature = signature
            self.template_vars["signature"] = signature

        if tag is not None:
            self.subject = f"[{tag}]: {subject}"

    def render_jinja_template(self):
        """Renders the html to be sent in the email. template names refer to file names
        in the /templates directory."""
        rendered_template = self._render_template(
            self.template_name, **self.template_vars
        )
        return rendered_template

    def add_attachments_to_mime_msg(self, msg: MIMEMultipart):
        """Loads all files in the self.attachements list and adds them to the message"""
        if self.attachments is None:
            return msg

        for file_path in self.attachments:
            if not os.path.isfile(file_path):
                print(f"Error: {file_path} does not exist.")
                continue

            filename = os.path.basename(file_path)

            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {filename}",
                )
                msg.attach(part)

        return msg

    @staticmethod
    def _render_template(template, **kwargs):
        """Renders templates using Jinja."""
        template_loader = jinja2.FileSystemLoader(
            Path(__file__).parent.parent / "templates"
        )
        template_env = jinja2.Environment(loader=template_loader)
        templ = template_env.get_template(template)
        return templ.render(**kwargs)
