#!/bin/bash
echo ">>> Bringing down containers"
docker-compose -f docker-compose.prod.yml down -v

echo ">>> Building and running up container services"
docker-compose -f docker-compose.prod.yml up -d --build

echo ">>> Making migrations"
docker-compose -f docker-compose.prod.yml exec web python manage.py makemigrations onlinecourse

echo ">>> Migrating"
docker-compose -f docker-compose.prod.yml exec web python manage.py migrate

echo ">>> Collecting Static"
docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic