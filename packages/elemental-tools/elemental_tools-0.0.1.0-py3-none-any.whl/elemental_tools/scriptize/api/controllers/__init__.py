from pydantic import BaseModel
from elemental_tools.scriptize.api.config import logger
from elemental_tools.db.mongo import Connect, Index
from datetime import datetime, timedelta
from fastapi.exceptions import HTTPException
from elemental_tools.scriptize.config import db_url, database_name


collection_name = f'tasks'

_indexes = [
	Index(['uid', 'title', 'status', 'schedule_date', 'task_name'], unique=True, sparse=True),
]

database = Connect(db_url, database_name)
collection = database.collection(collection_name)

database.set_indexes(collection_name, _indexes)


class TaskController:

	def add(self, doc: BaseModel):
		try:
			inserted_doc = collection.insert_one(doc.model_dump())

			if inserted_doc.inserted_id is None:
				raise HTTPException(detail='Cannot save task.', status_code=400)

			return inserted_doc.inserted_id

		except Exception as e:
			logger('error', f'Failed to store user because of exception: {str(e)}')

		return False

	def set_loop_count(self, _id: str, loops: int):
		logger('info', f'Setting loop count: {loops} for task _id: {str(_id)} ')

		selector = {'_id': _id}
		content = {"$set": {'loops': loops}}

		try:
			_update_result = collection.update_one(selector, content)
			if _update_result is None:
				raise HTTPException(detail='Cannot set task loop count.', status_code=400)

		except Exception as e:
			logger('error', f'Cannot set loop count for task because of exception: {str(e)}')

		return False

	def set_last_execution(self, _id):
		logger('info', f'Setting last execution for task _id: {str(_id)}')

		try:
			_current_date = datetime.now().isoformat()
			_update_result = database.collection(collection_name).update_one({'_id': _id}, {"$set": {'last_execution': _current_date}})

			if not _update_result:
				raise Exception('Cannot set task last execution date.')

		except Exception as e:
			logger('error', f'Cannot set last execution for task because of exception: {str(e)}')

		return False

	def query_not_processed_tasks(self):

		_current_date = datetime.now().isoformat()
		_too_old = datetime.now() - timedelta(days=100)

		_pipeline_functions_counter = [
			{
				'$addFields': {
					'functionType': 'counter',
					'currentTime': {'$toLong': {"$toDate": str(_current_date)}},
					'tooOld': str(_too_old),
					'lastExecutionInMS': {'$toLong': {"$toDate": '$last_execution'}}
				}
			},
			{
				"$match": {
					"$and": [
						{'status': True},
						{'schedule_date': None},
						{'timer': {'$ne': None}},
						{'loops': {'$gt': 0}},
						{'$expr': {'$gte': [{'$subtract': ['$currentTime', '$lastExecutionInMS']}, '$timer']}}
					]
				}
			}
		]
		_pipeline_functions_infinite = [
			{
				'$addFields': {
					'functionType': 'infinite',
					'currentTime': {'$toLong': {"$toDate": str(_current_date)}},
					'tooOld': str(_too_old),
					'lastExecutionInMS': {'$toLong': {"$toDate": '$last_execution'}}
				}
			},
			{
				"$match": {
					"$and": [
						{'status': True},
						{'schedule_date': None},
						{'timer': {'$ne': None}},
						{'loops': None},
						{'$expr': {'$gte': [{'$subtract': ['$currentTime', '$lastExecutionInMS']}, '$timer']}}
					]
				}
			}
		]
		_pipeline_functions_scheduled = [
			{
				'$addFields': {
					'functionType': 'scheduled',
					'currentTime': {'$toLong': {"$toDate": str(_current_date)}},
					'tooOld': str(_too_old),
					'lastExecutionInMS': {'$toLong': {"$toDate": '$last_execution'}}
				}
			},
			{
				"$match": {
					"$and": [
						{'status': True},
						{'schedule_date': {'$ne': None}},
						{'$expr': {'$gte': [{'$subtract': ['$currentTime', '$lastExecutionInMS']}, '$timer']}}
					]
				}
			}
		]

		# _all_loops = list(collection.aggregate(_pipeline_functions_infinite))

		_result = list(collection.aggregate(_pipeline_functions_infinite))

		_new_tasks = {"$and": [
			{'status': True},
			{"last_execution": {"$exists": False}}
		]}

		_result += list(collection.find(_new_tasks))
		return _result

	def set_status(self, _id: str, status: bool):
		logger('info', f'Setting status task _id: {str(_id)}')

		selector = {'_id': _id}
		content = {"$set": {'status': status}}

		try:
			update_result = collection.update_one(selector, content)
			if update_result is None:
				raise HTTPException(detail='Cannot set task status.', status_code=400)

		except Exception as e:
			logger('error', f'Cannot set task status because of exception: {str(e)}')

		return False

