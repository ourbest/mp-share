FROM python:3

RUN apt-get update && apt-get install -y vim

RUN mkdir -p /code/
WORKDIR /code/
ADD requirements.txt .

RUN pip install -r requirements.txt

ADD . .

ENTRYPOINT ["sh", "entry.sh"]