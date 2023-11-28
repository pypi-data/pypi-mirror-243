from dotenv import load_dotenv
import json

from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.generic_crud import GenericCRUD
from .external_user_id import get_extenal_user_id_by_api_type_id
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


class APILimitsLocal(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(schema_name="api_limit", default_table_name="api_limit_view")
    
    @staticmethod
    def get_api_limit_by_api_type_id_external_user_id( api_type_id: int, external_user_id: int) -> list:
        logger.start(object={'api_type_id': api_type_id,
                     'external_user_id': external_user_id})
        try:
            select_clause = "soft_limit_value,soft_limit_unit,hard_limit_value,hard_limit_unit"
            where = "api_type_id = {} AND external_user_id = {}".format(
                api_type_id, external_user_id)
            api_limit=APILimitsLocal()
            api_limit_result = api_limit.select_one_tuple_by_where(
                view_table_name="api_limit_view", select_clause_value=select_clause, where=where)
            logger.end(object={'api_limit_result': str(api_limit_result)})
            return api_limit_result
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
