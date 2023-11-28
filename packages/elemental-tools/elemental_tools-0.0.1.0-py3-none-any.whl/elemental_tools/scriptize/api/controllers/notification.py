from datetime import datetime

from bson import ObjectId
from elemental_tools.logger import Logger
from elemental_tools.db.mongo import Connect, Index
from fastapi import HTTPException

from elemental_tools.scriptize.api.models.notification import NotificationRequestModel
from elemental_tools.scriptize.config import db_url, log_path, database_name

logger = Logger(app_name='controllers', owner='notification', log_path=log_path).log

collection_name = f'notification'


class NotificationController:
	database = Connect(db_url, database_name)

	collection = database.collection(collection_name)

	def __init__(self, timeout: int = None, responses_selector={"$and": [{"last_response_execution": None}, {"last_response_execution": {"$exists": True}}]}, default_selector={"$and": [{'status': False}, {"content": {"$ne": None}}]}):
		self.timeout = 5
		if timeout is not None:
			self.timeout = timeout

		self.database = self.database
		self.notification_selector = default_selector
		self.responses_selector = responses_selector

	def add(self, doc: NotificationRequestModel):

		if all([doc.uid is None, doc.role is None]):
			raise Exception("You must specify at least one option: 'uid' or 'role' in order to add a notification.")

		insert = self.collection.insert_one(dict(**doc.__dict__))

		_inserted_item = self.collection.find_one({"_id": insert.inserted_id})

		return _inserted_item

	def set_content(self, doc: NotificationRequestModel):

		if all([doc.uid is None, doc.role is None]):
			raise Exception("You must specify at least one option: 'uid' or 'role' in order to add a notification.")

		_update_result = self.collection.update_one({"_id": doc.get_id()}, {"$set": doc.model_dump()})

		_inserted_item = self.collection.find_one({"_id": _update_result.upserted_id})

		return _inserted_item

	def set_responses_status(self, filter_):
		_result = self.collection.update_many({"_id": {"$in":[ObjectId(f) for f in filter_]}},
											  {"$set": {'last_response_execution': datetime.now().isoformat()}})
		return _result.modified_count

	def set_response(self, who: ObjectId, protocol: ObjectId, content: str):
		_update_result = self.collection.update_one({"_id": protocol}, {"$set": {"responser_id": who, "response": content, "last_response_execution": None}})

		return _update_result.modified_count

	def query(self, selector):
		result = None
		query_result = self.collection.find_one(selector)
		if query_result:
			return query_result
		return result

	def select(self, selector: dict):
		return self.collection.find_one(selector)

	def update(self, selector, content):
		logger('info', f'Updating User Information for Selector: {selector} with: {str(content)} ')
		_update_result = None
		_content = {"$set": content}

		try:
			_update_result = self.collection.update_one(selector, _content)

			if _update_result is None:
				raise HTTPException(detail='Cannot update user information.', status_code=400)

		except Exception as e:
			logger('error', f'Cannot update user information: {str(e)}')

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

	def query_all(self, selector):
		result = None
		query_result = self.collection.find(selector)
		if query_result:
			return query_result
		return result

	def is_there_notifications(self):

		return self.collection.count_documents(self.notification_selector) > 0

	def set_notifications_status(self, filter_):
		_result = self.collection.update_many({"_id": {"$in": [ObjectId(f) for f in filter_]}},
											  {"$set": {'status': True}})

		return _result.modified_count

	def is_there_responses(self):
		return self.collection.count_documents(self.responses_selector) > 0

