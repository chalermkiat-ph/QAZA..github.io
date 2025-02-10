import json
from databases import Databases

from fastapi import APIRouter, status, HTTPException
from ..helpers.http_exception import HttpException
from ..dtos.personal_dto import PersonalDto

DatabaseConfig = {}

router = APIRouter(
    prefix='/personal',
    tags=['personal'],
    responses={404: {"description": "Not found"}},
)


# public

@router.post('/getPersonalByCriteria', status_code=status.HTTP_200_OK)
def get_personal_by_criteria(criteria: dict):

    return __get_personal_by_criteria(criteria)

@router.get('/getAllPersonal', status_code=status.HTTP_200_OK)
def get_all_personal():

    return __get_all_personal()


@router.post('/createPersonal', status_code=status.HTTP_201_CREATED)
def create_personal(request: PersonalDto):
    __validate_personal_dto(request)

    return __create_personal(request)


@router.delete('/deletePersonalById', status_code=status.HTTP_200_OK)
def delete_personal_by_id(id: str):

    return __delete_personal_by_id(id)


# private

def __get_personal_by_criteria(criteria):
    context = __connect_database(DatabaseConfig)
    result = __get_data_by_criteria(context, criteria)

    return {
        "status": True,
        "count": len(result),
        "data": result,
        "description": "ok"
    }

def __delete_personal_by_id(id):
    context = __connect_database(DatabaseConfig)    
    result = __delete_by_id(context, id)
    # TODO: Validate after delete 

    return {
        "status": True,
        "data": id,
        "description": "ok"
    }


def __get_all_personal():
    context = __connect_database(DatabaseConfig)
    result = __get_all(context)

    return {
        "status": True,
        "data": result,
        "description": "ok"
    }


def __create_personal(request):
    context = __connect_database(DatabaseConfig)
    data = json.loads(request.json())
    __insert_data(context, data)

    return {
        "status": True,
        "data": request,
        "description": "ok"
    }


# error handling

def __delete_by_id(context, id):

    return context.delete_data_by_id(id)

def __get_data_by_criteria(context, criteria):

    return context.get_data_by_criteria(criteria)

def __get_all(context):

    return context.get_all_data()


@HttpException.insert_data_handling
def __insert_data(context, data):
    context.insert_data(data)


@HttpException.connect_database_handling
def __connect_database(databaseConfig):

    return Databases(databaseConfig)


def __validate_personal_dto(request):
    # validation model
    try:
        request.json()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Invalid json body : {e}")

    # if len(request.postman_test_suites) == 0:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                         detail="Please input attribute 'postman_test_suites'")
    #
    # for postman_test_suite in request.postman_test_suites:
    #     if len(postman_test_suite.postman_test_cases) == 0:
    #         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
    #                             detail="Please input attribute 'postman_test_cases'")
