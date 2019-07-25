FROM python:3

COPY small_app.py /app/
COPY requirements.txt /app/

workdir /app

RUN pip3 install -r requirements.txt

CMD gunicorn -w 4 -b 0.0.0.0:80 small_app:app