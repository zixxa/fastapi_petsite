up:
	docker compose -f docker-compose-local.yaml up -d

down:
	docker compose -f docker-compose-local.yaml down && docker network prune --force
migrate:
	cd src && alembic revision --autogenerate -m "commit" && alembic upgrade heads
