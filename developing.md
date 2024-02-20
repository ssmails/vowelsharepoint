#### Developing
```
Creates a virtual env, and install dev dependencies
make init-py-env

Activate virtual environment with dependencies
source env/bin/activate

Add code to main.py to test
cd vowelsharepoint/vowelsharepoint

Ensure .env file is set appropriately (For Env variables to be set check - examples/.sample-env)
python3 main.py
```

#### To run tests/ examples/ , either of the below must be done.
```
1. Package installed from pip (TODO).
2. Package installed via the github link.
pip install git+https://wwwin-github.cisco.com/vowel-it/vowelsharepoint.git
```


#### Building and Testing the package before publish (via source distribution)
##### Todo use poetry instead to package ?
```
Ensure your in project root /Users/sushroff/Documents/vowel-it/vowelsharepoint
sushroff@SUSHROFF-M-7MJQ vowelsharepoint % python3 -m venv env     
sushroff@SUSHROFF-M-7MJQ vowelsharepoint % source env/bin/activate 

(env) sushroff@SUSHROFF-M-7MJQ vowelsharepoint % python3 setup.py sdist  

Check packages available 
(env) sushroff@SUSHROFF-M-7MJQ vowelsharepoint % python -c "from setuptools import setup, find_packages; print(find_packages())"
['vowelsharepoint']

Below command will install the package in your virtual environment.
(env) sushroff@SUSHROFF-M-7MJQ vowelsharepoint % pip3 install dist/vowelsharepoint-0.0.1.tar.gz

Test examples
Ensure .env file is set appropriately (For Env variables to be set check - examples/.sample-env)
(env) sushroff@SUSHROFF-M-7MJQ vowelsharepoint % cd examples 
(env) sushroff@SUSHROFF-M-7MJQ examples % python3 rag_inference.py

```

#### References
https://www.madebymikal.com/all-python-packages-require-a-pyproject-toml-with-modern-pip/
https://snarky.ca/what-the-heck-is-pyproject-toml/

