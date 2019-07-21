FROM archlinux/base:latest

WORKDIR /web
RUN pacman -Syu python python-pip firefox geckodriver --needed --noconfirm
COPY ./smart_bot.py ./
COPY ./web-ebanking/ ./web-ebanking
RUN pip install -r ./web-ebanking/requirements.txt
CMD ["bash", "-c", "echo 'nameserver 8.8.8.8' > /etc/resolv.conf && cd web-ebanking && python3 SETUP_DB.py && exec bash start.sh"]
