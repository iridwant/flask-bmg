FROM python:3.8.10

WORKDIR /api

COPY . /api

RUN apt-get update && apt-get install -y python3-dev libpq-dev

RUN pip3 install -r requirements.txt

CMD [ "flask", "run", "--host", "0.0.0.0"]