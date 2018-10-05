FROM cypress/browsers:chrome69
WORKDIR /root

RUN npm i cypress
COPY ./cypress.json cypress.json

CMD $(npm bin)/cypress run
