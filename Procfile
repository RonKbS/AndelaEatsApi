web: gunicorn --workers=5 --threads=5 --timeout 360 run:app
release: python run.py db upgrade
