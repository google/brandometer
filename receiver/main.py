# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""# Documentation of receiver: It takes in responses from end users that have # completed the creative deployed by customers and writes the required data into # BigQuery on Google Cloud Platform.

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
import datetime
import os

from google.cloud import bigquery
from google.cloud.exceptions import NotFound


def receiver(request):
  params = {}
  params.update(request.get_json() or {})
  params.update(request.args or {})

  client = bigquery.Client()
  table_id = os.environ.get("TABLE_ID")

  try:
    client.get_table(table_id)  # Make an API request.
    print("Table {} already exists.".format(table_id))
  except NotFound:
    print("Table {} is not found- creating.".format(table_id))
    # Create the table.
    schema = [
        bigquery.SchemaField("CreatedAt", "DATETIME", mode="REQUIRED"),
        bigquery.SchemaField("Type", "String", mode="REQUIRED"),
        bigquery.SchemaField("ID", "String", mode="REQUIRED"),
        bigquery.SchemaField("Segmentation", "String", mode="REQUIRED"),
        bigquery.SchemaField("Response", "String", mode="REQUIRED"),
        bigquery.SchemaField("Visual", "String", mode="REQUIRED"),
        bigquery.SchemaField("CreativeSize", "String", mode="REQUIRED"),
        bigquery.SchemaField("RandomTimeStamp", "String", mode="REQUIRED"),
        bigquery.SchemaField("BomID", "String", mode="REQUIRED"),
    ]
    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)
    print("Created table {}.{}.{}".format(table.project, table.dataset_id,
                                          table.table_id))

  # Writing parameters into bigquery table.

  row_to_insert = {
      "CreatedAt": datetime.datetime.now().isoformat(),
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
  return ({"errors": errors}, 200, {})
