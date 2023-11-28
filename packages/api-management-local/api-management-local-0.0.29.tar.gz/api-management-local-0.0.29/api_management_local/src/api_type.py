from dotenv import load_dotenv
import json

from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.generic_crud import GenericCRUD
from user_context_remote.user_context import UserContext
from circles_local_database_python.connector import Connector
from src.Exception_API import ApiTypeDisabledException,ApiTypeIsNotExistException,NotEnoughStarsForActivityException,PassedTheHardLimitException


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

class ApiType():
    
    def get_action_id_by_api_type_id(api_type_id:int)->int:
        connection = Connector.connect("api_type")
        cursor = connection.cursor()
        query = f"""SELECT action_id FROM api_type.api_type_table WHERE  api_type_id=%s AND is_enabled=TRUE"""
        cursor.execute(query, (api_type_id,))
        action_id=cursor.fetchone()
        if action_id is None:
            query = f"""SELECT action_id FROM api_type.api_type_table WHERE  api_type_id=%s """
            cursor.execute(query, (api_type_id,))
            action_id=cursor.fetchone()
            if action_id is None:
                raise ApiTypeIsNotExistException
            else:
                raise ApiTypeDisabledException
            
        
        return action_id[0]