import os.path
from typing import Any

from dotenv import load_dotenv
import json
from bson import ObjectId
from pydantic import BaseModel

from elemental_tools.db.mongo import Connect, Index

from elemental_tools.Jarvis.scriptize.config import app_name, envi, db_url, logger, database_name
from elemental_tools.Jarvis.scriptize.api.config import root_user

if "install" in __name__:
	from elemental_tools.logger import Logger
	logger = Logger(app_name=f'{os.path.basename(__name__)}', owner='installation').log

from elemental_tools.Jarvis.scriptize.exceptions import SettingMissing


collection_name = f'settings'

database = Connect(db_url, database_name)
collection = database.collection(collection_name)

_setting_indexes = [Index(['name', 'uid'], unique=True, sparse=True)]

database.set_indexes(collection_name, _setting_indexes)


class Setting(BaseModel):
	name: str
	value: Any

	"""
	Default setting class
	:param name: The name of the setting
	:param value: The value of the setting
	"""


class SettingsController:
	"""
	Manipulates settings class
	"""

	def __init__(self):
		self._collection = collection

	def set(self, uid, _setting: Setting):
		try:
			# parse the document

			_update_selector = {
				"$and": [
					{"name": _setting.name},
					{"uid": uid}
				]
			}

			_update_content = {
				"$set": _setting.model_dump()
			}

			insert = self._collection.update_one(_update_selector, _update_content, upsert=True)

			return insert

		except Exception as e:
			logger('error', f'Failed to store user because of exception: {str(e)}')

		return False

	def get(self, uid, name, ignore_default=None, **kwargs):
		result = None
		try:
			selector = {"$and": [{"name": name}, {"uid": uid}]}
			result = self._collection.find_one(selector)['value']
			return result
		except:
			if not kwargs.items() and ignore_default is not None:
				raise SettingMissing(name)
			else:
				if result is None:
					try:
						result = kwargs['default']
					except KeyError:
						raise SettingMissing(name)

		return result


# INSTALL
class SettingsInstaller:

	_settings = SettingsController()

	def __init__(self):
		self.google_sheet_users_root_folder_id = Setting(name="google_sheet_users_root_folder_id", value="")
		self.google_sheet_default_permissions = Setting(name="google_sheet_default_permissions", value=[])
		self.transaction_cooldown = Setting(name='transaction_cooldown', value=5)

	def check(self):

		for _name, _value in vars(self).items():
			try:
				self._settings.get(root_user, _name, ignore_default=True)

			except:
				logger('alert', f"Default configuration: {_name} was not found at settings database.")

				try:
					logger('installing', f"Installing {_name}...")
					self._settings.set(root_user, getattr(self, _name))
				except:
					raise Exception(f'Default configuration {_name} was not set, please reinstall or update.')


settings = SettingsController()


def default_tax():
	logger('info', 'Retrieving tax information...')
	load_dotenv()
	tax = settings.get('crypto_default_taxes', 0.0065)
	logger('success', f'The defined tax is: {tax}')
	return tax

