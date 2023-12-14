FROM postgres
ENV POSTGRES_DB sqlytes-inventory-app
ENV POSTGRES_USER docker_admin
ENV POSTGRES_PASSWORD postgresadmin
COPY Backend/sql_data/ /docker-entrypoint-initdb.d/
