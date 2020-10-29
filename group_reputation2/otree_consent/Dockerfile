FROM python:3.7

COPY requirements*.txt /
RUN pip install -r /requirements.txt && \
    rm /requirements*.txt

WORKDIR /usr/src/app
COPY . .

CMD sh -c 'yes | otree resetdb && otree prodserver 0.0.0.0:8001'