venv:
	rm -rf venv
	python3 -m venv venv
	./venv/bin/pip install -U pip
	./venv/bin/pip install -U -r requirements.txt

test: venv
	./venv/bin/pytest tests --junitxml=report.xml

coverage: venv
	./venv/bin/pytest --verbose --cov-report term --cov-report xml --cov=chomp tests

black: venv
	./venv/bin/black chomp tests

clean:
	rm -rf venv

build: venv
	./venv/bin/python -m build

install:
	pip uninstall -y chomp
	pip install dist/chomp-$$(grep version pyproject.toml | cut -f2 -d\")-py3-none-any.whl

build_and_install: build install

upload:
	twine upload dist/*
