up:
	docker-compose up

down:
	docker-compose down

build:
	docker-compose up --build

migrate:
	docker-compose exec web python manage.py migrate

test:
	docker-compose -f docker-compose-test.yml up --build --abort-on-container-exit





