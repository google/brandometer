Brandometer
=============

N.B. This is not an officially supported Google product

This app provides prototype code to run brand studies on DCM.

See the [Google App Engine standard environment documentation][ae-docs] for more
detailed instructions.

[ae-docs]: https://cloud.google.com/appengine/docs/java/

* [Java 8](http://www.oracle.com/technetwork/java/javase/downloads/index.html)
* [Maven](https://maven.apache.org/download.cgi) (at least 3.5)
* [Google Cloud SDK](https://cloud.google.com/sdk/) (aka gcloud)


# Running locally

    mvn appengine:run

# Brandometer deployment

## Step 1 - Set up Cloud project and auth

    gcloud init

* When prompted to pick cloud project, create a new project.
* Update com.google.cloud.tools/configuration/project in pom.xml

## Step 2 - Set up App Engine project

    gcloud app create

## Step 3 - Deploy receiving server

    mvn appengine:deploy

Make a note of the "target url" value.

## Step 4 - Prepare creative

* Make a copy of the directory: ./sample_creative
* Generate a unique ID for the survey (e.g. using ```uuidgen``` command)
* Update config.js
    * Update the "response_server" variable to include your target_url (from previous step).
    * Set the unique ID on config.js
    * Update questions and options to match your survey needs.

### Note 
This server only has one functional responsibility i.e to log the details of GET requests coming on the path `<your_target_url/measure?param1=value1&param2=value2` on the app engine logs. _(You can view the logs using the StackDriver Log service in GCP.)_ 
The format of the GET request is like : `https://[your_target url]/measure?type=survey&id={survey_id}&seg={seg}&response={responses}&visual={visual_responses}&creative_size={size}&randomtimestamp={random_timestamp}&bomid={bomid}&times={time_measurement}` as mentioned in the /brandometer/sample_creative/config.js file.

Further more,
* This server *DOES NOT* host the creative web files (htmls/js). 
* Hitting any other url path like the `https:<your_target_url>/` will give a 404 as expected. The only path mapped is `/measure` as mentioned above.

## Step 5 - Connect logs to BigQuery

* https://console.cloud.google.com/bigquery and Enable BigQuery
* https://console.cloud.google.com/logs/exports to set up log exports
* Click "Create Export"
* Set time filter to ```No limit```
* Click "Submit Filter"
* Set sink name: ```BQ```
* Set sink service: ```Bigquery```
* Set sink destination: 
  * "Create new BigQuery dataset"
  * Set dataset name: ```appengine_logs```

## Step 6 - Schedule daily data preparation in BigQuery

* Update SQL below to reference your project name and paste into BigQuery query page - https://console.cloud.google.com/bigquery
* Create destination dataset
  * Create "CREATE DATASET"
  * Set dataset ID: ```dailySet```
  * Set default table expiration: ```Never```
  * Click "Create Dataset"
* Paste and run query below to test
* Run query to test
* Click "Schedule Query" and schedule to run daily
  * Dataset name: ```dailySet```
  * Table name: ```dailyResult_{run_time-1h|"%Y%m%d"}```
  * Destination table write preference: "Overwrite table"

```SQL
#standardSQL

SELECT
  timestamp,
  REGEXP_EXTRACT(protoPayload.resource, r"id=([^&]+)") AS id,
  REGEXP_EXTRACT(protoPayload.resource, r"seg=([^&]+)") AS seg,
  SAFE_CAST(REGEXP_EXTRACT(REGEXP_EXTRACT(protoPayload.resource, r'times=([^&]+)'),r'^(d+)%7C') AS INT64) AS render_to_q1_time_ms,
  SAFE_CAST(REGEXP_EXTRACT(REGEXP_EXTRACT(protoPayload.resource, r'times=([^&]+)'),r'^d+%7C(d+)$') AS INT64) AS q1_to_end_time_ms,
  ARRAY_LENGTH(SPLIT(REGEXP_EXTRACT(protoPayload.resource, r'response=([^&]+)'),'%7C')) AS num_questions,
  REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_EXTRACT(protoPayload.resource, r'response=([^&]+)'), r'%3A',':'),'%7C','|') AS response,
  REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_EXTRACT(protoPayload.resource, r'visual=([^&]+)'), r'%3A',':'),'%7C','|') AS visual_response,  
  REGEXP_EXTRACT(protoPayload.resource, r'(?:cid|bomid)=([^&]+)') AS bom_id,
  REGEXP_EXTRACT(protoPayload.line[SAFE_OFFSET(1)].logMessage, r'bomcookie=([^;]+);') AS bom_cookie,
  REGEXP_EXTRACT(protoPayload.resource, r'size=([^&]+)') AS size,
  protoPayload.userAgent AS user_agent,
  REGEXP_EXTRACT(protoPayload.resource, r'response=([^&]+)') AS raw_response,
  protoPayload.requestId AS protoPayload_request_id,
  protoPayload.line[SAFE_OFFSET(0)].logMessage AS log_message,
  protoPayload.line[SAFE_OFFSET(1)].logMessage AS bom_cookie_log_raw,
  protoPayload.resource AS raw_resource
FROM
  `[your-project-id].appengine_logs.appengine_googleapis_com_request_log_*`
WHERE
  _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 1 day))
  AND protoPayload.method = 'GET'
  AND protoPayload.wasLoadingRequest IS NULL
  AND REGEXP_CONTAINS(protoPayload.resource, r'^/measure\?.*')
```

## Step 7 - Report on surveys

Sample query:

```SQL
#standardSQL
WITH
  RawData AS (
  SELECT
    bom_cookie,
    seg,
    response,
    `timestamp`,
    ROW_NUMBER() OVER (PARTITION BY bom_cookie ORDER BY `timestamp`) response_number
  FROM
    `[your-project-id].dailySet.dailyResult_*`
  WHERE
    _TABLE_SUFFIX BETWEEN '20190701' # Update to match your study date
    AND FORMAT_DATE('%Y%m%d', CURRENT_DATE())
    AND id = '[your_unique_study_id]' ),
  CoreData AS (
  SELECT
    bom_cookie,
    seg,
    response,
    `timestamp`
  FROM RawData
  WHERE response_number = 1)
SELECT
  #For compliance, ensure that bom_cookie is not exported in final report.
  FORMAT_TIMESTAMP('%F', `timestamp`) `date`,
  seg,
  SPLIT(SPLIT(response, '|')[SAFE_ORDINAL(1)],':')[SAFE_ORDINAL(2)] AS response1,
  SPLIT(SPLIT(response, '|')[SAFE_ORDINAL(2)],':')[SAFE_ORDINAL(2)] AS response2
FROM
  CoreData
```

# Notes and checklists

## config.js

* Make sure you have the questions reviewed by the customer and they are in-line with the industry brand lift study. Generic questions will not yield good lift. Our recommendation would be to use the questions available on Youtube BLS. 
* Question Type: 
    * Single Option: Out the of the options, the user can choose only 1 option and the options will be randomized. 
    * Multiple Option: Users can choose multiple options and the options will be randomised. 
    * Ordered: Users can choose 1 option but the options will be ordered.  
* Itis  recommended to keep Option A as the correct answer. This helps during reporting and analysis at the end of the campaign.  
* If you have “None of the above” as the last option, switch isNone to True
* Next is critical because based on the option the user chooses, it will show the next question. Ex. If the user chooses option B, you can skip question 2 and move to 3. 
* To end the survey after a response, use end (this is case sensitive and you will need to use ‘end’, it will not capture responses if you have upper case)

## BLS Setup

* Ensure that you have edit/creative trafficking access for the specific advertiser in DCM 
* Check what the targeting will be in terms of Demographics and provide the same to Anant(for eg: Male 18-44). This is important as this impacts the no. of placements in the setup.
* Check the Nomenclature(Campaign,Placement if any), Site ID to be followed/assigned for the campaign(Naming can be edited later as well)

* DCM Setup
* Create/Edit the campaign in DCM within the Advertiser
* Create Brandometer Audiences within the campaign with Control(wt:1) and Expose(wt:7) Segments
* Create a single placement within the Campaign with the naming convention containing the Gender and Age Along with the remaining otherwise specified nomenclature
* Copy the placement and create as many copies as the number of placements required
* Change Nomenclature accordingly
* Upload all the survey creatives/default creative via Batch upload 
* Upload the Doubleclick logo creative or PSA creative 
* Default Ad should be assigned to all placements
* Create a Master Ad containing the client creative and assign it to all the placements 
* Create a Control Ad and assign it to all the placements with following details
    * Priority:9 
    * Assign the Doubleclick / PSA creative
    * Assign Audience Segment: Control
* Create a Pre-Survey Ad and assign to all placements
    * Assign priority 9
    * Assign Frequency Cap: 3 in 90 days (or length of campaign flight)
    * Assign the client creative
    * Assign Audience segment: Expose
* Create a Control Survey Ad based on nomenclature and assign the respective Control Survey creative to each Ad- replicate it for each placement according to nomenclature 
    * Assign Priority 9
    * Assign Appropriate Survey Creative
    * Assign Audience Segment: Control
* Create an Expose Survey based on nomenclature and assign the respective Expose Survey creative to each Ad- replicate it for each placement according to nomenclature
    * Assign Priority: 10
    * Assign Appropriate survey creative
