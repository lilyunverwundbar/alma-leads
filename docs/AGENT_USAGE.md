# Coding Agent Usage

## Short Writeup

I used Codex as the primary coding agent to scaffold and implement the full-stack application. I delegated broad repo creation, FastAPI route/model/service code, NextJS pages/components, styling, and documentation drafts. I kept direct human judgment on product shape, security boundaries, local-demo tradeoffs, and final review decisions because those choices need to match the assignment constraints.

One subtle issue the agent could have produced was accepting arbitrary uploaded file types or pretending email was sent when no provider was configured. I caught that during review and made the resume service allow only PDF/DOC/DOCX MIME types, plus made local email delivery write inspectable `.eml` files to an outbox. That gives both a safer public endpoint and a truthful local E2E workflow.

## Representative Prompt Excerpts

User prompt excerpt:

> Build an application to support creating, getting and updating leads. Use FastAPI, NextJS, storage persistence, email integration, production-like structure, and include run/design/agent usage docs.

Agent planning excerpt:

> Create a small monorepo with backend FastAPI, frontend NextJS, SQLite persistence, SMTP-compatible email with local outbox fallback, internal bearer-token auth, and docs required for submission.

Implementation review excerpt:

> Verify public submission persists a PENDING lead, sends prospect and attorney notifications, internal auth guards list/update APIs, and attorneys can transition a lead to REACHED_OUT.

## What Was Delegated

- Repository structure and boilerplate.
- FastAPI application setup, schemas, models, services, and routes.
- NextJS screens for public intake and internal review.
- Local runbook, design document, and notes.
- Focused backend tests.

## What Was Hand-Directed

- Choosing SQLite plus local resume storage for the assignment.
- Adding SMTP as the real email integration boundary with filesystem fallback for demos.
- Keeping internal auth intentionally simple but isolated behind FastAPI dependencies.
- Documenting production upgrades and risks.
