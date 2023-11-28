from datetime import datetime
from time import sleep
import re

from bson import ObjectId
from deep_translator import GoogleTranslator
from icecream import ic
from selenium import webdriver
from selenium.common import TimeoutException, \
	WebDriverException, NoSuchWindowException

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains


from elemental_tools.logger import Logger
from elemental_tools.Jarvis.config import chrome_options, webdriver_url, log_path, chrome_data_dir
from elemental_tools.Jarvis.brainiac import Brainiac, NewRequest, BrainiacRequest
from elemental_tools.Jarvis.exceptions import Unauthorized, Error, InvalidOption
from elemental_tools.scriptize.api.controllers.user import UserController
from elemental_tools.scriptize.api import constants as Constants
from elemental_tools.scriptize.api.controllers.wpp import WppController
from elemental_tools.scriptize.api.controllers.notification import NotificationController
from elemental_tools.scriptize.api.models import UserRequestModel
from elemental_tools.scriptize.config import enable_grid
from elemental_tools.Jarvis.tools import Tools, extract_and_remove_quoted_content

module_name = 'mercury'

logger = Logger(app_name='jarvis', owner='mercury', log_path=log_path).log


class RequestMercury(BrainiacRequest):
	wpp_contact_title = None
	language = 'en'

	translated_message = None
	translated_message_model = None

	skill_examples = None

	translated_message_model_lemma = None
	user: UserRequestModel = UserRequestModel

	quoted_content = None

	def __init__(self, request):
		super().__init__()

		self.request = request

		for attr_name in dir(request):
			if not callable(getattr(request, attr_name)) and not attr_name.startswith("__"):
				setattr(self, attr_name, getattr(request, attr_name))

	def __call__(self):
		return self.request


