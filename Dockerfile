FROM python:3

RUN pip install -U otree psycopg2-binary

WORKDIR /usr/src/app
ARG APP
COPY ./$APP .

RUN yes | otree resetdb && rm db.sqlite3

CMD sh -c ' \
    if [ "$ENV" = "development" ]; then     otree devserver 0.0.0.0:8000; \
    elif [ "$ENV" = "staging" ]; then       otree test $TEST_NAME $TEST_USERS; \
    else                                    otree prodserver; \
    fi'