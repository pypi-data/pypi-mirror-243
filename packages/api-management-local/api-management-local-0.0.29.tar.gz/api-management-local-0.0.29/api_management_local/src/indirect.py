import sys
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..')) 
from dotenv import load_dotenv
import json
import http
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.generic_crud import GenericCRUD
from src.api_call import APICallsLocal
from src.external_user_id import get_extenal_user_id_by_api_type_id
from src.api_management_local import APIManagementsLocal
from url_local.url_circlez import OurUrl
from url_local import action_name_enum, entity_name_enum, component_name_enum
from src.api_limit import (DEVELOPER_EMAIL,
                        API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
                        API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME, APILimitsLocal)
from src.stars import StarsLocal
from src.api_type import ApiType
from sdk.src.validate import validate_enviroment_variables
BRAND_NAME = os.getenv('BRAND_NAME')
validate_enviroment_variables()
AUTHENTICATION_API_VERSION = 1

authentication_login_validate_jwt_url = OurUrl.endpoint_url(
    brand_name=BRAND_NAME,
    environment_name=os.getenv('ENVIRONMENT_NAME'),
    component_name=component_name_enum.ComponentName.AUTHENTICATION.value,
    entity_name=entity_name_enum.EntityName.AUTH_LOGIN.value,
    version=AUTHENTICATION_API_VERSION,
    action_name=action_name_enum.ActionName.VALIDATE_JWT.value
)
api_management_local_python_code = {
    'component_id': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
    'component_name': API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': DEVELOPER_EMAIL
}
load_dotenv()
logger = Logger.create_logger(object=api_management_local_python_code)


class InDirect(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(schema_name="api_call", default_table_name="api_call_table",
                         default_id_column_name="api_call_id")

    def before_call_api(self, external_user_id: int, api_type_id: int, endpoint: str, outgoing_body: str, outgoing_header: str):
        action_id=ApiType.get_action_id_by_api_type_id(api_type_id)
        StarsLocal._profile_star_before_action(action_id)
        APIManagementsLocal.sleep_per_interval(api_type_id)
        if external_user_id == None:
            external_user_id = get_extenal_user_id_by_api_type_id(api_type_id)
        arr, outgoing_body_significant_fields_hash = APIManagementsLocal.check_cache(
            api_type_id, outgoing_body)
        if arr == None:
            is_network = None
            limit = APIManagementsLocal.check_limit(
                external_user_id=external_user_id, api_type_id=api_type_id)
        else:
            limit = None
            is_network = 0

        api_call_data_dict = {'api_type_id': api_type_id, 'external_user_id': external_user_id,
                              'endpoint': endpoint, 'outgoing_header': str(outgoing_header), 'outgoing_body': str(outgoing_body),
                              'outgoing_body_significant_fields_hash': outgoing_body_significant_fields_hash,
                              'is_network': is_network
                              }
        api_call_id = APICallsLocal._insert_api_call_dict(
            api_call_data_dict=api_call_data_dict)

        return limit, api_call_id, arr

    def after_call_api(self, external_user_id: int, api_type_id: int, endpoint: str, outgoing_body: str, outgoing_header: str, http_status_code: int, response_body: str, incoming_message: str, api_call_id: int, used_cache: bool):
        if http.HTTPStatus.OK == http_status_code:
            StarsLocal._api_executed(api_type_id=api_type_id)
        if used_cache:
            is_network = 0
        else:
            is_network = 1
        if external_user_id == None:
            external_user_id = get_extenal_user_id_by_api_type_id(api_type_id)
        # where="api_call_id= {}".format(api_call_id)
        update_data = {'external_user_id': external_user_id, 'endpoint': endpoint, 'outgoing_body': str(outgoing_body), 'outgoing_header': str(
            outgoing_header), 'http_status_code': http_status_code, 'response_body': str(response_body), 'incoming_message': str(incoming_message), 'is_network': is_network}
        self.update_by_id(id_column_value=api_call_id, json_data=update_data)
