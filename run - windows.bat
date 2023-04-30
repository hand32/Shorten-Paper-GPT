@echo off
docker-compose build shorten_paper
docker-compose run --rm shorten_paper
pause