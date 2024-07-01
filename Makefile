install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv --cov=ocrlogic tests/*.py

format:
	isort --profile=black . &&\
		black --line-length 88 .

lint:
	pylint --disable=R,C *.py ocrlogic/*.py utils/*.py tests/*.py

models_install:
	sudo apt-get update &&\
		sudo apt-get install -y tesseract-ocr libtesseract-dev tesseract-ocr-spa
