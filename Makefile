conda-reqs:
	@conda list -e > ./requirements.txt

conda-install:
	@conda install --file ./requirements.txt

py:
	@python automacao_mkt_chat.py

up:
	@docker compose up -d

down:
	@docker compose down

reload: down up

exec:
	@docker compose exec -it jupyter bash

exec-root:
	@docker compose exec -it --user root automacao_mkt bash