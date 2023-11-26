import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class SMTPClient:
    """
    A simple SMTP client for sending emails.

    Attributes:
        smtp_server (str): The address of the SMTP server.
        smtp_port (int): The port of the SMTP server (default is 587).
        user (str): The username for SMTP server authentication (default is None).
        password (str): The password for SMTP server authentication (default is None).
    """

    def __init__(self, smtp_server, smtp_port=587, user=None, password=None):
        """
        Initialize a new SMTPClient instance.

        Args:
            smtp_server (str): The address of the SMTP server.
            smtp_port (int): The port of the SMTP server.
            user (str, optional): The username for SMTP server authentication. Defaults to None.
            password (str, optional): The password for SMTP server authentication. Defaults to None.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.user = user
        self.password = password

    def send_email(self, sender, recipients, subject, body_text=None, body_html=None, attachments=None):
        """
        Send an email using the SMTP server.

        Args:
            sender (str): The email address of the sender.
            recipients (list): A list of email addresses to send the email to.
            subject (str): The subject of the email.
            body_text (str, optional): The plain text version of the email body. Defaults to None.
            body_html (str, optional): The HTML version of the email body. Defaults to None.
            attachments (list of str, optional): A list of file paths for files to be attached. Defaults to None.
        """
        # Create a MIMEMultipart object to represent the email
        msg = MIMEMultipart()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = ", ".join(recipients)

        # Add text body to email if provided
        if body_text:
            text_part = MIMEText(body_text, 'plain')
            msg.attach(text_part)

        # Add HTML body to email if provided
        if body_html:
            html_part = MIMEText(body_html, 'html')
            msg.attach(html_part)

        # Add attachments to the email if provided
        if attachments:
            for file_path in attachments:
                with open(file_path, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename={file_path.split('/')[-1]}",
                    )
                    msg.attach(part)

        # Establish a connection to the SMTP server
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            # StartTLS for security
            server.starttls()

            # Login if necessary
            if self.user and self.password:
                server.login(self.user, self.password)

            # Send the email
            server.sendmail(sender, recipients, msg.as_string())


if __name__ == "__main__":
    # Example usage
    client = SMTPClient("smtp.example.com", 587, "your_username", "your_password")

    client.send_email(
        sender="sender@example.com",
        recipients=["recipient1@example.com", "recipient2@example.com"],
        subject="Test Subject",
        body_text="This is the body of the email in plain text.",
        body_html="<h1>This is the body of the email in HTML.</h1>",
        attachments=["path_to_file1.txt", "path_to_image.jpg"]
    )
