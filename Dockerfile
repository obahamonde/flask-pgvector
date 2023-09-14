FROM python:3.10

ENV PYTHONDONWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SQLALCHEMY_DATABASE_URI postgresql+psycopg2://postgres:postgres@db:5432/postgres
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

EXPOSE 5500

COPY . /app

CMD ["gunicorn", "--bind", "0.0.0.0:5500", "app:app","--reload"]