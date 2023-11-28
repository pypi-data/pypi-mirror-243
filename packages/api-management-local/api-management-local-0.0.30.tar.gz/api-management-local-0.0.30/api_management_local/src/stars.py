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


class StarsLocal(GenericCRUD):
    def __init__(self) -> None:
        super().__init__(schema_name="action_star_subscription")

    @staticmethod
    def _get_the_action_stars_by_profile_id_action_id(profile_id, action_id)->int:
        user=UserContext.login_using_user_identification_and_password()
        subscription_id = user.get_effective_subscription_id_by_profile_id(profile_id=profile_id)
        select_clause = "action_stars"
        where = "subscription_id = {} AND action_id = {}".format(subscription_id, action_id)
        stars_local=StarsLocal()
        action_star = stars_local.select_one_tuple_by_where(
                view_table_name="action_star_subscription_view", select_clause_value=select_clause, where=where)
        logger.end(object={'api_limit_result': str(action_star)})
        return action_star[0]
    
    def _update_profile_stars(profile_id:int,action_id:int):
        #Effective_profile_id = UserContext.get_effective_profile_id()
        action_stars = StarsLocal._get_the_action_stars_by_profile_id_action_id(profile_id, action_id)
        connection = Connector.connect("profile")
        cursor = connection.cursor()
        query = f"""UPDATE profile.profile_table SET stars=stars+ %s WHERE profile_id= %s"""
        a=cursor.execute(query, (action_stars,profile_id))
        logger.info( {'action_id': action_id, #'stars': stars,# 
                      'action_stars': action_stars })

    def _api_executed(api_type_id):
        connection = Connector.connect("api_type")
        cursor = connection.cursor()
        query = f"""SELECT action_id FROM api_type.api_type_view WHERE api_type_id=%s"""
        cursor.execute(query, (api_type_id,))
        action_id=cursor.fetchone()
        user=UserContext.login_using_user_identification_and_password()
        profile_id = user.get_effective_profile_id()
        StarsLocal._update_profile_stars(profile_id,action_id[0])
    
    def how_many_stars_for_action_id(activty_id:int)->int:
        connection = Connector.connect("action_star_subscription")
        cursor = connection.cursor()
        query="SELECT action_stars FROM action_star_subscription.action_star_subscription_table WHERE action_id=%s"
        cursor.execute(query, (activty_id,))
        action_stars=cursor.fetchone()
        return action_stars[0]
   
    def how_many_stars_for_profile_id(profile_id:int)->int:
        connection = Connector.connect("profile")
        cursor = connection.cursor()
        query ="SELECT stars FROM profile.profile_table WHERE profile_id=%s"
        cursor.execute(query, (profile_id,))
        stars=cursor.fetchone()
        return stars[0]
        
    
    def _profile_star_before_action(activty_id:int):
        stars_for_action=StarsLocal.how_many_stars_for_action_id(activty_id)
        user=UserContext.login_using_user_identification_and_password()
        profile_id=user.get_effective_profile_id()
        stars_for_profile=StarsLocal.how_many_stars_for_profile_id(profile_id)
        if stars_for_profile+stars_for_action < 0:
            raise NotEnoughStarsForActivityException
        else:
            return
        

       
        
        
        
       

