FROM node:20-alpine3.17 as build

WORKDIR /app

COPY ./package.json .

RUN npm install

RUN npm install react-router-dom

COPY . .

EXPOSE 3000

CMD [ "npm", "start" ]
