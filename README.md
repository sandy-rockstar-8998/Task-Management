This is a Django project for employee and task management. It uses Django templates and a backend database.

## Fixes applied
- Corrected the app URL routing in `TaskApp/urls.py` so the root URL `/` now resolves to the homepage (`HOME`).
- Removed the duplicate root path mapping that previously caused route conflicts.
- Added a dedicated employee list path at `/employee-list/`.

## Deployment notes
- This repository is a Django app and cannot be hosted directly on GitHub Pages.
- To make this project live, deploy it to a Python/Django host such as Render, Railway, or PythonAnywhere.

## Example links
- GitHub repo URL: `https://github.com/<username>/<repo-name>`
- GitHub Pages static landing page (if enabled): `https://<username>.github.io/<repo-name>/`
- Recommended Django host: `https://<app-name>.onrender.com`
