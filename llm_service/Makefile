install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

# test:
# 	python -m pytest -vv --cov=ocrlogic --cov=api tests/*.py

format:
	isort --profile=black . &&\
		black --line-length 88 .

lint:
	pylint --disable=R,C *.py llmlogic/*.py

# install_models:
# 	sudo apt-get update &&\
# 		sudo apt-get install -y tesseract-ocr libtesseract-dev tesseract-ocr-spa
