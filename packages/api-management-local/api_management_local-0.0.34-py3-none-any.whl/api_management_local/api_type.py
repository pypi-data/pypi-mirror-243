import os
import sys
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
from dotenv import load_dotenv
import json

from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.generic_crud import GenericCRUD
from user_context_remote.user_context import UserContext
from circles_local_database_python.connector import Connector
from .exception_API import ApiTypeDisabledException,ApiTypeIsNotExistException,NotEnoughStarsForActivityException,PassedTheHardLimitException


API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID = 212
API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME = "api-management-local-python-package"
DEVELOPER_EMAIL = "heba.a@circ.zone"

api_management_local_python_code = {
    'component_id': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
load_dotenv()

logger = Logger.create_logger(object=api_management_local_python_code)

class ApiType(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(default_schema_name="api_type", default_table_name="api_type_view")
    
    @staticmethod
    def get_action_id_by_api_type_id(api_type_id:int)->int:
        api_type=ApiType()
        select_clause = "action_id"
        where = "api_type_id = {} AND is_enabled = TRUE".format(api_type_id)
        action_id = api_type.select_one_tuple_by_where(
                view_table_name="api_type_view", select_clause_value=select_clause, where=where)
        if action_id is None:
            select_clause = "action_id"
            where = "api_type_id = {}".format(api_type_id)
            api_type=ApiType()
            action_id = api_type.select_one_tuple_by_where(
                view_table_name="api_type_view", select_clause_value=select_clause, where=where)
            if action_id is None:
                raise ApiTypeIsNotExistException
            else:
                raise ApiTypeDisabledException
            
        
        return action_id[0]