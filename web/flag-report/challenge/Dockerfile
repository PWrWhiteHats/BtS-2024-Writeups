FROM python:alpine3.19

WORKDIR /app
COPY . /app

RUN apk add chromium chromium-chromedriver
RUN pip3 install -r requirements.txt

EXPOSE 5000

RUN flask init-db

CMD ["./run.sh"]
