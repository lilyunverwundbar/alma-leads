# System Design

## Goals

The application supports a public lead intake form and an authenticated internal attorney workflow. Prospects submit contact information and a resume/CV. The system persists the lead, queues two email notifications, and lets attorneys review and manually move the lead from `PENDING` to `REACHED_OUT`.

## Architecture

- NextJS serves the browser UI.
- FastAPI owns API validation, authentication, persistence, file upload handling, and email integration.
- SQLite stores lead metadata for local development.
- The filesystem stores uploaded resumes in `backend/storage/resumes`.
- SMTP sends email in configured environments. Local development writes `.eml` files to `backend/storage/outbox`.

This keeps the assignment easy to run locally while preserving a production-oriented boundary: the frontend never writes directly to storage, and the backend is the source of truth for lead state.

## Data Model

`Lead`

- `id`
- `first_name`
- `last_name`
- `email`
- `resume_filename`
- `resume_path`
- `state`: `PENDING` or `REACHED_OUT`
- `created_at`
- `updated_at`

The public response exposes the original resume filename but not the server filesystem path.

## API Design

- `POST /api/leads`: public multipart endpoint. Validates required fields and resume type, stores the resume, persists a `PENDING` lead, and sends prospect and attorney emails.
- `POST /api/auth/login`: returns a short-lived JWT for the configured internal attorney user.
- `GET /api/leads`: authenticated endpoint to list leads newest-first.
- `PATCH /api/leads/{lead_id}`: authenticated endpoint to update lead state.

## Authentication

The internal UI uses a bearer token from `/api/auth/login`. For this exercise, a single configured attorney account is enough to demonstrate the guarded UI. In production, this would be replaced with SSO/OIDC and role-based access control.

## Email

The email service is SMTP-compatible so it can work with providers such as SendGrid, Postmark, SES SMTP, or a company mail relay. When `SMTP_HOST` is unset, messages are written to an outbox directory. This avoids fake success during local demos: reviewers can inspect the exact generated emails.

## Production Considerations

- Replace SQLite with Postgres.
- Store resumes in object storage with private signed URLs.
- Add migrations through Alembic.
- Move email delivery to a background job queue.
- Add antivirus scanning for uploaded resumes.
- Add duplicate detection and rate limiting on the public form.
- Use managed identity/auth for internal users.
- Add structured logging, tracing, and audit history for state transitions.
