requirements:
	poetry export -f requirements.txt -o requirements.txt

devserver:
	python app/manage.py runserver 0.0.0.0:8000

migrations:
	python app/manage.py makemigrations

migrate:
	python app/manage.py migrate
