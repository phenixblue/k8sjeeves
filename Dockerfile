FROM python:3.8-slim

LABEL maintainer=joe@twr.io

COPY ./requirements.txt /app/

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./app.py /app/

CMD ["flask", "run", "--host=0.0.0.0"]