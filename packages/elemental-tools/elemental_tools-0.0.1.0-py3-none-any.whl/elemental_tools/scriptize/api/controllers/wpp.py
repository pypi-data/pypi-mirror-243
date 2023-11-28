from elemental_tools.logger import Logger
from elemental_tools.db.mongo import Connect, Index
from fastapi import HTTPException

from elemental_tools.scriptize.config import db_url, log_path, database_name

logger = Logger(app_name='controllers', owner='wpp', log_path=log_path).log
from pymongo import results

collection_name = f'wpp'

_wpp_indexes = [
			Index(['wpp_contact_title', 'msg_id'], unique=True, sparse=True),
			Index(['wpp_user_id', 'msg_id'], unique=True, sparse=True),
		]

database = Connect(db_url, database_name)

collection = database.collection(collection_name)
database.set_indexes(collection_name, _wpp_indexes)


class WppController:

	def __init__(self, timeout: int = None):
		self.timeout = 5
		if timeout is not None:
			self.timeout = timeout

		self.database = database

	def add(self, doc):
		insert = collection.insert_one(dict(doc))

		_inserted_item = collection.find_one({"_id": insert.inserted_id})

		return _inserted_item

	def query(self, selector):
		result = None
		query_result = collection.find(selector)
		if query_result:
			return query_result
		return result

	def select(self, selector: dict):
		return collection.find_one(selector)

	def update(self, selector, content):
		logger('info', f'Updating User Information for Selector: {selector} with: {str(content)} ')
		_update_result = None
		_content = {"$set": content}

		try:
			_update_result = collection.update_one(selector, _content)

			if _update_result is None:
				raise HTTPException(detail='Cannot update user information.', status_code=400)

		except Exception as e:
			logger('error', f'Cannot update user information: {str(e)}')

		return _update_result
