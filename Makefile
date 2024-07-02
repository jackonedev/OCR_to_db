install:
	cd ocr_service &&\
		make install

test:
	cd ocr_service &&\
		make test

format:
	cd ocr_service &&\
		make format

lint:
	cd ocr_service &&\
		make lint

install_models:
	cd ocr_service &&\
		make install_models
