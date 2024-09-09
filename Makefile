gen-reqs:
	@pip freeze > ./requirements.txt

py:
	@python automacao_mkt_chat.py

up:
	@docker compose up -d

down:
	@docker compose down

reload: down up

exec:
	@docker compose exec -it automacao_mkt ash

exec-root:
	@docker compose exec -it --user root automacao_mkt ash