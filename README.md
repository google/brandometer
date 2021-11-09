# Brandometer

N.B. This is not an officially supported Google product

For the marketers, Brandometer is a solution to measure brand impact through inexpensive and automated deployment of brand studies not yet offered by existing Google Display products.

To check out the Java implementation, you can check this [branch](https://github.com/google/brandometer/tree/release-v1.0) or this [release](https://github.com/google/brandometer/releases/tag/v1.0)

# Prerequisites

This solution leverages:
* [Google Cloud SDK](https://cloud.google.com/sdk/) (aka gcloud)
* [Python 3.x](https://www.python.org/downloads/)
* [pip](https://bootstrap.pypa.io/get-pip.py)

# Quick start to deployment

1. Create a [Google Cloud project](https://console.cloud.google.com/projectcreate) with billing enabled.
   Take note of the project id.

2. Download source code from [github](https://github.com/google/brandometer) on your workstation. 

```shell
   git clone https://github.com/google/brandometer.git
```
3. Set up project with gcloud

Run command: `gcloud auth login`. It will pop up a new login page to authorize your account

4. After login, set up the project config to your working PROJECT_ID 

```shell
   gcloud config set project $YOUR_PROJECT_ID
```

5. ```./deploy [project-id] [bigquery-location] [compute-region]```

If the deploy fails with an error, wait 5 minutes and try again. Sometimes a new project takes a little while to set up.

## Running the project locally


1. If you don't have virtual environment for this project yet. Create a new one and run the virtual environment. 

[please follow the instruction here](https://docs.python.org/3/tutorial/venv.html)

2. Install project requirements

```shell
   pip install -r creative/app/requirements.txt
```

3. For Windows, use the following command to setup project environment

```set FLASK_APP=path/to/creative/app```

```set FLASK_ENV=development```

then run the project by `flask run`

for MacOS, use the following command to run the project

```python main.py```

the project will be available on http://127.0.0.1:5000

## Running Unit Test

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