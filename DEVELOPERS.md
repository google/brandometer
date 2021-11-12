# Brandometer Developer Guide

This contains the guide for developers for setup and development.

# Prerequisites

This solution leverages:
* [Google Cloud SDK](https://cloud.google.com/sdk/) (aka gcloud)
* [Python 3.x](https://www.python.org/downloads/)
* [pip](https://bootstrap.pypa.io/get-pip.py)

# Running the project locally

1. Download source code from [github](https://github.com/google/brandometer) on your workstation.

```shell
   git clone https://github.com/google/brandometer.git
```

2. If you don't have virtual environment for this project yet. Create a new one and run the virtual environment.

[please follow the instruction here](https://docs.python.org/3/tutorial/venv.html)

3. Install project requirements

```shell
   pip install -r creative/app/requirements.txt
```

4. For Windows, use the following command to setup project environment

```set FLASK_APP=path/to/creative/app```

```set FLASK_ENV=development```

then run the project by `flask run`

for MacOS, use the following command to run the project

```python main.py```

the project will be available on http://127.0.0.1:5000

# Running Unit Test

1. Log in to gcloud with application-default login by command:

```gcloud auth application-default login```

This command will help SDK to automatically find the credentials to authenticate with Google Cloud

2. Change the working directory to brandometer/creative/app

```cd ~/path/to/brandometer/creative/app```

3. Run pytest with the following command

```PYTHONPATH=. pytest```

pytest will scan files in the project that has prefix with `test_` (for example, `test_foo_bar.py`) and run the existing unit test inside

example output (all test passed)

```
===================== test session starts =============================
platform darwin -- Python 3.8.2, pytest-6.2.3, py-1.10.0, pluggy-0.13.1
rootdir: /Users/xxx/gground/brandometer/creative/app
collected 5 items

test/test_survey_service.py .....                                [100%]

========================== 5 passed in 1.52s ===========================
```

More information about pytest [here](https://docs.pytest.org/en/6.2.x/index.html)