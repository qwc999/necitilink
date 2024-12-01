update:
	git pull git@github.com:qwc999/necitilink.git main

push:
	git push git@github.com:qwc999/necitilink.git main

stop:
	sudo docker-compose stop

kill:
	sudo docker-compose kill

down:
	sudo docker-compose down

build:
	sudo docker-compose --env-file .env build

up:
	sudo docker-compose up

logs:
	sudo docker-compose logs --tail=0 --follow

run: stop build up

all: update run