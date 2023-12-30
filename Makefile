build-wheel:
	python setup.py bdist_wheel

lint:
	pylint --rcfile=.pylintrc MelodieFuncFlow

test:
	pytest -s

test-cov:
	pytest -s --cov-report=term-missing \
		--cov=MelodieFuncFlow

format:
	black .