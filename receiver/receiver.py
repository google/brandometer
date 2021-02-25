"""
# Documentation of receiver: It takes in responses from end users that have
# completed the creative deployed by customers and writes the required data into
# BigQuery on Google Cloud Platform.

# Description of receiver:
# The function of the receiver is to capture the survey responses from end
# users, which comes in a string format with parameters. The receiver processes
# all incoming responses and creates a bigquery table if there is no existing
# one. If a bigquery table exists, the data would be written to its
# corresponding columns and rows. The receiver exists on the Google Cloud
# Platform with an external public HTTP endpoint in the US-Central1 region and
# is able to receive all responses from the end users. 

"""

import logging

from google.cloud import bigquery
from google.cloud.exceptions import NotFound

def receiver(request):
  params = {}
  params.update(request.get_json() or {})
  params.update(request.args or {})

  client = bigquery.Client()
  table_id = "jerraldwee-testing.jerraldwee_test.jerraldwee_test_receiver"

  try:
    client.get_table(table_id)  # Make an API request.
    print("Table {} already exists.".format(table_id))
  except NotFound:
    print("Table {} is not found- creating.".format(table_id))
    # Create the table.
    schema = [
      bigquery.SchemaField("Type","String",mode="REQUIRED"),
      bigquery.SchemaField("ID","String",mode="REQUIRED"),
      bigquery.SchemaField("Segmentation","String",mode="REQUIRED"),
      bigquery.SchemaField("Response","String",mode="REQUIRED"),
      bigquery.SchemaField("Visual","String",mode="REQUIRED"),
      bigquery.SchemaField("CreativeSize","String",mode="REQUIRED"),
      bigquery.SchemaField("RandomTimeStamp","String",mode="REQUIRED"),
      bigquery.SchemaField("BomID","String",mode="REQUIRED"),
    ]
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)
    print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))

  # Writing parameters into bigquery table.

  row_to_insert = {
      "Type": params.get("type"),
      "ID": params.get("id"),
      "Segmentation": params.get("seg"),
      "Response": params.get("response"),
      "Visual": params.get("visual"),
      "CreativeSize": params.get("creative_size"),
      "RandomTimeStamp": params.get("randomtimestamp"),
      "BomID": params.get("bomid"),
  }

  errors = client.insert_rows_json(table_id, [row_to_insert])

  return {errors:errors}
