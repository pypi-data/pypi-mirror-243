from time import sleep

from bson import ObjectId
from icecream import ic

from elemental_tools.logger import Logger

from elemental_tools.Jarvis.brainiac import NewRequest
from elemental_tools.Jarvis.brainiac import Brainiac

from elemental_tools.Jarvis.exceptions import Unauthorized, InvalidOption, Error

from elemental_tools.Jarvis.server.basic import Server
from elemental_tools.Jarvis.server.whatsapp.api import WhatsappOfficialAPI

from elemental_tools.Jarvis.scriptize.api.models import UserRequestModel
from elemental_tools.Jarvis.scriptize.api import UserController
from elemental_tools.Jarvis.scriptize.api.controllers.notification import NotificationController
from elemental_tools.Jarvis.scriptize.api.controllers.webhook import WebhookController
from elemental_tools.Jarvis.scriptize.api.controllers.wpp import WppController

from elemental_tools.Jarvis.config import log_path
from elemental_tools.Jarvis.tools import Tools, extract_and_remove_quoted_content


module_name = 'wpp-official-server'


class WhatsappOfficialServer(Server):
	logger = Logger(app_name='jarvis', owner=module_name, log_path=log_path).log

	wpp_db = WppController()
	notification_db = NotificationController()
	user_db = UserController()
	webhook_db = WebhookController()

	_cache = []
	tools = Tools()


	def __init__(self, brainiac: Brainiac, phone_number_id: str, token_wpp_api: str, timeout: float, bypass_translator: bool = False):
		self.timeout = timeout

		self.bypass_translator = bypass_translator

		self.brainiac = brainiac
		self.brainiac.bypass_translator = bypass_translator

		self.logger('info', f'Health Checking Wpp Official Server...')
		self.wpp_api = WhatsappOfficialAPI(phone_number_id, token_wpp_api)
		self.logger('info', f'Whatsapp phone connected is {self.wpp_api.health.phone_number}')
		self.logger('alert', f'Whatsapp code verification status is: {self.wpp_api.health.code_verification_status}')

		self.logger('info', f'Checking Webhook Database...')
		new_messages = self.webhook_db.get_unprocessed_wpp_messages()

		self._start()

	def send_message(self, request: NewRequest):
		destination_phone, message = request.wpp_contact_title, request.skill.result
		self.logger('info', f'Sending Message Destination: {str(destination_phone)} Message: {str(message)}')
		self.wpp_api.send_message(destination=destination_phone, message=str(message))
		self.logger('success', f"Message has been sent!")

	def _start(self, timeout=5):
		self.logger('start', f"Initializing Whatsapp Official Server with Brainiac!")

		while True:
			self.logger('info', f"Checking for new messages on your webhook...")
			new_messages = self.webhook_db.get_unprocessed_wpp_messages()
			_gen_list = list(new_messages)
			if len(_gen_list[0]):
				self.logger('info', f"New messages found! Processing...")

				for current_index, incoming_message in enumerate(_gen_list):
					ic(incoming_message)

					for message in incoming_message:
						user_ids = message.get('user_ids', [])
						messages = message.get('messages', [])

						for user_id, current_message in zip(user_ids, messages):
							wpp_user_id = user_id
							not_processed_id = current_message['id']
							incoming_phone = current_message['from']
							message_content = current_message['text']['body']

							_doc = {'msg_id': str(not_processed_id), 'wpp_contact_title': str(incoming_phone), 'wpp_user_id': str(wpp_user_id)}

							if self.wpp_db.add(_doc):
								self.logger('info', f'Processing message: id {not_processed_id}, contact {incoming_phone}, message {message_content}')
								user = self.user_db.query(selector={"wpp_user_id": wpp_user_id})

								if user is None:
									user = UserRequestModel()
									user.language = self.get_lang_from_country_code(incoming_phone)
									user.wpp_contact_title = incoming_phone
									user.wpp_user_id = str(wpp_user_id)
									_user_dict = user.model_dump()
									user.id = str(self.user_db.add(_user_dict)['_id'])
								else:
									user["id"] = str(user["_id"])
									user = UserRequestModel(**user)

								processable_text = self.translate_input(message=message_content,
																		language=user.language)

								try:
									processable_text, quoted_content = extract_and_remove_quoted_content(processable_text)
								except:
									quoted_content = []

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

										ic(_pipeline_attendant_waiting_for_response)

										_agg = self.notification_db.collection.aggregate(_pipeline_attendant_waiting_for_response)
										ic(_agg)

										_current_protocol = next(_agg)
										ic(_current_protocol)

										_current_attendant = self.user_db.query(
											{"_id": ObjectId(_current_protocol['responser_id'])})
										ic(_current_attendant)

										_attendant_request = NewRequest(
											message='',
											wpp_contact_title=_current_attendant['wpp_contact_title'],
											wpp_user_id=wpp_user_id
										)
										ic(_attendant_request)

										_requester_title = incoming_phone
										ic(_requester_title)

										if user.name is not None:
											_requester_title += f" - {user.name}"

										ic(_requester_title)
										_attendant_request_content = f"Protocol: \n{str(_current_protocol['_id'])}\n[{_requester_title}] "
										ic(_attendant_request_content)
										_attendant_request_content += f"{message_content}"
										ic(_attendant_request_content)
										_attendant_request.skill.result = _attendant_request_content
										ic(_attendant_request)
										self.send_message(_attendant_request)

									except:
										ic('exception')
										self.user_db.update({"_id": ObjectId(user.id)}, {"is_human_attendance": False})
										user.is_human_attendance = False

								if not user.is_human_attendance:

									_brainiac_request = NewRequest(
										message=processable_text,
										wpp_contact_title=incoming_phone,
										wpp_user_id=wpp_user_id,
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
												wpp_contact_title=incoming_phone,
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

					self.webhook_db.remove(incoming_message[current_index]['_id'])

			else:
				self.logger('alert', f"No new messages, skipping...")

			self.verify_notifications()
			sleep(self.timeout)

