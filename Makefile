PYTHON = .venv/bin/python

.PHONY = setup run-dev test lint isort-check isort-write black-check black-write mypy pylint

# Setup environment
setup:
	[ -f .venv/bin/python ] || python3.10 -m venv .venv
	${PYTHON} -m pip install -U --upgrade-strategy eager pip setuptools wheel
	${PYTHON} -m pip install -U --upgrade-strategy eager -e .[dev]

gen-cert:
	openssl req -config ./certs/certificate.conf -new -x509 -nodes -days 100000 -out ./certs/certificate.pem

# Run
run-dev:
	${PYTHON} -m flask run

run:
	$(PYTHON) -m gunicorn -c src/app/gunicorn.conf.py

# Tests
test:
	${PYTHON} -m pytest tests/


# Linting
lint: isort-check black-check mypy pylint

isort-check:
	${PYTHON} -m isort --check-only src/ tests/ setup.py

isort-write:
	${PYTHON} -m isort src/ tests/ setup.py

black-check:
	${PYTHON} -m black --check src/ tests/ setup.py

black-write:
	${PYTHON} -m black src/ tests/ setup.py

mypy:
	${PYTHON} -m mypy -p app

pylint:
	${PYTHON} -m pylint app
	${PYTHON} -m pylint --rcfile=.pylintrc.tests tests
