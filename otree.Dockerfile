# This Dockerfile assumes that the build context is already in the correct app.
# For example, if group_reputation3 is the targeted app then we assume we are
# inside the group_repuration3/ folder

FROM python:3.12-alpine

RUN pip install -U otree psycopg2-binary requests

# Install the minimal uvicorn package. The normal one has issues with serving
# the site.
RUN pip uninstall -y uvicorn
RUN pip install uvicorn[standard]

WORKDIR /app

COPY . .

EXPOSE 8000
RUN yes | otree resetdb && rm db.sqlite3

CMD [ "otree", "prodserver" ]
