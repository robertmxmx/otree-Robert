FROM python:3.7

RUN pip install -U otree psycopg2-binary

WORKDIR /usr/src/app
COPY . .

RUN yes | otree resetdb && rm db.sqlite3

CMD sh -c 'yes | otree resetdb && otree prodserver'
# CMD [ "otree", "test", "gr" ]