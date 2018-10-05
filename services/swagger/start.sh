#!/bin/bash
echo "running nginx"

if [ $URL != "**None**" ]; then
    sed -i -e 's@https://petstore.swagger.io/v2/swagger.json@'"$URL"'@g' /usr/share/nginx/html/index.html
fi
echo "running nginx"
exec nginx -g 'daemon off;'