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

# Survey Creation

1. Open Brandometer project and click on "Create survey"
2. Input details then submit
3. In the home page, download the zip file which will have 2 HTML5 creatives “Control & Expose” for Brand lift surveys and only one creative for Brand track surveys (only survey no lift)
4. Use both the creatives to run a Brand lift survey or only one of the two creatives to run a Brandtrack survey on Display only inventory through DV360.

# Campaign Manager setup

1. Create a new campaign in DCM within the Advertiser (No other channel should be part of this)
2. Create Brandometer Audiences within the campaign with Control(wt:1) and Expose(wt:7) Segments (See Below)
   a. Navigation: Campaign -> Property -> Audience segmentation
3. Create a placement within the Campaign with the naming convention containing the dimensions. NOTE: Brand-O-Meter setup will happen for 300x250 dimension.
4. Upload all the survey creatives/default creatives
5. Default Ad should be assigned to all placements (Use brand neutral creative[Its a creative that does not have any brand related comms/logos/names etc] for default ads 
6. Create a Control Survey Ad and assign it to 300x250 placement with following details
   a. Priority:9
   b. Assign the Control survey creative
   c. Assign Audience Segment: Control
   d. Frequency: 2/3
7. Create a Pre-Survey Ad and assign to all placements
   a. Assign priority 9
   b. Assign Frequency Cap: 2/3
   c. Assign the 300x250 brand creative
   d. Assign Audience segment: Expose
8. Create an Expose Survey based on nomenclature and assign the respective Expose Survey creative.
   a. Assign Priority: 10
   b. Assign Expose survey creative
   c. Assign Audience Segment: Expose
   d. Frequency: 2/3
9. Create a Master ad for both placements that will have DCO creative assigned to it.
   a. Assign Priority: 15
   b. Assign brand creative
   c. No Audience segment.
   d. No Fcap

## Summary:
1. Backup images can be any jpg brand creatives for respective dimensions.
2. No of placements: 1
3. No of ads for 300x250: 5
4. Each Brandometer placement will have : Default, pre-survey(expose audience), Expose survey, control survey, Master ads.

*300x250 Dimension*
| Ad type | Creative type | Audience | Frequency | Priority |
| --- | --- | --- | --- | --- |
| Defaultt Ad | Brand neutral | - | - | - |
| Control Ad | Control survey | Control | >2 | 9 |
| Pre-Survey Ad | Brand creative | Expose | >2 | 9 |
| Expose Survey Ad | Expose survey | Expose | >2 | 10 |
| Master Ad | Brand creative | - | - | 15 |

# DV360 setup
1. Assign the creatives synced from CM to respective LI items.
2. Each BOM cut/creative will have to be assigned in a separate LI. i.e. If you have Male & Female cuts then you will have 2 placements in CM and respective 2 Line items in DV360.

# Reporting
Use [this template](https://docs.google.com/spreadsheets/d/1h9sQois-mw2wYeddQ3khKwPp8LlGTTVBDP9tZmUpQpQ) to add responses & generate lift
Sample report [here](https://docs.google.com/spreadsheets/d/17Q6zvQMd7sxDd6xd74rducntfd0p3oKG9y5lzpjInks).

# FAQ
1. Can we have multiple questions?
Yes
2. Should we use “Brand name “ as option “A” & option B onwards competitor names?
Yes.
3. Can we run multiple cuts like male female separately to check the lift?
Yes, please setup multiple surveys to do so. Each cut will have a separate placement with 5 ads in CM for Brand lift study & respective Line items in DV360.

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