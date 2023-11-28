from dotenv import load_dotenv
import json
from typing import Dict
import ast
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.generic_crud import GenericCRUD
from .api_limit import (
    DEVELOPER_EMAIL,
    API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
    API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME)

api_management_local_python_code = {
    "component_id": API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
    "component_name": API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME,
    "component_category": LoggerComponentEnum.ComponentCategory.Code.value,
    "developer_email": DEVELOPER_EMAIL,
}
load_dotenv()

logger = Logger.create_logger(object=api_management_local_python_code)


class APICallsLocal(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(schema_name="api_call", default_table_name="api_call_table")

    @staticmethod
    def _insert_api_call_dict(api_call_data_dict: dict) -> int:
        if api_call_data_dict['is_network'] is None:
            api_call_data_dict['is_network'] = "null"
        logger.start(object={"api_call_data_dict ": api_call_data_dict})
        try:
            api_local=APICallsLocal()
            api_call_id = api_local.insert(json_data=api_call_data_dict)
            logger.end()
            return api_call_id
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            raise exception
