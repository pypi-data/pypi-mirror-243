import json
import requests


class User:
	endpoint = "/user"
	exists = False
	language = None
	host: str

	def __init__(self, wpp_contact_title, language=None, uid=None):

		if uid is not None:
			user = requests.get(url=str(self.host + self.endpoint), params={'wpp_contact_title': wpp_contact_title})

		else:
			user = requests.get(url=str(self.host + self.endpoint), params={'_id': uid})

		if user.status_code == 200:
			self.exists = True
			for key, value in user.json().items():
				setattr(self, key, value)

		elif user.status_code == 404:
			for key, value in user.json()['model'].items():
				if user.json()['model'][key] is None:
					value = getattr(self, key, None)
				setattr(self, key, value)

	def save(self):
		result = requests.post(url=str(self.host + self.endpoint + "/add"), data=json.dumps(self.__dict__))

		if result.status_code == 500:
			return None

		return result


class Statement:
	endpoint = "/statement"
	exists = False
	language = None
	host: str

	def __init__(self, wpp_contact_title=None, language=None, uid=None):

		params = {}

		params = {
			'wpp_contact_title': wpp_contact_title
		}

		if uid is not None:
			user = requests.get(url=str(self.host + self.endpoint), params=params)

		else:
			user = requests.get(url=str(self.host + self.endpoint), params={'_id': uid})

		if user.status_code == 200:
			self.exists = True
			for key, value in user.json().items():
				setattr(self, key, value)

		elif user.status_code == 404:
			for key, value in user.json()['model'].items():
				if user.json()['model'][key] is None:
					value = getattr(self, key, None)
				setattr(self, key, value)

	def save(self):
		result = requests.post(url=str(self.host + self.endpoint + "/add"), data=json.dumps(self.__dict__))

		if result.status_code == 500:
			return None

		return result


class Requests:

	def __init__(self, host):
		self.User = User
		self.User.host = host
		self.Statement = User
		self.Statement.host = host
