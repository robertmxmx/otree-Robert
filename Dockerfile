FROM python:alpine

RUN pip install -U otree psycopg2-binary requests
RUN pip uninstall -y uvicorn
RUN pip install uvicorn[standard]

WORKDIR /app

# ARG injection does not work with Elastic Beanstalk so this needs to be
# changed depending on what app is to be deployed
ARG APP=group_reputation3

COPY ./$APP .

EXPOSE 8000
RUN yes | otree resetdb && rm db.sqlite3

CMD [ "otree", "prodserver" ]
