install:
	cd ocr_service &&\
		make install &&\
		cd .. &&\
	cd llm_service &&\
		make install

test:
	cd ocr_service &&\
		make test

format:
	cd ocr_service &&\
		make format &&\
		cd .. &&\
	cd llm_service &&\
		make format

lint:
	cd ocr_service &&\
		make lint &&\
		cd .. &&\
	cd llm_service &&\
		make lint

reformat: format lint

install_models:
	cd ocr_service &&\
		make install_models
