ThreatPulse — Cyber Threat Intelligence Platform
===============================================

ThreatPulse is a lightweight Cyber-Threat-Intelligence (CTI) aggregation and analysis platform. It
collects feeds (threats, IOCs, CVEs), provides a REST API for automation, and ships a modern React
frontend dashboard for exploration, reporting and incident triage.

Key features
------------
- Aggregates threat feeds and IOC sources (fetch commands available in `threats/management/commands`).
- Browsable CVE catalog with severity badges and exploit indicators.
- Centralized reports: create, list, preview and download PDFs.
- Role-aware API and UI (admin/staff vs regular users).
- JWT authentication with refresh support (DRF + Simple JWT).

Repository layout
-----------------
- `backend/` — Django + Django REST Framework API and background management commands.
- `frontend/` — React + Vite single-page app that consumes the backend API.
- `scripts/` — small helper scripts (E2E smoke checks, utilities).

Quickstart — Backend (development)
---------------------------------
Requirements: Python 3.11+, pip

1. Create a virtualenv and install:

```powershell
cd backend
python -m venv .venv
.venv\\Scripts\\activate    # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

2. By default the API root is `http://127.0.0.1:8000/api/`.

Quickstart — Frontend (development)
----------------------------------
Requirements: Node 18+, npm

```powershell
cd frontend
npm install
npm run dev
```

The frontend expects the backend API under `/api/`. `vite.config.js` contains a development proxy so the
frontend can talk to the backend without CORS changes when both are run locally.

Authentication
--------------
- The backend uses JWT access + refresh tokens (via `rest_framework_simplejwt`).
- The frontend stores tokens via `AuthContext` and uses Axios interceptors to attach the access token
	and transparently refresh when receiving `401` responses.

Testing
-------
- Backend unit tests: from `backend/` run `python manage.py test`.
- Frontend unit tests: from `frontend/` run `npm install` then `npm test` (Jest + Testing Library).
- A lightweight E2E smoke script is available at `scripts/e2e_api_check.py` which exercises register,
	token issuance, report create/list/download and a few read endpoints.

CI
--
A GitHub Actions workflow is included at `.github/workflows/ci.yml` that runs backend tests and frontend
tests on push/PR. Adjust runners or matrix if you need different Node/Python versions.

Environment & configuration
---------------------------
- Backend: configure standard Django settings via `backend/config/settings.py` and environment variables.
- Frontend: Vite accepts `VITE_API_BASE_URL` to override the API base URL; by default the app uses `/api/`.

Troubleshooting
---------------
- If `npm install` fails due to optional dev dependencies (e.g., Tailwind), remove those devDeps from
	`frontend/package.json` or install with `--legacy-peer-deps`:

```powershell
cd frontend
npm install --legacy-peer-deps
```

- `reportlab` is optional for PDF generation. The backend uses lazy import and will fall back if `reportlab`
	is not installed — install it if you need PDF export from the server:

```powershell
cd backend
pip install reportlab
```

Next steps & suggestions
-----------------------
- Add more frontend tests to improve coverage (pages and mocked API flows).
- If you want Tailwind styling, re-add Tailwind devDependencies and run `npx tailwindcss init -p` in
	the `frontend` folder.
- Add an integration/E2E test runner (Cypress) for UI flows if you plan to deploy to production.

Contributing
------------
Open issues, submit PRs, and follow standard GitHub flow. For major changes, open an issue first to
discuss the approach.

License
-------
This project does not include a license file by default. Add a `LICENSE` file to indicate reuse rules.

Files to inspect
----------------
- See `backend/README.md` (if present) and `frontend/README.md` for folder-level notes.

Contact
-------
If you want me to continue, I can: run the E2E script, retry Tailwind integration, or add CI badges.
