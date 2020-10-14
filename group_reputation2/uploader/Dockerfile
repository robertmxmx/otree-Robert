FROM node:alpine

WORKDIR /usr/src/app

COPY ./package*.json ./
RUN npm install

COPY . .

ARG UPLOADER_SECRET
ENV UPLOADER_SECRET ${UPLOADER_SECRET}}

# RUN npm run build
# CMD [ "npm", "run", "start" ]

CMD [ "npm", "run", "dev" ]