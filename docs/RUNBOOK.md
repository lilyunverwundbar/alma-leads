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
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

The API will be available at `http://127.0.0.1:8000`.

Useful endpoints:

- `GET /health`
- `POST /api/leads`
- `POST /api/auth/login`
- `GET /api/leads`
- `PATCH /api/leads/{lead_id}`

By default, email is written to `backend/storage/outbox/*.eml`. To send real email, set `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`, `FROM_EMAIL`, and `INTERNAL_ATTORNEY_EMAIL` in `backend/.env`. I used SendGrid and used my own personal email for atterney and from email.

## Frontend

```bash
cd frontend
cp .env.example .env.local
npm install
npm run dev -- --hostname 127.0.0.1 --port 3000
```

Open `http://127.0.0.1:3000/lead`.

Internal login defaults from `backend/.env.example`:

- Email: `attorney@company.com`
- Password: `change-me`

## E2E Demo Script

1. Open `/lead`.
2. Submit first name, last name, email, and a PDF/DOC/DOCX resume.
3. Confirm success message.
4. Check the prospect and attorney inboxes.
5. Open `/internal`.
6. Sign in with attorney credentials defined in backend/.env.
7. Verify the lead appears with `PENDING` state.
8. Click `Reached out`.
9. Verify the lead state changes to `REACHED_OUT`.

## Tests

```bash
cd backend
source .venv/bin/activate
pytest
```

## View Local Data

Leads are stored in SQLite at:

```text
backend/storage/leads.db
```

From the repo root, view leads with:

```bash
sqlite3 backend/storage/leads.db "select id, first_name, last_name, email, state, created_at from leads order by created_at desc;"
```

For a more visual option, open the file with a SQLite browser app such as DB Browser for SQLite.
