FROM python:3

ARG app=group_reputation2

WORKDIR /usr/src/app

RUN pip install -U otree

COPY ./$app .
RUN yes | otree resetdb
RUN otree collectstatic

ENV REDIS_URL 'redis://redis:6379'
ENV OTREE_PRODUCTION 1
CMD [ "otree", "prodserver" ]

# RUN rm db.sqlite3
# CMD [ "otree", "devserver" ]