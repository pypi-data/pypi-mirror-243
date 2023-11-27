import os
from elemental_tools.Jarvis.scriptize.config import log_path
from elemental_tools.logger import Logger

logger = Logger(app_name='scriptize-api', owner='initialization', log_path=log_path).log

host = os.environ.get('HOST', 'http://vault.local')
port = int(os.environ.get('PORT', '7007'))

app_name = os.environ.get('APP_NAME', 'scriptize')
root_user = 'root'
