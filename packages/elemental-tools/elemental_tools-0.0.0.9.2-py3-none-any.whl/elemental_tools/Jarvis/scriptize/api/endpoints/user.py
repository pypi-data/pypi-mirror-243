from typing import List

from bson import ObjectId
from fastapi.responses import JSONResponse
from elemental_tools.Jarvis.scriptize.api.controllers.user import UserController
from elemental_tools.Jarvis.scriptize.api.controllers.institution import InstitutionController
from elemental_tools.Jarvis.scriptize.api.config import logger
from fastapi import HTTPException
from fastapi.routing import APIRouter
from elemental_tools.Jarvis.scriptize.api.models import UserRequestModel, UserInstitutionSetting
import json
from pymongo.errors import DuplicateKeyError

router = APIRouter()

user_controller = UserController()
institution_controller = InstitutionController()


@router.post("/user/add", tags=['User'])
def user_add(body: UserRequestModel):
    try:
        for inst in body.institutions:
            try:
                _this_inst = institution_controller.query({'_id': ObjectId(inst.institution_id)})

                if _this_inst is None:
                    raise HTTPException(detail='Unavailable institution, please check the available institutions at /institutions endpoint.', status_code=404)
            except:
                raise HTTPException(
                    detail='Unavailable institution, please check the available institutions at /institutions endpoint.',
                    status_code=404)

        result = user_controller.add(body.model_dump())

        _inserted_id = result['_id']
    except DuplicateKeyError as d:
        logger('error', f'Failed to store user because of exception: {str(d)}')
        raise HTTPException(detail='An user with this wpp_contact_title already exists', status_code=403)

    return JSONResponse(content=dict(uid=str(_inserted_id)), status_code=200)


@router.put("/user/edit", tags=['User'])
def user_edit(uid: str, body: UserRequestModel):
    try:

        for inst in body.institutions:
            _this_inst = institution_controller.query({'_id': ObjectId(inst['_id'])})

            if _this_inst is None:
                raise HTTPException(
                    detail='Unavailable institution, please check the available institutions at /institutions endpoint.',
                    status_code=404)

        result = user_controller.update({'_id': ObjectId(uid)}, body.model_dump())
    except:
        raise HTTPException(detail='Cannot edit user', status_code=500)

    return JSONResponse(content=result, status_code=200)


@router.patch("/user/institutions", tags=['User'], description="To add institutions to a user")
def user_edit(uid: str, body: List[UserInstitutionSetting]):
    try:

        for inst_to_add in body:

            _this_inst = institution_controller.query({'_id': ObjectId(inst_to_add.institution_id)})

            if _this_inst is None:
                raise HTTPException(
                    detail='Unavailable institution, please check the available institutions at /institutions endpoint.',
                    status_code=404)

        _new_user_institutions = [e.model_dump() for e in body]
        _new_user_institutions_ids = [inst['institution_id'] for inst in _new_user_institutions]

        _current_user_institutions = user_controller.query({'_id': ObjectId(uid)}).get('institutions', [])

        _merge_user_institutions = [c_i for c_i in _current_user_institutions if c_i['institution_id'] not in _new_user_institutions_ids] + _new_user_institutions

        result = user_controller.update({'_id': ObjectId(uid)}, {"institutions": _merge_user_institutions})

    except Exception as e:
        raise HTTPException(detail=f'Cannot edit user because of {str(e)}', status_code=500)

    return JSONResponse(content={'count': result.modified_count}, status_code=200)


@router.get("/user", tags=['User'])
def user_get(wpp_contact_title: str):
    try:
        result = user_controller.query({'wpp_contact_title': {"$eq": wpp_contact_title}})
        result['_id'] = str(ObjectId(result['_id']))
        if result is None:
             return JSONResponse(content={'message': 'Cannot find user', 'model': UserRequestModel().__dict__}, status_code=404)
    except:
        raise HTTPException(detail='Cannot query user', status_code=500)

    return JSONResponse(content=result, status_code=200)