class mercury:
	connected = False
	wts_url = "https://web.whatsapp.com/"
	wpp_db = WppController()
	notification_db = NotificationController()
	wpp_contact_title = ""
	user_db = UserController()
	page_content = None
	log_owner = 'mercury'
	driver_options = chrome_options
	_b = webdriver.Chrome
	_cache = []
	_first_state = True
	tools = Tools()

	def __init__(self, brainiac: Brainiac, bypass_translator: bool = False):

		self.bypass_translator = bypass_translator

		self.brainiac = brainiac
		self.brainiac.bypass_translator = bypass_translator

		logger('alert', f'Setting Chrome data dir: {chrome_data_dir}')

		self.driver_options.add_argument(f"profile-directory=Profile 1")
		self.driver_options.add_argument(f"user-data-dir={chrome_data_dir}")

		self.start()

	def is_browser_enabled(self):
		try:
			if self._b.session_id is not None:
				return True
		except:
			try:
				self._b.close()
			except:
				pass

		return False

	def browser(self):

		if not enable_grid:
			self._b = webdriver.Chrome(options=self.driver_options)

		else:
			try:
				self._b = webdriver.Remote(command_executor=webdriver_url, options=self.driver_options)
			except Exception as e:
				logger('critical', f"Browser failed because of an error: {str(e)}")

		return self._b

	def connect(self):
		self._b.get(self.wts_url)

		while not self.connected:
			try:
				logger('info', "Waiting for QR code scan...")

				WebDriverWait(self._b, 1000).until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "_3WByx")))

				self.page_content = self._b.page_source
				self.connected = True

			except TimeoutException:
				print("Timeout occurred. Retrying...")
				sleep(2)
				continue

		return self.connected

	def clean_phone(self, phone):
		_result = phone
		_result = _result.replace(' ', '')
		_result = _result.replace('-', '')
		return _result

	def send_message(self, request: NewRequest):
		wpp_contact_title, message = request.wpp_contact_title, request.skill.result

		log_owner = module_name + '-send-message'
		logger('info', f'Client Title: {str(wpp_contact_title)} Response: {str(message)}')

		self._b.find_element(By.XPATH, f"//span[@dir='auto' and @title='{wpp_contact_title}']").click()
		logger('info', f"""Mercury clicked on: //span[@dir='auto' and @title='{wpp_contact_title}']""")

		input_xpath = (
			'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]'
		)

		input_box = WebDriverWait(self._b, 60).until(
			expected_conditions.presence_of_element_located((By.XPATH, input_xpath)))
		logger('alert', f"Mercury typing...")
		input_box.send_keys(message)
		input_box.send_keys(Keys.ENTER)
		logger('success', f"Message has been sent!")
		sleep(2)

	def get_selected_conversation(self, old=False):
		wpp_contact_title = None
		default_path = """//div[@class='g0rxnol2']//div[@aria-selected='true']//div[contains(@class, '_199zF _3j691')]//div[@class='_8nE1Y']//div[@role='gridcell' and @aria-colindex='2']"""

		# selected_contact = self._b.find_element(By.XPATH, f"{default_path}//div[@class='_21S-L']")

		# wpp_contact_title = selected_contact.find_element(By.XPATH, f"{default_path}//div//span[@dir='auto']").get_attribute("title")

		if not old:
			wpp_contact_title = self._b.find_element(By.XPATH, f"{default_path}//span[@dir='auto']").get_attribute(
				"title")
		else:
			wpp_contact_title = self._b.find_element(By.XPATH, f"{default_path}//span[@dir='auto']").get_attribute(
				"title")

		logger('conversation', f"The selected conversation is: {wpp_contact_title}")

		return wpp_contact_title

	def get_lang_from_country_code(self, wpp_contact_title):
		log_owner = module_name + '-language-selector'
		self.tools.codes_and_languages()
		try:
			contact_lang = [lang for code, lang in self.tools.codes_and_languages().items() if wpp_contact_title.startswith(code)][0]
		except:

			if wpp_contact_title.startswith('+'):
				contact_lang = 'en'
			else:
				contact_lang = 'auto'

		logger('info', f"The defined language is {contact_lang}")
		return contact_lang

	def verify_notifications(self):

		_to_send_notifications = {}
		_to_send_responses = {}

		_result_notifications = {}
		_result_responses = {}

		_is_there_notifications = self.notification_db.is_there_notifications()
		_is_there_responses = self.notification_db.is_there_responses()

		logger('info', f"Verifying for new notifications...")

		# PREPARE NOTIFICATIONS
		if _is_there_notifications:
			logger('info', f"Notifications found!")
			_notifications = self.notification_db.query_all(self.notification_db.notification_selector)
		else:
			logger('alert', f"No Notifications found, skipping...")
			_notifications = []

		# PREPARE RESPONSES
		if _is_there_responses:
			logger('info', f"Responses found!")
			_responses = self.notification_db.query_all(self.notification_db.responses_selector)
		else:
			logger('alert', f"No Responses found, skipping...")
			_responses = []

		# ATTACH NOTIFICATIONS TO BE SENT
		for notification in _notifications:
			try:
				logger('info', f"Processing Notification {str(notification['_id'])}")

				if notification['uid'] is not None:

					_destination = self.user_db.query({'_id': ObjectId(notification['uid'])})

					_content = self.translate_output(notification['content'], _destination['language'])

					_to_send_notifications = {**_to_send_notifications, notification['_id']: {_destination['wpp_contact_title']: _content}}

				if notification['role'] is not None:

					_users_in_role = self.user_db.query_all({'role': {"$in": notification['role']}})

					for user in _users_in_role:

						_destination = self.user_db.query({'_id': ObjectId(user['_id'])})

						_content = self.translate_output(notification['content'], _destination['language'])

						_to_send_notifications[notification['_id']] = {_destination['wpp_contact_title']: _content}
			except:
				pass

		# ATTACH RESPONSES TO BE SENT
		for response in _responses:
			try:
				logger('info', f"Processing Response {str(response['_id'])}")

				if response['client_id'] is not None:

					_destination = self.user_db.query({'_id': ObjectId(response['client_id'])})

					_content = response['response']
					_to_send_responses = {**_to_send_responses, response['_id']: {_destination['wpp_contact_title']: _content}}

			except:
				pass

		# SEND NOTIFICATIONS
		for notification_id in _to_send_notifications:
			try:
				for destination, content in _to_send_notifications[notification_id].items():
					destination = destination
					content = content

					logger('info', f"Sending notification {str(notification_id)} to {str(destination)} and content {str(content)}")

					try:
						_request = NewRequest(
							message=content,
							wpp_contact_title=destination
						)

						_request.skill.result = content

						self.send_message(_request)

						_result_notifications[notification_id] = True

					except:
						_result_notifications[notification_id] = False
			except:
				pass

		# UPDATE THE NOTIFICATION DATABASE
		if _result_notifications.values() and _is_there_notifications:
			logger('info', f"Updating Notification Information")

			_update_notification_filter = []
			for notification_id in _result_notifications:
				if _result_notifications[notification_id]:
					_update_notification_filter.append(notification_id)

			_update_notification_result = self.notification_db.set_notifications_status(_update_notification_filter)

			if _is_there_notifications and all(_result_notifications.values()) and _update_notification_result:
				logger('success', f"Successfully sent notification's!")

			else:
				logger('error', f"Error sending some notification's, you should take a look.")

		# SEND RESPONSES
		for response_id in _to_send_responses:
			try:
				for destination, content in _to_send_responses[response_id].items():
					destination = destination
					content = content

					logger('info', f"Sending Response {str(response_id)} to {str(destination)} and content: {str(content)}")

					try:
						_request = NewRequest(
							message=content,
							wpp_contact_title=destination
						)

						_request.skill.result = content

						_this_user = self.user_db.query({"wpp_contact_title": str(destination)})

						_selector_human_attendance_update = {"$and": [{"_id": ObjectId(_this_user["_id"])}, {"$or": [{"role": {"$exists": False}}, {"role": {"$nin": Constants.internal_roles}}, {"admin": {"$ne": True}}]}]}

						
						_result_pipeline_under_human_attendance = self.user_db.update(_selector_human_attendance_update, {"is_human_attendance": True})

						self.send_message(_request)

						_result_responses[response_id] = True

					except:
						_result_responses[response_id] = False

			except:
				pass

		# UPDATE THE RESPONSES DATABASE
		if _result_responses.values() and _is_there_responses:
			logger('info', f"Updating Responses Information")

			_update_responses_filter = []

			for response_id in _result_responses:
				if _result_responses[response_id]:
					_update_responses_filter.append(response_id)

			_update_responses_result = self.notification_db.set_responses_status(_update_responses_filter)

			if _is_there_responses and all(_result_responses.values()) and _update_responses_result:
				logger('success', f"Successfully sent Responses!")

			else:
				logger('error', f"Error sending some Responses, you should take a look.")

		return _result_notifications, _result_responses

	def translate_input(self, message, language):
		if not self.bypass_translator:
			try:
				logger('info', "Translating input information")

				# Identify text within double quotes using regular expressions
				double_quoted_texts = re.findall(r'"([^"]*)"', message)

				# Identify text within single quotes using regular expressions
				single_quoted_texts = re.findall(r"'([^']*)'", message)

				# Replace text within double quotes with a placeholder
				double_placeholder = 'DOUBLE_QUOTED_TEXT_PLACEHOLDER'
				message_without_double_quotes = re.sub(r'"([^"]*)"', f'"{double_placeholder}"', message)

				# Replace text within single quotes with a placeholder
				single_placeholder = 'SINGLE_QUOTED_TEXT_PLACEHOLDER'
				message_without_quotes = re.sub(r"'([^']*)'", f"'{single_placeholder}'", message_without_double_quotes)

				# Translate the modified message
				translated_message = GoogleTranslator(source=language, target='en').translate(message_without_quotes)

				# Replace the placeholders with the original text within quotes
				for double_quoted_text in double_quoted_texts:
					translated_message = translated_message.replace(f'"{double_placeholder}"',
																	f'"{double_quoted_text}"', 1)

				for single_quoted_text in single_quoted_texts:
					translated_message = translated_message.replace(f"'{single_placeholder}'",
																	f"'{single_quoted_text}'", 1)

				if translated_message.lower() != message.lower():
					logger('success', "The message was translated")
				else:
					logger('alert', "The message stays untranslated")

				result = translated_message

			except:
				logger('error',
					   "Could not translate the message! Maybe some connection error, or something related to GoogleTranslator")
				raise Exception(
					'Could not translate the message! Maybe some connection error, or something related to GoogleTranslator')

		else:
			result = message

		return result

	def translate_output(self, message, language):
		if not self.bypass_translator:
			try:
				logger('info', f"Translating output information: {message}")

				# Identify text within double quotes using regular expressions
				double_quoted_texts = re.findall(r'"([^"]*)"', message)

				# Identify text within single quotes using regular expressions
				single_quoted_texts = re.findall(r"'([^']*)'", message)

				# Replace text within double quotes with a placeholder
				double_placeholder = 'DOUBLE_QUOTED_TEXT_PLACEHOLDER'
				message_without_double_quotes = re.sub(r'"([^"]*)"', f'"{double_placeholder}"', message)

				# Replace text within single quotes with a placeholder
				single_placeholder = 'SINGLE_QUOTED_TEXT_PLACEHOLDER'
				message_without_quotes = re.sub(r"'([^']*)'", f"'{single_placeholder}'", message_without_double_quotes)

				# Translate the modified message
				translated_message = GoogleTranslator(source='en', target=language).translate(message_without_quotes)

				# Replace the placeholders with the original text within quotes
				for double_quoted_text in double_quoted_texts:
					translated_message = translated_message.replace(f'"{double_placeholder}"',
																	f'"{double_quoted_text}"', 1)

				for single_quoted_text in single_quoted_texts:
					translated_message = translated_message.replace(f"'{single_placeholder}'",
																	f"'{single_quoted_text}'", 1)

				if translated_message.lower() != message.lower():
					logger('success', "The outgoing message was translated")
				else:
					logger('alert', "The outgoing message stays untranslated")

				result = translated_message

			except:
				logger('error',
					   "Could not translate the message! Maybe some connection error, or something related to GoogleTranslator")
				raise Exception(
					'Could not translate the message! Maybe some connection error, or something related to GoogleTranslator')

		else:
			result = message

		return result

	def hang_on_function(self):
		conversations = []
		self._cache = []

		def delete_message(wpp_contact_title):
			actionChains = ActionChains(self._b)
			if wpp_contact_title:
				current_contact = self._b.find_element(By.XPATH, f"//span[@dir='auto' and @title='{wpp_contact_title}']")
				actionChains.context_click(current_contact).perform()
				try:
					delete_conversation_button = WebDriverWait(self._b, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, """//*[@id="app"]/div/span[4]/div/ul/div/li[3]""")))
					sleep(0.5)
					delete_conversation_button.click()
					confirm_button = WebDriverWait(self._b, 10).until(expected_conditions.visibility_of_element_located((By.XPATH, "//button[@class='emrlamx0 aiput80m h1a80dm5 sta02ykp g0rxnol2 l7jjieqr hnx8ox4h f8jlpxt4 l1l4so3b le5p0ye3 m2gb0jvt rfxpxord gwd8mfxi mnh9o63b qmy7ya1v dcuuyf4k swfxs4et bgr8sfoe a6r886iw fx1ldmn8 orxa12fk bkifpc9x rpz5dbxo bn27j4ou oixtjehm hjo1mxmu snayiamo szmswy5k']")))
					sleep(0.2)
					confirm_button.click()

				except TimeoutException:
					pass

		def read_conversation(wpp_contact_title):
			logger('conversation', f"Reading {wpp_contact_title} conversation")
			_today_messages_elements = self._b.find_elements(By.XPATH, "//div[@tabindex='-1' and @class='n5hs2j7m oq31bsqd gx1rr48f qh5tioqs']//div[@role='row']//div[contains(@class,'CzM4m _2zFLj') and contains(@data-id, 'false_')]")

			if len(_today_messages_elements):
				_last_message = _today_messages_elements[-1].get_attribute('data-id')

				if _last_message not in [_already_processed_message['msg_id'] for _already_processed_message in self._cache]:

					data_ids_to_exclude = [msg['msg_id'] for msg in self.wpp_db.query({"wpp_contact_title": wpp_contact_title})]

					
					not_processed_messages_ids = [message.get_attribute('data-id') for message in _today_messages_elements if message.get_attribute('data-id') not in data_ids_to_exclude]

					
					if len(not_processed_messages_ids):
						logger('info', 'Validating if message is already processed')

						for not_processed_id in not_processed_messages_ids:

							self._cache.append(not_processed_id)

							
							print('not_processed_incoming_message_text')

							not_processed_ = self._b.find_element(By.XPATH, f"//div[@data-id='{not_processed_id}']//span[@dir='ltr']//span")

							
							not_processed_incoming_message_text = not_processed_.text
							

							_doc = {'msg_id': str(not_processed_id), 'wpp_contact_title': str(wpp_contact_title)}

							
							if self.wpp_db.add(_doc):
								logger('info', f'Processing message: id {not_processed_id}, contact {wpp_contact_title}, message {not_processed_incoming_message_text}')

								user = self.user_db.query(selector={"wpp_contact_title": wpp_contact_title})
								
								if user is None:
									user = UserRequestModel()
									user.language = self.get_lang_from_country_code(wpp_contact_title)
									user.wpp_contact_title = wpp_contact_title
									_user_dict = user.model_dump()
									user.id = str(self.user_db.add(_user_dict)['_id'])
								else:
									user["id"] = str(user["_id"])
									user = UserRequestModel(**user)

								processable_text = self.translate_input(message=not_processed_incoming_message_text, language=user.language)

								try:
									processable_text, quoted_content = extract_and_remove_quoted_content(processable_text)
								except:
									quoted_content = []

								ic(user)
								if user.is_human_attendance:
									
									try:

										_pipeline_attendant_waiting_for_response = [
											{
												'$match': {"$and": [{"client_id": ObjectId(str(user.get_id()))},
													  {"responser_id": {'$exists': True}}]}
											},
											{
										        '$sort': {
										            'creation_date': 1
										        }
										    }
										]

										_agg = self.notification_db.collection.aggregate(_pipeline_attendant_waiting_for_response)

										_current_protocol = next(_agg)

										_current_attendant = self.user_db.query({"_id": ObjectId(_current_protocol['responser_id'])})

										_attendant_request = NewRequest(
											message='',
											wpp_contact_title=_current_attendant['wpp_contact_title']
										)

										_requester_title = wpp_contact_title

										if user.name is not None:
											_requester_title += f" - {user.name}"

										_attendant_request_content = f"Protocol: \n{str(_current_protocol['_id'])}\n[{_requester_title}] "

										_attendant_request_content += f"{not_processed_incoming_message_text}"

										_attendant_request.skill.result = _attendant_request_content

										self.send_message(_attendant_request)

									except:
										ic('excpeption')
										self.user_db.update({"_id": ObjectId(user.id)}, {"is_human_attendance": False})
										user.is_human_attendance = False

								if not user.is_human_attendance:

									_brainiac_request = NewRequest(
										message=processable_text,
										wpp_contact_title=wpp_contact_title,
										user=user
									)
									
									_brainiac_request.quoted_content = quoted_content
									_brainiac_request.last_subject = user.last_subject

									try:

										_brainiac_request.skill.result = self.brainiac.process_message(
											_brainiac_request
										)

									except Unauthorized as er:

										print("Raised Unauthorized")

										_brainiac_request.skill.result = str(er)

									except (InvalidOption, Error) as er:

										print("Raised InvalidOption")

										if user.last_subject and user.last_subject is not None:
											processable_text += f"\n{str(user.last_subject)}"

											_brainiac_request = NewRequest(
												message=processable_text,
												wpp_contact_title=wpp_contact_title,
												user=user,
												quoted_content=quoted_content
											)

											_brainiac_request.skill.result = self.brainiac.process_message(
												_brainiac_request
											)

										else:
											_brainiac_request.skill.result = str(er)

									_brainiac_request.skill.result = self.translate_output(_brainiac_request.skill.result, user.language)

									self.send_message(_brainiac_request)

		try:
			load_side_bar = WebDriverWait(self._b, 10).until(
				expected_conditions.presence_of_element_located((By.CLASS_NAME, "lhggkp7q.ln8gz9je.rx9719la"))
			)
		except:
			load_side_bar = False

		if load_side_bar:
			try:
				WebDriverWait(self._b, 0.5).until(
					expected_conditions.presence_of_element_located((By.CLASS_NAME, "_199zF._3j691._1KV7I"))
				)
				conversations = self._b.find_elements(By.CLASS_NAME, "_199zF._3j691._1KV7I")
			except:
				# logger('conversation', "No new messages. Waiting...")
				pass

			if conversations:
				for conversation in conversations:
					conversation.click()
					wpp_contact_title = self.get_selected_conversation()
					logger('info', f"New BrainiacRequest Received from {wpp_contact_title}")
					read_conversation(wpp_contact_title)

			else:
				# logger('conversation', "No new messages, searching for old ones that are not processed.")
				old_conversations = self._b.find_elements(By.XPATH, "//div[@class='_199zF _3j691']")

				sleep(100)
				for each_conversation in old_conversations:
					try:
						each_conversation.click()
						read_conversation(self.get_selected_conversation(old=True))
					except:
						pass

			self.verify_notifications()

		else:
			# logger('conversation', "No available conversations to hang on, as soon you receive a message, I will be working on!")
			pass

	def infinity_loop(self):
		while self.is_browser_enabled():
			self.hang_on_function()

		if not self.is_browser_enabled():
			self.restart()

	def restart(self, ):
		logger('alert', 'Browser must be reinitialized')
		sleep(60)

		if not self.is_browser_enabled():
			self.browser()
			logger('success', "Browser Restarted Successfully")

		if self.is_browser_enabled():
			self.connect()
			logger('success', "Whatsapp Connected Successfully")
			self.hang_on()

		while not self.is_browser_enabled():
			try:
				WebDriverWait(self._b, 2000)
			except Exception as e:
				self.restart()

		if self.is_browser_enabled():
			self.infinity_loop()

	def hang_on(self):

		# if self._first_state:
		# 	self._b.close()
		# 	self.driver_options.add_argument("--headless=new")
		# 	self._b = self.browser()
		# 	sleep(5)
		# 	self._first_state = False

		while True:
			try:
				sleep(2)
				self.infinity_loop()
				logger('fatal-error', 'Hang on loop unexpectedly quit')

			except WebDriverException:
				pass

	def start(self):

		try:
			logger('start', 'Initializing')
			sleep(5)
			self.browser()
			logger('info', "Prompting for Whatsapp Connection")
			self.connect()
			logger('success', "Whatsapp Connected!")
			self.hang_on()

		except WebDriverException or NoSuchWindowException:
			self.restart()

