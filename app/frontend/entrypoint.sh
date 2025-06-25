#!/bin/sh
echo "$API_BASE_URL"
envsubst < /usr/share/nginx/html/config.js.template > /usr/share/nginx/html/config.js
exec nginx -g "daemon off;"