FROM node:10.4.1-alpine

WORKDIR  /usr/src/app

ENV PATH /usr/src/app/node_modules/.bin:$PATH

COPY package.json /usr/src/app/package.json

RUN npm install --no-cache
RUN npm install react-scripts@1.1.4 -g

CMD ["npm", "start"]