import os
import sys

from dotenv import load_dotenv
from elemental_tools.logger import Logger

module_name = 'api+task-manager'
app_name = os.environ.get('APP_NAME', 'scriptize-api')

envi = os.environ.get('environment', None)

# load cache into class
cache_file = './_cache/.dump'
if envi is None:
	if sys.platform == "darwin" or sys.platform == "win32":
		envi = 'debug'
	else:
		envi = 'production'

log_path = os.environ.get("LOG_PATH", default=None)

if log_path is not None:
	log_path += "_" + envi
logger = Logger(app_name='scriptize', owner='initialization', log_path=log_path).log

logger('info', 'Setting Environment (debug, production) based on platform')
if envi is None:
	if sys.platform == "darwin" or sys.platform == "win32":
		envi = 'debug'
	else:
		envi = 'production'
logger('success', 'The current environment is set to ' + envi)


class Cache:

	def __init__(self, file: str =cache_file):
		self.cache_file = file

		if not os.path.isdir(os.path.dirname(os.path.abspath(cache_file))):
			os.makedirs(os.path.dirname(os.path.abspath(cache_file)), exist_ok=True)

		self.cache_file_content = open(cache_file, 'a+')
		if self.cache_file_content.readlines():
			self.cache_file_content = self.load()
			try:
				data = eval(self.cache_file_content.read())
				for cache_item in data:
					for title, value in cache_item.items():
						setattr(self, title, value)

			except SyntaxError:
				raise Exception("Failed to parse the cache file!")

	def save(self):
		self.cache_file_content.write(str([{title: value for title, value in self.__dict__.items() if not title.startswith('__')}]))
		self.cache_file_content.close()
		return open(cache_file, 'a+')

	def load(self):
		return open(self.cache_file, 'a+')

	def get(self, prop):
		return getattr(self, prop, None)


logger('info', 'Loading .env file...')
load_dotenv()
logger('success', '.env file loaded successfully!')
webdriver_url = os.environ.get('WEBDRIVER_URL', 'http://localhost:4444/')

logger('info', 'Setting up configuration variables...')

db_url = os.environ.get('DB_URL', None)

host = os.environ.get('HOST', '127.0.0.1')
port = int(os.environ.get('PORT', 10200))
download_path = os.environ.get('DOWNLOAD_PATH',  '/Users/tom/teste')
thread_limit = 10
enable_grid = os.environ.get('ENABLE_GRID', False)
database_name = os.environ.get('DB_NAME', str(app_name + f"_{envi}"))
logger('success', 'The configuration variables were successfully set.')

logger('info', 'Loading secrets and keys, shhh...')
binance_key = os.environ.get('BINANCE_KEY', None)
binance_secret = os.environ.get('BINANCE_SECRET', None)

b4u_url = os.environ.get('B4U_API_URL', None)
b4u_key = os.environ.get('B4U_API_KEY', None)
b4u_secret = os.environ.get('B4U_API_SECRET', None)
logger('success', 'The configuration variables were successfully set.')




