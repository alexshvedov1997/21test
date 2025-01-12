FROM python:3.10.9

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN  pip install --no-cache-dir --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt


COPY ./src /app/

ADD ./src/start.sh /
RUN chmod +x /start.sh
