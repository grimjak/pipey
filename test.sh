#!/bin/bash

fails=""

inspect() {
    if [ $1 -ne 0 ]; then
        fails="${fails} $2"
    fi
}

# run unit and integration tests
docker-compose -f docker-compose.yml up -d --build
docker-compose -f docker-compose.yml run api python manage.py test
inspect $? users
docker-compose -f docker-compose.yml run api flake8 project
inspect $? users-lint
docker-compose -f docker-compose.yml run client npm test -- --coverage
inspect $? client
docker-compose -f docker-compose.yml down
# run e2e tests, switch to use prod setup
docker-compose -f docker-compose-prod.yml up -d --build
docker-compose -f docker-compose-prod.yml run api python manage.py seed-db
docker-compose -f docker-compose-prod.yml -f ./cypress/docker-compose-prod.yml run cypress node_modules/.bin/cypress run --config baseUrl=http://nginx
#./node_modules/.bin/cypress run --config baseUrl=http://localhost
inspect $? e2e
docker-compose -f docker-compose-prod.yml down


# return proper code
if [ -n "${fails}" ]; then
    echo "Tests failed: ${fails}"
    exit 1
else
    echo "Tests passed!"
    exit 0
fi
