FROM php

WORKDIR /web/for-hijacking

COPY ./index.php .
COPY ./sessions.xml .

EXPOSE 80
CMD ["php", "-S", "0.0.0.0:80"]
