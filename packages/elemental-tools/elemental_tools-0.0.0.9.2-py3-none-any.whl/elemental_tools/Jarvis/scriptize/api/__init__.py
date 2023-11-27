import json

import uvicorn
from bson import ObjectId
from pydantic import field_validator, BaseModel, Field

from fastapi import FastAPI, HTTPException, Query
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse
from fastapi.requests import Request

from typing import Union, Optional
from datetime import datetime

from elemental_tools.Jarvis.scriptize.api import constants as Constants
from elemental_tools.Jarvis.scriptize.api.config import logger
from elemental_tools.Jarvis.scriptize.api.controllers.user import UserController
from elemental_tools.Jarvis.scriptize.pydantic_tools import generate_script_information_from_pydantic_models
from elemental_tools.Jarvis.scriptize.api.endpoints.user import router as user_endpoints
from elemental_tools.Jarvis.scriptize.api.endpoints.institution import router as institution_endpoints
from elemental_tools.Jarvis.scriptize.api.endpoints.notification import router as notification_endpoints
from elemental_tools.Jarvis.scriptize.exceptions import ParameterMissing
from elemental_tools.Jarvis.scriptize.api.controllers import TaskController
from elemental_tools.Jarvis.scriptize.pydantic_tools.config import default_arguments

router = APIRouter()


class Api(FastAPI):
	script_pydantic_models = None

	def __init__(self, title: str = "", endpoints=None, log_path: str = None, script_pydantic_models=None):
		super().__init__()
		self.logger = logger

		self.include_router(user_endpoints)
		self.include_router(institution_endpoints)
		self.include_router(notification_endpoints)

		if endpoints is not None:
			self.include_router(**user_endpoints)

		if script_pydantic_models is not None:
			_user_controller = UserController()
			_task_controller = TaskController()
			scripts_information = generate_script_information_from_pydantic_models(script_pydantic_models)

			script_router = APIRouter()

			# Endpoint to schedule tasks
			class TaskRequestModel(BaseModel):
				description: str = Field(examples=['ras'],
									   description='Name of the folder where the script you are running is stored')
				timer: int = Field(examples=[10, 30, 1000], default=None,
								   description='A milliseconds timer (ms) for task execution loop, if no timer is specified the task will be executed immediately or by the schedule date if provided.')
				schedule_date: Union[datetime, None] = Field(examples=[str(datetime.now().isoformat())],
															 description='A timestamp to schedule task execution if no schedule_date is specified, task will be executed immediately or by the timer if provided',
															 default=None)
				loops: Union[int, None] = Field(examples=[0, 1, 10000, None], default=None,
								   description='A loop counter for the task execution, if no loops were provided the task will be executed immediately infinitely')
				task_name: str = Field(examples=['ras'],
									   description='Name of the folder where the script you are running is stored')
				parameters: dict = Field(examples=[{'current_script_param': 'current_execution_argument'}],
										 description='A dictionary to store the execution arguments, such as passwords, usernames, and so on... They must have the correct type on your start method at the main.py of each script folder located at the scripts directory.')
				uid: str = Field(examples=["User id"], description='A loop counter for the task execution, if no loops were provided the task will be executed immediately infinitely')
				status: bool = Field(examples=[True, False], default=False)

				_entrypoint: str

				@field_validator("schedule_date")
				def future_date_validator(cls, value):
					if value is not None:
						if value <= datetime.now():
							raise ValueError("schedule_date must be a future date and time")
						return value
					else:
						pass

				@field_validator("task_name")
				def task_name_validator(cls, name):
					cls._entrypoint = script_pydantic_models[name]
					cls.parameters = script_pydantic_models[name]
					return name

				def get_entrypoint(self):
					return self._entrypoint

			def instant_run(func, args):

				def execute_function(func, args: dict = None):
					# process no arguments scripts
					if args is None:
						return func()

					# process keyword arguments and not keyword arguments
					try:
						result = func(**args)
					except TypeError:
						try:
							result = func(*args.values())
						except TypeError as e:
							raise ParameterMissing(str(e))

					return result

				try:
					result = execute_function(func, args)
					return result
				except ParameterMissing as e:
					raise HTTPException(detail=str(e), status_code=500)

			@script_router.post("/tasks/add", tags=['Scripts/Tasks'])
			def schedule_task(body: TaskRequestModel, run_test: bool = False):
				response = {"message": "Task processed successfully!"}

				logger('info', f"Searching for tasks by name: {body.task_name} in {script_pydantic_models}")

				# Store task data
				if body.task_name in script_pydantic_models.keys():
					logger('info', f"Task {body.task_name} found in dict: {str(script_pydantic_models.keys())}")
					if body.timer is None or run_test:
						response['execution_result'] = instant_run(script_pydantic_models[body.task_name]['function'],
																   body.parameters)
						if not run_test:
							return JSONResponse(content=str(response), status_code=200)

					try:
						_uid = ObjectId(body.uid)
					except:
						raise HTTPException(detail="uid is invalid", status_code=500)

					_user = _user_controller.query({"_id": _uid})

					if _user:

						_insert_result = _task_controller.add(body)

						if _insert_result:
							return JSONResponse(content={"id": str(_insert_result)}, status_code=200)
						else:
							raise HTTPException(detail='Cannot save task schedule', status_code=500)

					raise HTTPException(detail='uid not found', status_code=400)

				else:
					raise HTTPException(detail='Task Not Found', status_code=404)

			# Endpoint to list available tasks
			@script_router.get("/tasks/list", tags=['Scripts/Tasks'])
			def list_tasks():
				return scripts_information

			self.include_router(script_router)


run = uvicorn.run

