"""TODO(jerraldwee): DO NOT SUBMIT without one-line documentation for receiver.

TODO(jerraldwee): DO NOT SUBMIT without a detailed description of receiver.
"""
# function of the receiver is to take into parameters and process them accordingly, 
# writing the required information into a bigquery table.
# file is to be written into 'main.py' on google cloud functions
import logging
import datetime

from google.cloud import bigquery
from google.cloud.exceptions import NotFound

def receiver(request):
  params = {}
  params.update(request.get_json() or {})
  params.update(request.args or {})

  client = bigquery.Client()
  table_id = "jerraldwee-testing.jerraldwee_test.jerraldwee_test_receiver"

  # Check if table exists. https://cloud.google.com/bigquery/docs/samples/bigquery-table-exists
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
      bigquery.SchemaField("Creative_Size","String",mode="REQUIRED"),
      bigquery.SchemaField("RandomTimeStamp","String",mode="REQUIRED"),
      bigquery.SchemaField("BomID","String",mode="REQUIRED"),
    ]
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)
    print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))

  # Write params into table.
  # params = {?type=survey&id=5694467986161664&seg=Female_25-34_expose&response=1%3AA&visual=1%3AC&creative_size=300x250&randomtimestamp=2236200.2053949493&bomid=d06c2dea-892f-45f3-a038-bef0ba75fad4&times=24380%7C0 }
  # type=survey&
  # id=5694467986161664&
  # seg=Female_25-34_expose&
  # response=1%3AA&
  # visual=1%3AC&
  # creative_size=300x250&
  # randomtimestamp=2236200.2053949493&
  # bomid=d06c2dea-892f-45f3-a038-bef0ba75fad4&
  # times=24380%7C0 }

  row_to_insert = {
      "Type": params.get("type"),
      "ID": params.get("id"),
      "Segmentation": params.get("seg"),
      "Response": params.get("response"),
      "Visual": params.get("visual"),
      "Creative_Size": params.get("creative_size"),
      "RandomTimeStamp": params.get("randomtimestamp"),
      "BomID": params.get("bomid"),
      # TODO: Jerrald to complete based on params list above
  }

  errors = client.insert_rows_json(table_id, [row_to_insert])

  return "done"
