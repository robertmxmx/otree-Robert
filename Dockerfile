FROM python:3

RUN pip install -U otree

WORKDIR /usr/src/app
ARG APP
COPY ./$APP .

RUN yes | otree resetdb && rm db.sqlite3
CMD [ "otree", "devserver", "0.0.0.0:8000"]