FROM php

WORKDIR /web/ppc-database

COPY ./index.php .
COPY ./dump.rdb .

EXPOSE 80
CMD ["php", "-S", "0.0.0.0:80"]
