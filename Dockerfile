FROM python:3.9.1-buster

ENV REDIS_HOST=""
ENV REDIS_PORT=""
ENV REDIS_DB=""

WORKDIR /app
COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "app:app"]