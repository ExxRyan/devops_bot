FROM postgres:16

USER postgres

RUN rm -rf /var/lib/postgresql/data/*

WORKDIR /var/lib/postgresql

COPY setup_replica.sh .

USER root

RUN chmod u+x setup_replica.sh

RUN chown postgres:postgres setup_replica.sh

USER postgres

CMD ["./setup_replica.sh"]