FROM python:3

RUN "apt update"
RUN "python3 -m pip install -r requirements.txt"

CMD "gunicorn -c gunicorn.conf.py app:app"
