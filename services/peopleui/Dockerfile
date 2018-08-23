FROM node

ENV NPM_CONFIG_LOGLEVEL warn
ARG app_env
ENV APP_ENV ${app_env}

COPY . ./app
WORKDIR /app


RUN npm install
RUN npm install --save bootstrap

CMD if [ $[APP_ENV] = production]; \
    then \
    npm install -g http-server && \
    npm run build && \
    hs -p 3000; \
    else \
    npm run start; \
    fi

EXPOSE 3000