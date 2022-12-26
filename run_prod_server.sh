#!/bin/bash
echo -e "\n>>> Bringing down containers"
docker compose -f docker-compose.prod.yml down -v

echo -e "\n>>> Building and running up container services"
docker compose -f docker-compose.prod.yml up -d --build

sleep 5
echo -e "\n>>> Making migrations"
docker compose -f docker-compose.prod.yml exec web python manage.py makemigrations onlinecourse

echo -e "\n>>> Migrating"
docker compose -f docker-compose.prod.yml exec web python manage.py migrate

echo -e "\n>>> Collecting Static"
docker compose -f docker-compose.prod.yml exec web python manage.py collectstatic

echo -e "\n>>> Creating Superuser"
docker compose -f docker-compose.prod.yml exec web python manage.py createsuperuser --noinput

sleep 2
echo -e "\n>>> Checking Certbot"
docker compose -f docker-compose.prod.yml run certbot certonly --webroot --webroot-path /var/www/certbot -d practice2deploy4amar.com -d www.practice2deploy4amar.com --dry-run -v

sleep 5
echo -e "\n>>> Getting certificates"
docker compose -f docker-compose.prod.yml run certbot certonly --webroot --webroot-path /var/www/certbot -d practice2deploy4amar.com -d www.practice2deploy4amar.com -v

sleep 5
echo -e "\n>>> Configuring NGINX to serve certificate"
rm nginx/conf/nginx.initial.conf
rsync nginx.final.conf nginx/conf/

echo -e "\n>>> Restarting Server containers/services"
docker compose -f docker-compose.prod.yml restart

# schedule a cron job to renew certs
# docker compose -f docker-compose.prod.yml run certbot renew
