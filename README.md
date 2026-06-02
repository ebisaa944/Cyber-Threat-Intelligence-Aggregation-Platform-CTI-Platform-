ThreatPulse
============

Local development and test instructions for the ThreatPulse project.

Backend (Django)
-----------------

Requirements: Python 3.11+, pipenv/venv

Create virtualenv and install:

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 8000
```

Run backend tests:

```bash
cd backend
python manage.py test
```

Frontend (React + Vite)
-----------------------

Requirements: Node 18+, npm

```bash
cd frontend
npm install
npm run dev
```

Notes
-----
- The frontend expects the backend API under `/api/` (Vite dev server proxy is configured in `vite.config.js`).
- If you want to use Tailwind, install `tailwindcss`, `postcss`, and `autoprefixer` in the `frontend` folder and run `npx tailwindcss init -p`.

Testing & CI
------------

Frontend tests use Jest + Testing Library. To run them locally:

```bash
cd frontend
npm install
npm test
```

A GitHub Actions workflow is included at `.github/workflows/ci.yml` which runs backend tests and frontend tests on push and pull requests.
# Cyber-Threat-Intelligence-Aggregation-Platform-CTI-Platform-
