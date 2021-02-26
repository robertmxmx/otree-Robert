FROM python:3.7

COPY requirements*.txt /
RUN pip install -r /requirements.txt && \
    rm /requirements*.txt

WORKDIR /usr/src/app
COPY . .

# RUN yes | otree resetdb && rm db.sqlite3
# CMD [ "otree", "test", "gr" ]

# CMD [ "otree", "devserver", "0.0.0.0:8000" ]

CMD sh -c 'yes | otree resetdb && otree prodserver 0.0.0.0:8000'