import smtplib
from dataclasses import dataclass
from email.message import EmailMessage
from pathlib import Path
from uuid import uuid4

from app.core.config import Settings
from app.models.lead import Lead


@dataclass(frozen=True)
class EmailResult:
    delivered: bool
    location: str


class EmailService:
    def __init__(self, settings: Settings):
        self.settings = settings

    def send_lead_notifications(self, lead: Lead) -> list[EmailResult]:
        prospect = EmailMessage()
        prospect["Subject"] = "We received your information"
        prospect["From"] = self.settings.from_email
        prospect["To"] = lead.email
        prospect.set_content(
            f"Hi {lead.first_name},\n\n"
            "Thanks for reaching out. An attorney will review your information and contact you soon.\n\n"
            "Alma Legal"
        )

        attorney = EmailMessage()
        attorney["Subject"] = f"New lead: {lead.first_name} {lead.last_name}"
        attorney["From"] = self.settings.from_email
        attorney["To"] = self.settings.internal_attorney_email
        attorney.set_content(
            "A new lead was submitted.\n\n"
            f"Name: {lead.first_name} {lead.last_name}\n"
            f"Email: {lead.email}\n"
            f"Resume: {lead.resume_filename}\n"
            f"Internal UI: {self.settings.public_web_url}/internal\n"
        )

        return [self._send(message) for message in (prospect, attorney)]

    def _send(self, message: EmailMessage) -> EmailResult:
        if not self.settings.smtp_host:
            return self._write_to_outbox(message)

        smtp_class = smtplib.SMTP_SSL if self.settings.smtp_use_ssl else smtplib.SMTP
        with smtp_class(self.settings.smtp_host, self.settings.smtp_port, timeout=10) as smtp:
            if self.settings.smtp_use_tls and not self.settings.smtp_use_ssl:
                smtp.starttls()
            if self.settings.smtp_username and self.settings.smtp_password:
                smtp.login(self.settings.smtp_username, self.settings.smtp_password)
            smtp.send_message(message)
        return EmailResult(delivered=True, location=f"smtp://{self.settings.smtp_host}")

    def _write_to_outbox(self, message: EmailMessage) -> EmailResult:
        self.settings.outbox_dir.mkdir(parents=True, exist_ok=True)
        path = Path(self.settings.outbox_dir) / f"{uuid4()}.eml"
        path.write_text(message.as_string(), encoding="utf-8")
        return EmailResult(delivered=False, location=str(path))
