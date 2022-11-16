FROM python:3.8

RUN apt-get update
RUN apt-get install -y python-pip python-dev build-essential

WORKDIR /app

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000

COPY . .

CMD [ "flask", "run"]
