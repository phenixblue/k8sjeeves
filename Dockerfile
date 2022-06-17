FROM python:3-alpine

LABEL maintainer=joe@twr.io

COPY ./requirements.txt /app/

WORKDIR /app

RUN apk add --update --no-cache bind-tools ca-certificates

RUN pip install -r requirements.txt

COPY ./app.py /app/

CMD ["flask", "run"]