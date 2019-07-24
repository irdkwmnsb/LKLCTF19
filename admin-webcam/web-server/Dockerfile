FROM ubuntu:18.04

RUN apt update && apt install lighttpd -y

ENTRYPOINT ["lighttpd", "-D", "-f", "/etc/lighttpd/lighttpd.conf"]