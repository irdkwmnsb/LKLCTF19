FROM archlinux/base:latest

WORKDIR /web
RUN pacman -Syu python python-pip firefox geckodriver --needed --noconfirm
RUN pip install tornado requests selenium loguru
COPY ./smart_bot.py ./
CMD ["bash", "-c", "echo 'nameserver 8.8.8.8' > /etc/resolv.conf && SERVICE_SMART_BOT_SESSION_ID=dfe5cd552bf72b356a1d5c173405dd94b9f48a4153b522548ee7870ad0eda085 MOZ_HEADLESS=1 python3 smart_bot.py"]
