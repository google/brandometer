# Quick Start Guide

## Prequisite

1. Python 3.x

this project is required to have Python 3.x ready on your machine.

Don't have Python yet? [Download and Install here](https://www.python.org/downloads/)

to check if the installation is successful on your machine, open command line tool and enter:

```python -V```

it should show `Python 3.x.x` which is installed and ready to use

2. Install pip

Have `pip` ready on your machine.

After install Python 3.x, download `get-pip.py` [here](https://bootstrap.pypa.io/get-pip.py) then use the following command:

```python get-pip.py```

the console will show the progress for downloading and install pip to your machine.

you can verify pip installation by `pip --version`, you should be able to see pip version installed on your machine.

## Run the project

1. After cloning this project, open cmd and change directory path to your project

```cd ~/path/to/brandometer```

2. if you doesn't have virtual environment for this project yet. Create a new one and run the virtual environment. 

[please follow the instruction here](https://docs.python.org/3/tutorial/venv.html)

3. install project requirements

```pip install -r creative/app/requirements.txt```

4. setup project with gcloud

run command: `gcloud auth login` it will popup a new login page to authorize your account

after login setup the project config to your working PROJECT_ID 

```gcloud config set project $YOUR_PROJECT_ID```

5. run the project

for Windows, use the following command to setup project environment

```set FLASK_APP=path/to/creative/app```

```set FLASK_ENV=development```

then run the project by `flask run`

for MacOS, use the following command to run the project

```python main.py```

the project will be available on http://127.0.0.1:5000

## Deploy the project

```cd ~/path/to/brandometer```

1. Create a GCP project with billing enabled. Make note of the project id.

2. ```./deploy [project-id] [bigquery-location] [compute-region]```

If the deploy fails with an error, wait 5 minutes and try again. Sometimes a new project takes a little while to set up.

## Run Unit Test

1. login to gcloud with application-default login by command:


```gcloud auth application-default login```

this commandline will help SDK to automatically find the credentials to authenticate with Google Cloud

2. change the working directory to brandometer/creative/app

```cd ~/path/to/brandometer/creative/app```

3. run pytest with the following command

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