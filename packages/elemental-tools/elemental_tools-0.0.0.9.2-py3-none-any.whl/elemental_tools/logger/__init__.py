import os
from time import sleep
from datetime import datetime

from elemental_tools.design import unicode_colors


def relative(path):
	return os.path.join(os.path.dirname(__file__), path)


class Logger:

	def __init__(self, app_name: str, owner: str, log_path: str = None, environment: str = None):
		if app_name is None:
			self.app_name_upper = 'YOUR-APP-NAME-GOES-HERE'
		else:
			self.app_name_upper = str(app_name).upper()

		self.path = log_path
		self.environment = environment
		self.owner = owner

	def log(self, level: str, message, app_name: str = None, **kwargs):
		timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
		level = level.upper()
		owner = self.owner.upper()
		correspondent_clr = unicode_colors.reset
		_current_app = self.app_name_upper

		if app_name is not None:
			_current_app = str(app_name).upper()

		def generate_log_path():
			if self.environment is not None:
				self.path = str(self.log_path + f"_{self.environment}")
			try:
				os.makedirs(self.path, exist_ok=True)
			except:
				pass
			filename = datetime.now().strftime('%d-%m-%Y') + ".log"
			self.log_path = os.path.join(self.path, filename)
			sleep(0.5)
			return self.log_path

		message_enclouser = timestamp + f" - [{_current_app}]" + f" [{owner}]" + ' ' + ' '.join([f'[{str(item).upper()}]' for item in [*kwargs.values()]]) + f" [{level}]"

		content = f"\n{message_enclouser.replace('  ', ' ')}: {str(message)}"

		if self.path is not None:
			with open(generate_log_path(), 'a+') as f:
				f.write(str(content))

		if level == 'INFO' or level == 'START':
			correspondent_clr = unicode_colors.success_cyan
		elif level == 'WARNING' or level == 'ALERT':
			correspondent_clr = unicode_colors.alert
		elif level == 'SUCCESS' or level == 'OK':
			correspondent_clr = unicode_colors.success
		elif level in ['CRITICAL', 'ERROR', 'FAULT', 'FAIL', 'FATAL']:
			correspondent_clr = unicode_colors.fail

		print(correspondent_clr, content[1:], unicode_colors.reset)
		return content
