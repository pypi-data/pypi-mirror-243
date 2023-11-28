from typing import List

from bson import ObjectId
from fastapi.responses import JSONResponse

from elemental_tools.scriptize.api.controllers.notification import NotificationController

from elemental_tools.scriptize.api.config import logger

from fastapi import HTTPException
from fastapi.routing import APIRouter
from elemental_tools.scriptize.api.models.notification import NotificationRequestModel

from pymongo.errors import DuplicateKeyError

router = APIRouter()

notification_controller = NotificationController()


@router.post("/notification/add", tags=['Notification'])
def notification_add(body: NotificationRequestModel):
    try:
        result = notification_controller.add(body)

        _inserted_id = result['_id']
    except DuplicateKeyError as d:
        logger('error', f'Failed to store notification because of exception: {str(d)}')
        raise HTTPException(detail='An notification with this wpp_contact_title already exists', status_code=403)

    return JSONResponse(content=dict(uid=str(_inserted_id)), status_code=200)


@router.put("/notification/edit", tags=['Notification'])
def notification_edit(uid: str, body: NotificationRequestModel):
    try:
        result = notification_controller.update({'_id': ObjectId(uid)}, body.model_dump())

    except:
        raise HTTPException(detail='Cannot edit notification', status_code=500)

    return JSONResponse(content=result, status_code=200)


@router.get("/notification", tags=['Notification'])
def notification_get(wpp_contact_title: str):
    try:
        result = notification_controller.query({'wpp_contact_title': {"$eq": wpp_contact_title}})
        result['_id'] = str(ObjectId(result['_id']))
        if result is None:
             return JSONResponse(content={'message': 'Cannot find notification', 'model': NotificationRequestModel().__dict__}, status_code=404)
    except:
        raise HTTPException(detail='Cannot query notification', status_code=500)

    return JSONResponse(content=result, status_code=200)

