FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev git wget curl

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install pipenv
RUN export LC_ALL=C.UTF-8; export LANG=C.UTF-8; pipenv install -r requirements.txt

COPY . /app

EXPOSE 8070

CMD [ "./run.sh" ]