init-py-env:
	rm -rf env
	python3 -m venv env && \
		source env/bin/activate && \
		python3 -m pip install --upgrade pip && \
		python3 -m pip install -r vowelsharepoint/requirements.txt
