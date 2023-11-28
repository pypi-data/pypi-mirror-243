from dotenv import load_dotenv
import json
import os
from circles_local_database_python.connector import Connector
from logger_local.Logger import Logger
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from circles_local_database_python.connector import Connector
from url_local.url_circlez import OurUrl
from url_local import action_name_enum, entity_name_enum, component_name_enum
from .api_limit import (DEVELOPER_EMAIL,
                        API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_ID,
                        API_MANAGEMENT_LOCAL_PYTHON_COMPONENT_NAME, APILimitsLocal)
import requests
from sdk.src.validate import validate_enviroment_variables
from .APILimitStatus import APILimitStatus
import http
import random
from .Exception_API import ApiTypeDisabledException,ApiTypeIsNotExistException
import time
load_dotenv()
BRAND_NAME = os.getenv('BRAND_NAME')
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
logger = Logger.create_logger(object=api_management_local_python_code)


class APIManagementsLocal():
    def __init__(self) -> None:
        pass
    def delete_api(external_user_id: int, api_type_id: int, data: str):
        logger.start(object={'external_user_id': str(external_user_id), 'api_type_id': str(api_type_id), 'data': data})
        
        try:
            check_limit = APIManagementsLocal.check_limit(external_user_id=external_user_id, api_type_id=api_type_id)
            data_j = json.loads(data)
            
            if check_limit == APILimitStatus.BELOW_SOFT_LIMIT:     
                requests.delete(data=data_j)
                logger.end()
                return  
            
            elif check_limit == APILimitStatus.BETWEEN_SOFT_LIMIT_AND_HARD_LIMIT:
                logger.warn("you passed the soft limit")
            
            else:
                logger.error("you passed the hard limit")
                
        except Exception as exception:
            logger.exception("exception="+str(exception), object=exception)
            raise 
        finally:
            logger.end() 



    def get_api(external_user_id: int, api_type_id: int, data: str):
        logger.start(object={'external_user_id': str(external_user_id), 'api_type_id': str(api_type_id), 'data': data})
        
        try:
            check_limit = APIManagementsLocal.check_limit(external_user_id=external_user_id, api_type_id=api_type_id)
            data_j = json.loads(data)
            
            if check_limit == APILimitStatus.BELOW_SOFT_LIMIT:     
                requests.get(data=data_j)
                logger.end()
                return  
            
            elif check_limit == APILimitStatus.BETWEEN_SOFT_LIMIT_AND_HARD_LIMIT:
                logger.warn("you passed the soft limit")
            
            else:
                logger.error("you passed the hard limit")
                
        except Exception as exception:
            logger.exception("exception="+str(exception), object=exception)
            raise 
        finally:
            logger.end() 

    def put_api(external_user_id: int, api_type_id: int, data: str):
        logger.start(object={'external_user_id': str(external_user_id), 'api_type_id': str(api_type_id), 'data': data})
        
        try:
            check_limit = APIManagementsLocal.check_limit(external_user_id=external_user_id, api_type_id=api_type_id)
            data_j = json.loads(data)
            
            if check_limit == APILimitStatus.BELOW_SOFT_LIMIT:     
                requests.put(data=data_j)
                logger.end()
                return  
            
            elif check_limit == APILimitStatus.BETWEEN_SOFT_LIMIT_AND_HARD_LIMIT:
                logger.warn("you passed the soft limit")
            
            else:
                logger.error("you passed the hard limit")
                
        except Exception as exception:
            logger.exception("exception="+str(exception), object=exception)
            raise 
        finally:
            logger.end() 

    @staticmethod
    def _second_from_last_network_api( api_type_id: int) -> int:
        logger.start(object={'api_type_id': str(api_type_id)})
        connection = Connector.connect("api_call")
        cursor = connection.cursor()
        query = f"""SELECT TIMESTAMPDIFF(SECOND,start_timestamp, NOW()) FROM api_call.api_call_view WHERE api_type_id=%s AND is_network=TRUE ORDER BY start_timestamp DESC LIMIT 1"""
        cursor.execute(query, (api_type_id,))
        arr = cursor.fetchone()
        second_from_last_network_api = arr[0]
        logger.info("second_from_last_network_api = " +
                    str(second_from_last_network_api))
        return second_from_last_network_api

  


   

    @staticmethod
    def _get_hard_limit_by_api_type_id(api_type_id: int):
        connection = Connector.connect("api_call")
        cursor = connection.cursor()
        try:
            query = f""" SELECT hard_limit_value, hard_limit_unit FROM api_limit.api_limit_table WHERE api_type_id = %s"""
            cursor.execute(query, (api_type_id,))
            arr = cursor.fetchone()
            hard_limit_value_by_api_type_id = arr[0]
            hard_limit_unit_by_api_type_id = arr[1]
            return hard_limit_value_by_api_type_id, hard_limit_unit_by_api_type_id
        except Exception as exception:
            logger.exception("exception="+str(exception), object=exception)
            raise exception
    
    
    @staticmethod
    def get_actual_api_succ_network_by_api_type_id_last_x_units(external_user_id: int, api_type_id: int, value: int, unit: str) -> int:
        logger.start(object={'api_type_id': str(
            api_type_id), 'value': str(value), 'unit': unit})
        connection = Connector.connect("api_call")
        cursor = connection.cursor()

        try:
            query = """
                SELECT COUNT(*)
                FROM api_call_view
                WHERE api_type_id = {} AND external_user_id = {}
                AND TIMESTAMPDIFF({}, created_timestamp, NOW()) <= {}
                AND http_status_code = {} AND is_network=TRUE
            """
            http_status_code = http.HTTPStatus.OK.value
            sql = (query.format(api_type_id, external_user_id,
                   unit, value, http_status_code))
            cursor.execute(sql)
            actual_succ_count = cursor.fetchone()[0]
            logger.end(object={'actual_succ_count': actual_succ_count})
            return actual_succ_count
        except Exception as exception:
            logger.exception(object=exception)
            logger.end()
            
    @staticmethod
    def sleep_per_interval( api_type_id: int):
            logger.start(object={'api_type_id': str(api_type_id)})
            connection = Connector.connect("api_type")
            cursor = connection.cursor()
            query = f"""SELECT interval_min_seconds, interval_max_seconds FROM api_type.api_type_view WHERE is_enabled=TRUE AND api_type_id= %s """
            cursor.execute(query, (api_type_id,))
            arr = cursor.fetchone()
            APIManagementsLocal._check_api_type_result(api_type_id,arr)
            interval_min_seconds = arr[0]
            interval_max_seconds = arr[1]
            random_interval = random.uniform(
                interval_min_seconds, interval_max_seconds)
            logger.info("interval_min_seconds= "+str(interval_min_seconds) + " interval_max_seconds= " +
                        str(interval_max_seconds) + " random_interval= "+str(random_interval))
            second_from_last_network_api = APIManagementsLocal._second_from_last_network_api(
                api_type_id)
            if random_interval > second_from_last_network_api:
                sleep_second = random_interval-second_from_last_network_api
                logger.info("seleeping "+str(sleep_second) + " seconds")
                time.sleep(sleep_second)
            else:
                logger.info("No sleep needed")
                logger.end()

    @staticmethod          
    def check_cache(api_type_id: int, outgoing_body: str):
            logger.start(object={'api_type_id': str(api_type_id), 'outgoing_body': outgoing_body})
            connection = Connector.connect("api_call")
            cursor = connection.cursor()

            try:
                outgoing_body_significant_fields_hash = hash(
                    APIManagementsLocal._get_json_with_only_sagnificant_fields_by_api_type_id(outgoing_body, api_type_id=str(api_type_id)))
                query = f"""SELECT  http_status_code,response_body 
                            FROM api_call.api_call_view
                            JOIN api_type.api_type_view ON api_type.api_type_view.api_type_id = api_call.api_call_view.api_type_id
                            WHERE api_call_view.api_type_id= %s AND http_status_code=200
                                AND TIMESTAMPDIFF( MINUTE , api_call.api_call_view.start_timestamp, NOW() ) <= api_type_view.expiration_value
                                AND outgoing_body_significant_fields_hash= %s 
                                AND is_network=TRUE
                            ORDER BY api_call_id DESC LIMIT 1"""
                cursor.execute(
                    query, (api_type_id, outgoing_body_significant_fields_hash))
                arr = cursor.fetchone()
                logger.end()
                return arr, outgoing_body_significant_fields_hash
            except Exception as exception:
                logger.exception("exception="+str(exception), object=exception)
                logger.end()
                
    @staticmethod
    def check_limit(external_user_id: int, api_type_id: int) -> int:
        logger.start(
            object={'external_user_id': external_user_id, 'api_type_id': str(api_type_id)})
        limits = APILimitsLocal.get_api_limit_by_api_type_id_external_user_id(
            api_type_id, external_user_id)
        soft_limit_value = limits[0]
        soft_limit_unit = limits[1]
        hard_limit_value = limits[2]
        # hard_limit_unit=limits[3]
        api_succ = APIManagementsLocal.get_actual_api_succ_network_by_api_type_id_last_x_units(
            external_user_id, api_type_id, soft_limit_value, soft_limit_unit)

        if api_succ < soft_limit_value:
            return APILimitStatus.BELOW_SOFT_LIMIT
        elif soft_limit_value <= api_succ and api_succ < hard_limit_value:
            return APILimitStatus.BETWEEN_SOFT_LIMIT_AND_HARD_LIMIT
        else:
            return APILimitStatus.GREATER_THAN_HARD_LIMIT
        
    
    @staticmethod
    def _get_json_with_only_sagnificant_fields_by_api_type_id(json1: json, api_type_id: int) -> json:
        logger.start(object={'json1': str(json1),
                     'api_type_id': str(api_type_id)})
        connection = Connector.connect("api_type")
        try:
            cursor = connection.cursor()
            query = f"SELECT field_name FROM api_type.api_type_field_view WHERE api_type_id = %s AND field_significant = TRUE"
            cursor.execute(query, (api_type_id,))
            significant_fields = [row[0] for row in cursor.fetchall()]
            data = json.loads(json1)
            filtered_data = {key: data[key]
                             for key in significant_fields if key in data}
            filtered_json = json.dumps(filtered_data)
            logger.end(object={'filtered_json': str(filtered_json)})
            return filtered_json
        except Exception as exception:
            logger.exception("exception"+str(exception), object=exception)
            logger.end()
    
    def _check_api_type_result(api_type_id:int,arr:list):
        if arr is None:
            connection = Connector.connect("api_type")
            cursor = connection.cursor()
            query = f"SELECT is_enabled FROM api_type.api_type_view WHERE api_type_id = %s"
            cursor.execute(query, (api_type_id,))
            is_enabled=cursor.fetchone()
            if is_enabled is None:
                raise ApiTypeIsNotExistException
            elif is_enabled[0]==0:
                raise  ApiTypeDisabledException
            else:
                return
 


