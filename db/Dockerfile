FROM postgres:16

WORKDIR /app

USER root

RUN mkdir -p /oracle/pg_data/archive/

RUN chown -R postgres:postgres /oracle/

RUN apt-get update
RUN apt-get install -y openssh-server sed
RUN mkdir /var/run/sshd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

COPY init.sh /docker-entrypoint-initdb.d/
COPY ./pg_hba.conf /etc/postgresql/pg_hba.conf
COPY ./postgresql.conf /etc/postgresql/postgresql.conf

CMD ["./entrypoint.sh"]



