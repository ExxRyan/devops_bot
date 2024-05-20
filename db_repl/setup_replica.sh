rm -rf /var/lib/postgresql/data/*

until PGPASSWORD=${DB_REPL_PASSWORD:-repl_password} pg_basebackup -R -h ${DB_HOST:-postgres_master} -U ${DB_REPL_USER:-repl_user} -D /var/lib/postgresql/data -P
do
    echo 'Waiting for primary to connect...'
    sleep 1s
done

echo 'Backup done, starting replica...'
chmod 0700 /var/lib/postgresql/data
postgres