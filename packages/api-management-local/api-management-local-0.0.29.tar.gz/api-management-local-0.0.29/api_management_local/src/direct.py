
from dotenv import load_dotenv
import json
import os
from circles_local_database_python.connector import Connector
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.connector import Connector
from circles_local_database_python.generic_crud import GenericCRUD
from .api_call import APICallsLocal
from .api_management_local import APIManagementsLocal
from .external_user_id import get_extenal_user_id_by_api_type_id

from url_local.url_circlez import OurUrl
from url_local import action_name_enum, entity_name_enum, component_name_enum
from user_context_remote.user_context import UserContext
from .api_limit import (DEVELOPER_EMAIL,
                        API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
                        API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME, APILimitsLocal)
import requests
from requests import request
import http
from sdk.src.validate import validate_enviroment_variables
from .APILimitStatus import APILimitStatus
from .API_Mangement_Manager import APIMangementManager
from .api_type import ApiType
from .stars import StarsLocal
from .Exception_API import ApiTypeDisabledException,ApiTypeIsNotExistException,PassedTheHardLimitException

BRAND_NAME = os.getenv('BRAND_NAME')
validate_enviroment_variables()
AUTHENTICATION_API_VERSION = 1

url_circlez = OurUrl()
authentication_login_validate_jwt_url = url_circlez.endpoint_url(
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


class Direct(GenericCRUD):
    def __init__(self) -> None:
        pass

    @staticmethod
    def try_to_call_api(external_user_id: int, api_type_id: int, endpoint: str, outgoing_body: str, outgoing_header: str, **kwargs) -> str:
        logger.start(object={'external_user_id': str(external_user_id), 'api_type_id': str(api_type_id), 'endpoint': str(
            endpoint), 'outgoing_body': str(outgoing_body), 'outgoing_header': str(outgoing_header)})
        action_id=ApiType.get_action_id_by_api_type_id(api_type_id)
        StarsLocal._profile_star_before_action(action_id)
        api_management = APIManagementsLocal()
        api_management.sleep_per_interval(api_type_id)
        if external_user_id == None:
            external_user_id = get_extenal_user_id_by_api_type_id(api_type_id)
        # connection = Connector.connect("api_call")
        # cursor = connection.cursor()
        try:
            arr, outgoing_body_significant_fields_hash = api_management.check_cache(
                api_type_id, outgoing_body)
            if arr == None:
                check = api_management.check_limit(
                    external_user_id=external_user_id, api_type_id=api_type_id)
                logger.info("check= " + str(check))
                if check == APILimitStatus.BETWEEN_SOFT_LIMIT_AND_HARD_LIMIT:
                    logger.warn("You excced the soft limit")
                if check != APILimitStatus.GREATER_THAN_HARD_LIMIT:
                    output = requests.post(
                        url=endpoint, data=outgoing_body, headers=outgoing_header)
                    status_code = output.status_code
                    text = output.text
                    incoming_message = output.content.decode('utf-8')
                    response_body = output.json()
                    response_body_str = json.dumps(response_body)
                    if http.HTTPStatus.OK == status_code:
                      StarsLocal._api_executed(api_type_id=api_type_id)
                    is_network = 1
                    api_call_data_dict = {'api_type_id': api_type_id, 'external_user_id': external_user_id,
                                          'endpoint': endpoint, 'outgoing_header': str(outgoing_header), 'outgoing_body': str(outgoing_body),
                                          'outgoing_body_significant_fields_hash': outgoing_body_significant_fields_hash,
                                          'incoming_message': incoming_message, 'http_status_code': status_code, 'response_body': response_body_str,
                                          'is_network': is_network
                                          }
                    api_call_id = APICallsLocal._insert_api_call_dict(
                        api_call_data_dict)
                    logger.end("check= " + str(check),
                               object={'status_code': status_code, 'text': text})
                    # return request("post", url=endpoint, data=outgoing_body, json=json, **kwargs)
                    return {'status_code': status_code, 'text': text}
                else:
                    logger.error("you passed the hard limit")

                    raise PassedTheHardLimitException
            else:
                status_code = arr[0]
                text = arr[1]
                is_network = 0
                incoming_message = ""
                response_body = ""
                api_call_data_dict = {'api_type_id': api_type_id, 'external_user_id': external_user_id,
                                      'endpoint': endpoint, 'outgoing_header': str(outgoing_header), 'outgoing_body': str(outgoing_body),
                                      'outgoing_body_significant_fields_hash': outgoing_body_significant_fields_hash,
                                      'incoming_message': incoming_message, 'http_status_code': status_code, 'response_body': response_body,
                                      'is_network': is_network
                                      }
                StarsLocal._api_executed(api_type_id=api_type_id)
                api_call_id = APICallsLocal._insert_api_call_dict(
                    api_call_data_dict)
                logger.info("bringing result from cache in database", object={
                            'status_code': status_code, 'text': text})
                return {'status_code': status_code, 'text': text}
        except Exception as exception:
            logger.exception("exception="+str(exception), object=exception)
            logger.end()
            raise exception
