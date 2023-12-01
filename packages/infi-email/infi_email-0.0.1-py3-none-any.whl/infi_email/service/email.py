import smtplib
import ssl
import logging
from email.message import EmailMessage

from infi_email.config import Config


def send_email(from_email: str, email_password: str, to_email: list[str], subject: str, message: str):
    """
    Send an email using the provided data.
    """

    try:
        # Create an SSL context for secure email sending
        context: ssl.SSLContext = ssl.create_default_context()

        # Create an EmailMessage object
        email_instance: EmailMessage = EmailMessage()
        email_instance["From"]: str = from_email
        email_instance["To"]: list[str] = ', '.join(to_email)
        email_instance["subject"]: str = subject
        email_instance.set_content(message)

        # Use SMTP_SSL to securely send the email
        with smtplib.SMTP_SSL(Config.SMTP_SERVER, Config.SMTP_PORT, context=context) as smtp:
            # Login to SMTP server
            smtp.login(from_email, email_password)
            # Send the email
            smtp.sendmail(from_email, to_email, email_instance.as_string())

    except Exception as e:
        logging.error(f"Failed to send email - {str(e)}")
