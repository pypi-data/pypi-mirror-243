from datetime import datetime

from dateutil.relativedelta import relativedelta
from elemental_tools.logger import Logger
from elemental_tools.db.mongo import Connect, Index
from fastapi import HTTPException
from icecream import ic
from pydantic import BaseModel

from elemental_tools.scriptize.api.settings import settings
from elemental_tools.scriptize.config import db_url, log_path, database_name

collection_name = f'transaction'

logger = Logger(app_name='controllers', owner=collection_name, log_path=log_path).log

_transaction_indexes = [
	Index(['uid', 'status', 'amount_from', 'amount_to', 'price', 'currency_from', 'currency_to', 'creation_date'],
		  unique=True, sparse=True),
]


def get_cooldown():
	return str(settings.get(uid='root', name='transaction_cooldown', default=5))


class TransactionRequestModel(BaseModel):
	creation_date: str = datetime.now().isoformat()
	uid: str
	currency_from: str = "BRL"
	currency_to: str = "USDT"
	price: float = None
	amount_from: float = None
	amount_to: float = None


class TransactionController:
	database = Connect(db_url, database_name)

	collection = database.collection(collection_name)
	database.set_indexes(collection_name, _transaction_indexes)

	def add(self, transaction: TransactionRequestModel):
		try:
			self._remove_old_transactions(transaction)
			self.collection.insert_one(transaction.model_dump())
			return transaction
		except Exception as e:
			logger('error', f'Cannot add transaction: {str(vars(transaction))} because of exception: {str(e)}')

	def _remove_old_transactions(self, transaction: TransactionRequestModel):

		_selector_user_old_transactions = {
			"$and": [
				{"uid": transaction.uid},
				{"status": {"$exists": False}},
				{"processed": {"$exists": False}},
				{"exported": {"$exists": False}}
			]
		}

		_user_old_transactions = self.collection.find(_selector_user_old_transactions)
		_user_old_transactions = list(_user_old_transactions)

		if len(_user_old_transactions):
			for old_transaction in _user_old_transactions:
				self.collection.delete_many({"_id": old_transaction["_id"]})

		else:
			logger('alert', f'Remove old transaction skipping, since no old transactions were found.')

	def query(self, selector):
		result = None
		result = self.collection.find(selector)
		if result:
			return result

	def close_transaction(self, transaction: TransactionRequestModel):

		_cooldown_date = datetime.now() - relativedelta(minutes=int(get_cooldown()))

		_pipeline_transactions = [
			{
				'$addFields': {
					'transactionType': 'open',
					"five_min_ms": {"$toLong": {"$toDate": str(_cooldown_date)}},
					'creation_date_isoformat': {"$toLong": {"$toDate": '$creation_date'}}
				}
			},
			{
				"$match": {
					"$and": [
						{"status": {"$exists": False}},
						{"uid": transaction.uid},
						{'$expr': {'$lte': ["$five_min_ms", "$creation_date_isoformat"]}}
					]
				}
			},
			{
				'$sort': {
					'creation_date': 1
				}
			}
		]

		try:
			
			_current_transaction_list = self.collection.aggregate(_pipeline_transactions)
			_current_transaction_list = list(_current_transaction_list)
			logger("info", f"user transaction: {_current_transaction_list}")
			if len(_current_transaction_list):
				_now = datetime.now().isoformat()

				_result = self.collection.update_one({"_id": _current_transaction_list[0]['_id']},
													 {"$set": {"status": True, "date": str(_now)}})
				if _result.modified_count:
					logger('success', f"Transaction closed: {_current_transaction_list[0]}")
					return _current_transaction_list[0]

		except Exception as e:
			logger('alert', f'Cannot get transaction because of exception: {e}')

		return False

	def get_to_export_transactions(self, uid):
		try:
			_pipeline_to_export_transactions = [
				{
					'$match': {
						"$and": [
							{"uid": str(uid)},
							{"exported": {"$exists": False}},
							{"status": True}
						]}
				},
				{
					'$sort': {
						'creation_date': 1
					}
				}
			]

			_current_transaction_list = self.collection.aggregate(_pipeline_to_export_transactions)
			_current_transaction_list = list(_current_transaction_list)
			logger("info", f"user transactions list: {_current_transaction_list}")
			if len(_current_transaction_list):
				return _current_transaction_list

		except Exception as e:
			logger('alert', f'Cannot get transaction because of exception: {e}')

		return False

	def set_exportation_status(self, transaction_ids: list):
		selector = {"_id": {"$in": transaction_ids}}
		_current_transaction_list = self.collection.find(selector)
		_closed_date = datetime.now().isoformat()
		_result = self.collection.update_one(selector, {"$set": {"exported": True, "date": _closed_date}})

		if _result.modified_count:
			logger('success', f"Transaction exported example: {_current_transaction_list[0]}")
			return _current_transaction_list[0]
