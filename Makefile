down:
	docker compose down

up:
	docker compose up -d --build

pull:
	git fetch
	git merge origin/main

deploy: pull down up
