setup: requirements.txt
	pip install -r requirements.txt

build:
	python CpmCalculationService.py
run:
	python CpmCalculationService.py
test:
	pytest
clean:
	rm -rf __pycache__
