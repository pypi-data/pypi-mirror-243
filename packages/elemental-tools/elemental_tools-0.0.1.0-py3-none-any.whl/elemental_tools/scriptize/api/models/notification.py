from datetime import datetime

from bson import ObjectId
from pydantic import BaseModel, Field, PrivateAttr
from typing import Optional, Union, List, Dict, Any


class NotificationRequestModel(BaseModel, extra='allow'):
	_id = PrivateAttr()
	creation_date: str = datetime.now().isoformat()
	role: Union[list, None] = Field(
		description='List of roles to notify. Check your admin to obtain more information about that.', default=None)
	status: Union[bool, None] = Field(description='Notification Status', default=False)
	content: Union[str, None] = Field(description='Notification Content', default=None)
	uid: Union[Any, None] = Field(description='Notification User', default=None)
	client_id: Union[Any, None] = Field(description='Notification Requester identifier', default=None)

	def get_id(self):
		return self._id

	def set_id(self, _id):
		self._id = ObjectId(_id)
		return self._id

