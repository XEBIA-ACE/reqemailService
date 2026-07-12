# EmailService

The EmailService is responsible for sending verification and transactional emails using either SMTP or AWS SES. It includes failover mechanisms to queue and retry delivery if emails cannot be sent immediately.

## Technologies
- **SMTP** for basic email sending capabilities.
- **AWS SES** for scalable and reliable email delivery.

## Directory Structure
- **application/**: Core application logic.
- **domain/**: Business logic interfaces and domain models.
- **infrastructure/**: Implementation of SMTP and AWS SES integrations.
- **interfaces/**: REST API endpoints and input/output management.

## Endpoints
- **/health**: A simple health check endpoint to verify the service is running.

## Setup
To set up the service locally, ensure you have Docker installed and run:
```sh
docker build -t email_service .
docker run -p 8000:8000 email_service
```

Ensure to populate the `.env` file with appropriate values as shown in `.env.example`.
