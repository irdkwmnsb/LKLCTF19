FROM python:3

WORKDIR /var/fuzzy

COPY flag.txt .
COPY app.py .
COPY templates .
# graph.json нужно сгенерировать. python3 gen_graph.py
COPY graph.json .
COPY gunicorn.conf.py .
COPY fish_text_api.py .
COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

CMD gunicorn -c gunicorn.conf.py app:app
