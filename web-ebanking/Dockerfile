FROM python:3

WORKDIR /web
COPY ./web-ebanking/ ./web-ebanking
COPY ./smart_bot/smart_bot.py .
RUN pip install -r ./web-ebanking/requirements.txt
CMD ["bash", "-c", "cd web-ebanking && python3 SETUP_DB.py && exec bash start.sh"]
