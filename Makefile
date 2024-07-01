install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest

format:
	isort --profile=black . &&\
		black --line-length 88 *.py

lint:
	pylint --disable=R,C *.py
