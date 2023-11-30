import sys
import os
script_directory = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_directory, '..'))
from .url import URL
from .constants_url_profile_local import UrlProfileLocalConstants
from logger_local.Logger import Logger
from dotenv import load_dotenv
from circles_local_database_python.generic_crud import GenericCRUD
import dotenv
dotenv.load_dotenv()

logger = Logger.create_logger(
    object=UrlProfileLocalConstants.OBJECT_FOR_LOGGER_CODE)


class UrlProfilesLocal(GenericCRUD):

    def __init__(self):
        INIT_METHOD_NAME = '__init__'

        logger.start(INIT_METHOD_NAME)
        super().__init__(default_schema_name="profile_url", default_table_name='profile_url_table',
                         default_id_column_name='profile_id', default_view_table_name='profile_url_view')

        logger.end(INIT_METHOD_NAME)

    def insert(self, url_id: str, url_type_id: int, profile_id: int):
        INSERT_URL_PROFILE_METHOD_NAME = 'insert_url_profile'
        logger.start(INSERT_URL_PROFILE_METHOD_NAME,
                     object={"url_id": url_id})
        profile_url_json = {'profile_id': profile_id,
                            'url_type_id': url_type_id,
                            'url': url_id}
        profile_url_id = GenericCRUD.insert(self, data_json=profile_url_json)
        logger.end(INSERT_URL_PROFILE_METHOD_NAME)
        return profile_url_id

    def update(self, url_id: str, url_type_id: int, profile_id: int):

        UPDATE_URL_PROFILE_METHOD_NAME = 'update_url_profile'
        logger.start(UPDATE_URL_PROFILE_METHOD_NAME,
                     object={"url_id": url_id})
        profile_url_json = {'profile_id': profile_id,
                            'url_type_id': url_type_id,
                            'url': url_id}
        GenericCRUD.update_by_id(self, data_json=profile_url_json,
                                 id_column_value=profile_id, order_by='start_timestamp desc')
        logger.end(UPDATE_URL_PROFILE_METHOD_NAME)

    def delete_by_profile_id(self, profile_id: int):
        DELETE_URL_PROFILE_METHOD_NAME = 'delete_url_profile'
        logger.start(DELETE_URL_PROFILE_METHOD_NAME,
                     object={"profile_id": profile_id})
        GenericCRUD.delete_by_id(self, id_column_value=profile_id)
        logger.end(DELETE_URL_PROFILE_METHOD_NAME)

    def get_last_url_by_profile_id(self, profile_id: int) -> URL:
        GET_LAST_URL_ID_BY_PROFILE_ID_METHOD_NAME = "get_last_url_id_by_profile_id"
        logger.start(GET_LAST_URL_ID_BY_PROFILE_ID_METHOD_NAME,
                     object={'profile_id': profile_id})
        where_clause = f"profile_id = {profile_id}"
        url = GenericCRUD.select_one_tuple_by_where(self, select_clause_value="url",
                                                      where=where_clause, order_by="start_timestamp desc")
        logger.end(GET_LAST_URL_ID_BY_PROFILE_ID_METHOD_NAME,
                   object={'url': url})
        if not url:
            return None
        return url[0]
