from fastapi.responses import JSONResponse
from elemental_tools.scriptize.api.controllers.statement import StatementController
from fastapi import HTTPException
from fastapi.routing import APIRouter

router = APIRouter()


from elemental_tools.scriptize.api.models import StatementRequestModel


# @router.post("/statement/add", tags=['Statement'])
# def statement_add(body: UserRequestModel):
# 	try:
# 		logger('info', f'API received the doc: {str(body.__dict__)}')
# 		statement_db = StatementDB()
#
# 		result = statement_db.add(body.__dict__)
# 		if not result:
# 			raise HTTPException(detail='An user with this wpp_contact_title already exists', status_code=403)
# 		elif result is None:
# 			raise HTTPException(detail='An exception was thrown when trying to add a user.', status_code=500)
# 	except:
# 		raise HTTPException(detail='Cannot add user', status_code=500)
#
# 	return JSONResponse(content=dict(result), status_code=200)
#
#
# @router.put("/statement/edit", tags=['Statement'])
# def statement_edit(body: UserRequestModel):
# 	try:
# 		result = statement_db.update(body.__dict__)
# 	except:
# 		raise HTTPException(detail='Cannot edit user', status_code=500)
#
# 	return JSONResponse(content=result, status_code=200)


@router.get("/statement", tags=['Statement'])
def statement_get(uid: str, date: str, institution=None):
	try:
		statement_db = StatementController(uid=uid, institution=institution)

		result = statement_db.retrieve_statement()

		if result is None:
			return JSONResponse(content={'message': 'Cannot find user', 'model': StatementRequestModel().__dict__}, status_code=404)
	except:
		raise HTTPException(detail='Cannot query user', status_code=500)

	return JSONResponse(content=result, status_code=200)

