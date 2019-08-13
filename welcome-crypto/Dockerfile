FROM python:3

WORKDIR /app

COPY small_app.py .
COPY requirements.txt .

RUN pip3 install -r requirements.txt

CMD gunicorn -w 4 -b 0.0.0.0:80 small_app:app