build-wheel:
	python setup.py bdist_wheel

lint:
	pylint --rcfile=.pylintrc MelodieFuncFlow

test:
	pytest -s

test-cov:
	pytest -s --cov

format:
	black .