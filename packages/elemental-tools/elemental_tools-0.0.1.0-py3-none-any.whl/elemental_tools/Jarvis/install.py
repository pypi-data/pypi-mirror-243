import os

import nltk
from pymongo.errors import DuplicateKeyError

from elemental_tools.scriptize.config import logger
from elemental_tools.Jarvis.config import chrome_options, webdriver_url, log_path, chrome_data_dir, envi

from time import sleep

from selenium import webdriver

from elemental_tools.scriptize.api.settings import SettingsInstaller
from elemental_tools.scriptize.api.settings import SettingsController, Setting, collection as SettingsCollection
from elemental_tools.scriptize.config import enable_grid


class Jarvis:

	_settings = SettingsController()

	developer = "Elemental Company"

	def install(self):
		nltk.download('wordnet')

		_default_settings = [
			Setting(name='website', value=""),
			Setting(name='developer', value="Elemental Company"),
			Setting(name='company_name', value=None),
			Setting(name='default_response_request_attendance', value="To obtain assistance from one of our attendants please type\nI want to talk with an attendant.\nAnd we will help you as fast as we can!"),
			Setting(name='default_response_attendance_time',
					value='Remember that our attendance time is from: 9AM to 6PM.')
		]

		for setting in _default_settings:
			try:
				SettingsCollection.insert_one(document={**setting.model_dump(), **{'uid': 'jarvis'}})
			except DuplicateKeyError:
				pass


class api:
	def install(self):
		SettingsInstaller().check()


profile_limit = 4


def install_jarvis_grid():
	if enable_grid is True:
		# validate for profiles:
		logger('installing', "Now we must provide some profile settings...", app_name='grid-setup')
		logger('installing', "Remember to run 'sudo chmod -R 777' on your volumes folder", app_name='grid-setup')
		logger('profile',
			   f"Check your grid vnc and set up {str(profile_limit)} profiles. So we can get started. Remember, I will be checking one by one by one later!",
			   app_name='grid-setup')
		logger('setting',
			   f"I have checked that your chrome data dir is set to: {chrome_data_dir}, so we must save this profiles into it.",
			   app_name='grid-setup')

		driver_options = chrome_options

		driver_options.add_argument(f"user-data-dir={chrome_data_dir}")

		logger('info', f"Now please provide me some profiles. {str(profile_limit)} to be exact...",
			   app_name='grid-setup')
		_b = webdriver.Remote(command_executor=webdriver_url, options=driver_options)

		logger('info', f"Just press enter when your work is ready to be verified.", app_name='grid-setup')

		input()
		_b.close()
		_c_profile = 0

		for each in os.listdir(chrome_data_dir):
			if os.path.isdir(each):
				try:
					_c_profile += 1
					_driver_options = chrome_options
					_driver_options.add_argument(f"profile-directory=Profile {str(_c_profile)}")
					_driver_options.add_argument(f"user-data-dir={chrome_data_dir}")
					_b = webdriver.Remote(command_executor=webdriver_url, options=_driver_options)

					sleep(1)
					_b.close()
					sleep(1)
				except Exception as e:
					raise Exception(
						f"You're a liar!!! I found a error verifying the profile n {str(_c_profile)}. Get back when you're ready. Or this exception stops happen: {str(e)}")

		logger('success', f"All profiles verified.", app_name='grid-setup')

	else:
		raise Exception('You must enable grid-setup on the .env file or in the environment variables to be able to use the selenium grid.')



if __name__ == "__main__":
	Jarvis().install()
	api().install()
	install_jarvis_grid()
