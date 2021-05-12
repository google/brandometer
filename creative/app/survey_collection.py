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
