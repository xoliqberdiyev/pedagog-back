down:
	docker compose down

up:
	docker compose up -d --build

pull:
	git fetch
	git merge origin/main

logs:
	docker compose logs -f

deploy: pull down up
