# Gargoyle Render Starter

This repo is packaged so you can push it to GitHub and deploy it as a Render web service.

## Included
- `app.py` - Flask web app with a landing page and demo API
- `templates/index.html` - main website page
- `static/style.css` - site styling
- `static/script.js` - frontend logic for the demo form
- `docs/` - project docs copied from the original package
- `render.yaml` - Render blueprint for a Python web service
- `requirements.txt` - Python dependencies

## Local run
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000`

## API test
```bash
curl -X POST http://127.0.0.1:5000/api/demo       -H "Content-Type: application/json"       -d '{"query":"How should a fintech startup enter a regulatory sandbox?"}'
```

## Deploy on Render
1. Create a new GitHub repo and upload these files.
2. In Render, create a new Web Service from that repo.
3. Render should detect the included `render.yaml`, or you can manually use:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
4. Deploy.
