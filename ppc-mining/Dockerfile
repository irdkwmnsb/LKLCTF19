FROM python:3
WORKDIR /ppc
COPY service.py service.py
COPY generate_expression.py generate_expression.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD python3 service.py 9999
