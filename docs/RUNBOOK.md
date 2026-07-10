# Local Runbook

## Prerequisites

- Python 3.12+
- Node 20+
- npm

## Backend

```bash
cd backend
cp .env.example .env
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

Useful endpoints:

- `GET /health`
- `POST /api/leads`
- `POST /api/auth/login`
- `GET /api/leads`
- `PATCH /api/leads/{lead_id}`

By default, email is written to `backend/storage/outbox/*.eml`. To send real email, set `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `FROM_EMAIL`, and `INTERNAL_ATTORNEY_EMAIL` in `backend/.env`.

## Frontend

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev
```

Open `http://localhost:3000/lead`.

Internal login defaults from `backend/.env.example`:

- Email: `attorney@company.com`
- Password: `change-me`

## E2E Demo Script

1. Open `/lead`.
2. Submit first name, last name, email, and a PDF/DOC/DOCX resume.
3. Confirm success message.
4. Check `backend/storage/outbox` for prospect and attorney emails.
5. Open `/internal`.
6. Sign in with attorney credentials.
7. Verify the lead appears with `PENDING` state.
8. Click `Reached out`.
9. Verify the lead state changes to `REACHED_OUT`.

## Tests

```bash
cd backend
source .venv/bin/activate
pytest
```
