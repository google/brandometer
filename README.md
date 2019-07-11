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

## Step 5 - Connect logs to BigQuery

* https://console.cloud.google.com/bigquery and Enable BigQuery
* https://console.cloud.google.com/logs/exports to set up log exports
* Click "Create Export"
* Set sink name: "BQ"
* Set sink service: "Bigquery"
* Set sink destination: 
  * "Create new BigQuery dataset"
  * Set dataset name: "appengine_logs"

## Step 6 - Schedule daily data preparation in BigQuery

* Update SQL below to reference your project name and paste into BigQuery query page - https://console.cloud.google.com/bigquery
* Run query to test
* Click "Schedule Query" and schedule to run daily
  * Dataset name: "dailySet"
  * Table name: "dailyResult_{run_time-1h|"%Y%m%d"}"
  * Destination table write preference: "Overwrite table"

```SQL
#standardSQL

SELECT
  timestamp,
  REGEXP_EXTRACT(protoPayload.resource, r"av=([^&]+)") AS av,
  REGEXP_EXTRACT(protoPayload.resource, r"id=([^&]+)") AS id,
  REGEXP_EXTRACT(protoPayload.resource, r"seg=([^&]+)") AS seg,
  SAFE_CAST(REGEXP_EXTRACT(REGEXP_EXTRACT(protoPayload.resource, r'times=([^&]+)'),r'^(d+)%7C') as int64) AS render_to_q1_time_ms,
  SAFE_CAST(REGEXP_EXTRACT(REGEXP_EXTRACT(protoPayload.resource, r'times=([^&]+)'),r'^d+%7C(d+)$') as int64) AS q1_to_end_time_ms,
  ARRAY_LENGTH(SPLIT(REGEXP_EXTRACT(protoPayload.resource, r'response=([^&]+)'),'%7C')) as num_questions,
  REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_EXTRACT(protoPayload.resource, r"response=([^&]+)"), r"%3A",":"),"%7C","|") AS response,
  REGEXP_REPLACE(REGEXP_REPLACE(REGEXP_EXTRACT(protoPayload.resource, r"visual=([^&]+)"), r"%3A",":"),"%7C","|") AS visual_response,
  REGEXP_EXTRACT(protoPayload.line[OFFSET(0)].logMessage, r"(?i:ResponseReceiver):\s*(.*?)\s*$") AS location,
  REGEXP_EXTRACT(protoPayload.resource, r"(?:cid|bomid)=([^&]+)") AS bomid,
  REGEXP_EXTRACT(protoPayload.line[OFFSET(1)].logMessage, r"bomcookie=([^;]+);") AS bomCookie,
  REGEXP_EXTRACT(protoPayload.resource, r"size=([^&]+)") AS size,
  protoPayload.userAgent AS userAgent,
  REGEXP_EXTRACT(protoPayload.resource, r"response=([^&]+)") AS rawResponse,
  protoPayload.requestId AS protoPayload_requestId,
  protoPayload.line[OFFSET(0)].logMessage AS logMessage,
  protoPayload.line[OFFSET(1)].logMessage AS bomCookieLogRaw,
  protoPayload.resource AS rawResource
FROM `[TODO set your_project_name].appengine_logs.appengine_googleapis_com_request_log_*`
WHERE
_TABLE_SUFFIX = format_date('%Y%m%d', date_sub(current_date(), interval 1 day))
AND protoPayload.method = "GET"
AND protoPayload.wasLoadingRequest IS NULL
AND REGEXP_CONTAINS(protoPayload.resource, "^\\/measure\\?.*")
```

## Step 7 - Report on surveys

Sample query:

```SQL
SELECT
  DATE(timestamp) dt, 
  NTH(1, SPLIT(seg,'_')) age,
  NTH(2, SPLIT(seg,'_')) gender,
  NTH(2, SPLIT(NTH(1, SPLIT(response,'|')),':')) response1,
  NTH(2, SPLIT(NTH(2, SPLIT(response,'|')),':')) response2,
  NTH(2, SPLIT(NTH(3, SPLIT(response,'|')),':')) response3,

  FROM (
    SELECT
      bomcookie,
      FIRST(seg) seg,
      FIRST(location) location,
      FIRST(response) response,
      FIRST(timestamp) timestamp 
    FROM
      TABLE_DATE_RANGE(
        [[your_project_name].dailySet.dailyResult_],
        TIMESTAMP(2019-07-01),
        current_timestamp()
      )
  WHERE
    id = "[your_unique_study_id]"
    GROUP BY bomcookie
    ORDER BY timestamp ASC
  )
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
