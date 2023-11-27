from datetime import datetime
from typing import Optional, Union, List, Dict

from bson import ObjectId
from fastapi import HTTPException


from pydantic import field_validator, Field, Extra, PrivateAttr
from pydantic import BaseModel

from fastapi import HTTPException


class GooglePermission(BaseModel, extra='allow'):

    uid: str = Field(description='Ids of the user that is gaining access to this doc', default=None)
    email: str = Field(description='The current email assigned to the permission of this uid. For later updates.', default=None)
    date: str = Field(description='A timestamp for the changes made to the doc', default=datetime.now().isoformat())


class GoogleDriveFolder(BaseModel, extra='allow'):

    folder_caption: str = Field(description='A string containing the Google Drive folder caption identifier', default=None)
    external_id: Union[str, None] = Field(description='Save the id for the current sheet', default=None)
    permissions: Union[list, None] = Field(description='A list containing the ids and emails of the users that already have access to this sheet', default=[])


class GoogleSheet(BaseModel, extra='allow'):

    name: Union[str, None] = Field(description='A name for the sheet to ease identification', default=None)
    external_id: Union[str, None] = Field(description='Id for the current sheet', default=None)
    date: str = Field(description='A timestamp for the changes made to the doc', default=datetime.now().isoformat())
    authorized_emails: list = Field(description='A list with the emails of the persons who can see this sheet.', default=[])


class GoogleInformation(BaseModel, extra='allow'):

    sheets: Dict[str, GoogleSheet] = Field(description='Store the Year and the Id for each Google Sheet Already Created.', default={})
    sheets_permissions: list = Field(description='Save email list with the permissions to the sheets', default=[])
    drive: Dict[str, GoogleDriveFolder] = Field(description='Keeps ids for the folders where the user information is stored.', default={})


class UserInstitutionSetting(BaseModel, extra='allow'):

    status: Union[bool, None] = Field(examples=[True, False], description='A boolean indicating whether the institution integration will be enabled', default=True)

    institution_id: str = Field(examples=['4a5s6d4a8s789as4d56asd12'], description='A stringed object id obtained using the institution endpoint')

    email: str = Field(description='Email for the user account on the current institution website')

    password: str = Field(description='Password for the user account on the current institution website')

    last_sync: str = Field(description='Timestamp for the last synchronization to this institution', default=datetime.now().isoformat())


class UserRequestModel(BaseModel, extra='allow'):
    name: Union[str, None] = Field(description='Username', default=None)
    email: Union[str, None] = Field(description='User email for google drive sharing and other stuff', default=None)
    wpp_contact_title: Union[str, None] = Field(description='Whatsapp contact title', default=None)
    wpp_user_id: Union[str, None] = Field(description='Whatsapp user id', default=None)
    status: Union[bool, None] = Field(description='User status', default=False)
    admin: Union[bool, None] = Field(description='Set if a user has admin privileges', default=False)
    tax: float = Field(description='Set tax for user transactions', default=0.0065)
    language: str = Field(description='Language for message translation', default='pt')
    is_human_attendance: bool = Field(description='Indicates whenever the user is under attendance by a human being.', default=False)
    last_subject: Union[str, None] = Field(description='Indicates the latest subject threaded with the chat', default="")
    _last_update: str = PrivateAttr(
        default='')

    google_sync: bool = Field(description='Activate the google statement synchronization for the current user', default=False)

    institutions: List[UserInstitutionSetting] = Field(examples=[[UserInstitutionSetting(**{"status":True, "institution_id": "4a5s6d4a8s789as4d56asd12", "email": "a@b.com", "password": "123456"})]], description='Store the user information for the institutions to be integrated', default=[])

    google: Union[GoogleInformation, None] = Field(default=GoogleInformation())

    @field_validator('wpp_contact_title')
    def validate_wpp_contact(cls, contact):
        if contact is not None:
            cls.last_update = datetime.now().isoformat()
            return contact
        else:
            raise HTTPException(detail='Invalid wpp contact.', status_code=500)

    def get_id(self):
        """

        :return: The hidden element _id as ObjectId
        :type: ObjectId
        """

        return self._id

    def get_google(self):
        return self.google


class StatementRequestModel(BaseModel, extra='allow'):
    uid: str = Field(description='User id for the current statement registration', default=None)
    status: bool = Field(description='User status', default=False)
    admin: bool = Field(description='Set if a user has admin privileges', default=False)
    tax: float = Field(description='Set tax for user transactions', default=0.0065)
    language: str = Field(description='Language for message translation', default='pt')
    last_update: str = Field(
        description='A date time that will be defined automatically whenever the document changes',
        default=datetime.now())


class SheetStyle(BaseModel, extra='allow'):
    background: str
    color: str


class InstitutionRequestModel(BaseModel, extra='allow'):
    tax_number: str = Field(description='Institution tax number known as CNPJ in Brazil')
    name: str = Field(description='Institution name', default=None)
    alias: str = Field(description='The name that will be used in user sheets')
    status: bool = Field(description='Institution status', default=False)
    website: str = Field(description='Website of the current institution', default=None)

    style: SheetStyle = Field(description='Save the style of the current institution', examples=[{'background': "#000000", 'color': "#ffffff"}])

    last_update: str = Field(
        examples=[datetime.now().isoformat()],
        description='A date time that will be defined automatically whenever the document changes',
        default=datetime.now().isoformat()
    )

    def get_id(self):
        return str(self._id)


