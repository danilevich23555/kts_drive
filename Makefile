install:
	pip install -r requirements.txt --upgrade

migrate.up:
	alembic upgrade head

migrate.down:
	alembic downgrade -1





