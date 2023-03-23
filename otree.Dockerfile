# This Dockerfile assumes that the build context is already in the correct app.
# For example, if group_reputation3 is the targeted app then we assume we are
# inside the group_repuration3/ folder

FROM python:alpine

RUN pip install -U otree psycopg2-binary requests
RUN pip uninstall -y uvicorn
RUN pip install uvicorn[standard]

WORKDIR /app

COPY . .

EXPOSE 8000
RUN yes | otree resetdb && rm db.sqlite3

CMD [ "otree", "prodserver" ]
