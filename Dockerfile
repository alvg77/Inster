FROM python:3.8

WORKDIR /app
COPY . .

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV SECRET_KEY="uwpwJprR9NhNN8OWg9rLTl6JLt2gnA"
ENV MAIL_USERNAME="ttttest835@gmail.com"
ENV MAIL_PASSWORD="AcihwbU3NWEsUQk"

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
