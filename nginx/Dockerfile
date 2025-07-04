FROM nginx:alpine

RUN mkdir -p /etc/nginx/certs

COPY cert.pem /etc/nginx/certs/cert.pem
COPY key.pem /etc/nginx/certs/key.pem
COPY nginx.conf /etc/nginx/conf.d/default.conf
