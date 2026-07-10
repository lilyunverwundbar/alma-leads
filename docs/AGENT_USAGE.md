# Coding Agent Usage

## Short Writeup

I used Codex as the primary implementation agent, but I kept ownership of the product and architecture decisions. I asked the agent to scaffold the FastAPI/NextJS monorepo, implement the lead workflow, and draft the supporting docs. I personally directed the tradeoffs around persistence, authentication scope, email provider integration, upload handling, and what should be production-ready versus intentionally simple for the exercise.

My main review focus was whether the generated implementation matched the real workflow rather than only passing a happy-path demo. I made sure the automatic prospect email is treated as an acknowledgement, not as the `REACHED_OUT` state; that state only changes after an attorney manually follows up. I also reviewed the email path and moved from a local-only outbox fallback to a real SMTP integration using SendGrid-compatible settings.

One place the agent produced subtly bad code was test/config coupling: after adding real SMTP settings, tests started reading my local `.env` and attempted to contact SendGrid. I caught that because tests failed with a network/DNS error instead of exercising app logic. I fixed it by forcing tests into local outbox mode and a test SQLite database, so automated tests remain deterministic while the running app can still use real SMTP credentials.

## Representative Prompt Excerpts

Initial implementation prompt:

> Build an application to support creating, getting and updating leads for an immigration law firm. Use FastAPI, NextJS, storage persistence, email integration, production-like structure, and include run/design/agent usage docs.

Architecture direction prompt:

> Use a small monorepo with a clear backend/frontend split. Keep the public intake endpoint unauthenticated, but guard internal lead listing and state updates behind auth. Use SQLite for the assignment, but write the design doc so Postgres, object storage, migrations, and background jobs are the obvious production upgrade path.

Email workflow prompt:

> The automatic prospect email should be a receipt only. Do not mark the lead `REACHED_OUT` until an attorney manually clicks the action after personally following up. Add real SMTP support, but keep a local outbox fallback so the app can be tested without provider credentials.

Security and privacy review prompt:

> Check the upload path and secrets handling. Resume files should not be committed, `.env` should stay ignored, and the API should validate file type and size. Do not expose server resume paths in public responses.

Agent correction excerpt:

> Tests should not depend on my real SendGrid `.env`. Make tests use a local test database and outbox mode so they stay deterministic while production email remains configurable.

## What Was Delegated

- Monorepo scaffolding and boilerplate.
- FastAPI models, schemas, auth dependency, storage service, email service, and route handlers.
- NextJS public intake form and internal attorney queue UI.
- Initial CSS and responsive layout.
- First drafts of the runbook, design doc, email setup doc, and attribution notes.
- Focused backend tests and build verification commands.

## What Was Hand-Directed

- Choosing SQLite and local file storage as assignment-appropriate defaults, while documenting Postgres and object storage as future replacements.
- Emphasizing that auto-email is not equivalent to attorney outreach, preserving the manual `PENDING` to `REACHED_OUT` workflow.
- Setting up SendGrid account and API key for real delivery, while retaining a truthful local outbox fallback.
- Keeping internal auth intentionally simple using a passward login, but isolated behind FastAPI dependencies so it could be replaced by SSO/OIDC.
- Reviewing generated code for CORS behavior, stale NextJS build issues, upload validation, ignored secrets, and deterministic tests.
