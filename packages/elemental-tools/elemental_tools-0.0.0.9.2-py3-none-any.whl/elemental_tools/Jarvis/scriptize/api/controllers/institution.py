from bson import ObjectId
from elemental_tools.logger import Logger
from elemental_tools.db.mongo import Connect, Index
from fastapi import HTTPException

from elemental_tools.Jarvis.scriptize.config import db_url, log_path, database_name
from pymongo import results

logger = Logger(app_name='controllers', owner='institution', log_path=log_path).log

collection_name = f'institutions'

_institution_indexes = [
			Index(['tax_number', 'name'], unique=True, sparse=True),
		]


class InstitutionController:
	database = Connect(db_url, database_name)

	collection = database.collection(collection_name)
	database.set_indexes(collection_name, _institution_indexes)

	def __init__(self, timeout: int = None):
		self.timeout = 5
		if timeout is not None:
			self.timeout = timeout

		self.database = self.database

	def add(self, doc):
		insert = self.collection.insert_one(dict(doc))

		_inserted_item = self.collection.find_one({"_id": insert.inserted_id})

		return _inserted_item

	def query(self, selector):
		result = None
		query_result = self.collection.find_one(selector)
		if query_result:
			return query_result
		return result

	def query_all(self, selector):
		result = None
		query_result = self.collection.find(selector)
		if query_result:
			return query_result
		return result

	def select(self, selector: dict):
		return self.collection.find_one(selector)

	def update(self, selector, content):
		logger('info', f'Updating Institution Information for Selector: {selector} with: {str(content)} ')
		_update_result = None
		_content = {"$set": content}

		try:
			_update_result = self.collection.update_one(selector, _content)

			if _update_result is None:
				raise HTTPException(detail='Cannot update institution information.', status_code=400)

		except Exception as e:
			logger('error', f'Cannot update institution information: {str(e)}')

		return _update_result

	def get_status(self, uid):
		_result = None
		print(f'get_status selector "_id":{ObjectId(uid)}')
		query_result = self.collection.find_one({"_id": ObjectId(uid)})
		if 'status' in query_result.keys():
			_result = query_result['status']
		if _result is not None:
			return _result
		return False


