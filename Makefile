build-wheel:
	python setup.py bdist_wheel

lint:
	pylint --rcfile=.pylintrc ModuleTemplate

test:
	pytest -s

test-cov:
	pytest -s --cov

format:
	black .