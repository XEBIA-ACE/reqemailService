# Implementation of email service using SMTP and AWS SES

from typing import Protocol

class EmailService(Protocol):
    def send_email(self, to_address: str, subject: str, message: str) -> bool: # Type hint added
        """Send an email using the specified service."""
        pass


class SmtpEmailService:
    def send_email(self, to_address: str, subject: str, message: str) -> bool: # Type hint added
        # TODO: Implement SMTP logic
        print(f"Sending email to {to_address} via SMTP...")
        return True


class AwsSesEmailService:
    def send_email(self, to_address: str, subject: str, message: str) -> bool: # Type hint added
        # TODO: Implement AWS SES logic
        print(f"Sending email to {to_address} via AWS SES...")
        return True