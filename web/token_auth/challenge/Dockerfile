FROM alpine:3.19.1

RUN apk add --update nodejs npm mysql mysql-client && \
    rm -rf /var/cache/apk/*

WORKDIR /app

COPY . .

RUN npm install

# install and configure mysql
COPY init.sql /docker-entrypoint-initdb.d/

RUN mkdir -p /run/mysqld && \
	chown -R mysql:mysql /run/mysqld && \
	mysql_install_db --user=mysql --datadir=/var/lib/mysql


EXPOSE 3000

ENV JWT_SECRET=bc344cdc3385f34112400b4476ce103b1bbf4349cde930293c68e5afc58789eb \ 
	FLAG=BtSCTF{W4tch_0ut,pr0t0typ3_15_th3r3!}

CMD ["sh", "-c", "mysqld --skip-performance-schema --user=mysql --console & while ! mysqladmin ping -h localhost --silent; do sleep 1; done && mysql -u root < /docker-entrypoint-initdb.d/init.sql && npm run prod"]
