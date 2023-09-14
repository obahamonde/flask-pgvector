FROM postgres:latest

ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD postgres
ENV POSTGRES_DB postgres


RUN apt-get update && apt-get install -y \
	build-essential \
	postgresql-server-dev-all \
	git \
	&& rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/pgvector/pgvector.git

RUN cd pgvector && make install

RUN echo "shared_preload_libraries = 'pgvector'" >> /usr/share/postgresql/postgresql.conf.sample



