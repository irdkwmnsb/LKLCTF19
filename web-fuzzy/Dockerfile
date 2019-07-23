FROM python:3

WORKDIR /var/fuzzy

COPY . .
# graph.json нужно сгенерировать. python3 gen_graph.pY

RUN python3 -m pip install -r requirements.txt

CMD gunicorn -c gunicorn.conf.py app:app
