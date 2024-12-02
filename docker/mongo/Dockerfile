FROM mongo:6.0

COPY ../scripts/init_mongo.js /docker-entrypoint-initdb.d/

RUN chmod -R 700 /docker-entrypoint-initdb.d/
