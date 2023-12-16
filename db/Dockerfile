FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=psw123 \
    MYSQL_DATABASE=product_db \
    MYSQL_USER=user \
    MYSQL_PASSWORD=666
COPY ./db/init_db /docker-entrypoint-initdb.d
EXPOSE 3306

CMD ["mysqld", "--default-authentication-plugin=mysql_native_password"]