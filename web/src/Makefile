run:
	gunicorn -k gevent -b 0.0.0.0:8000 main:app --reload --worker-connections 1000

runc:
	gunicorn --reload -c gunicorn_config.py main:app

dotest:
	python tests/app_tests.py

kill:
	pkill gunicorn