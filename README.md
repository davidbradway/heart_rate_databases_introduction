# Mongo Test

## Setup

```bash
virtualenv -p python3 env
source env/bin/activate
pip install -r requirements.txt

FLASK_APP=app.py flask run

# Deploy
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app

```
