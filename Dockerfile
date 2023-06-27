FROM python:3.10-alpine

ARG TOKEN
ARG apikey_binance
ARG secret_binance

ENV TOKEN=$TOKEN
ENV apikey_binance=$apikey_binance
ENV secret_binance=$secret_binance

WORKDIR /app

COPY requirements.txt requirements.txt
COPY main.py main.py

RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "main.py"]