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
"""Importing Google Firestore for survey storage."""
from google.cloud import firestore

db = firestore.Client()
survey_collection = db.collection(u'Surveys')


def get_all():
  return survey_collection.stream()


def get_by_id(survey_id):
  return survey_collection.document(survey_id)


def get_doc_by_id(survey_id):
  ref = get_by_id(survey_id)
  return ref.get()


def delete_by_id(survey_id):
  survey_collection.document(survey_id).delete()


def update_by_id(survey_id, data):
  ref = survey_collection.document(survey_id)
  ref.update(data)
  return ref


def create(data):
  ref = survey_collection.document()
  ref.set(data)
  return ref
