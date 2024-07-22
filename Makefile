wheel:
	python setup.py bdist_wheel --version 0.0.1

libs:
	pip install -r requirements.txt

remove:
	pip uninstall -y loguru-cli

dev-install:
	pip install -e .