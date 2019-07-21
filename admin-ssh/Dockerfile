FROM archlinux/base:latest
WORKDIR /admin
RUN pacman -Syu gcc ninja meson cmake openssl wget zlib tar --needed --noconfirm
COPY server/ .
RUN bash get-libssh.sh
RUN meson --wipe build && ninja -C build
CMD build/main
