import os
from url_local.url_circlez import OurUrl
import json
from typing import Any
import sys
from url_local import action_name_enum, entity_name_enum, component_name_enum
from language_local.lang_code import LangCode
from dotenv import load_dotenv
import requests
from httpstatus import HTTPStatus
from sdk.src.mini_logger import MiniLogger
# from circles_local_database_python.connector import Connector

# from logger_local.Logger import Logger
load_dotenv()
BRAND_NAME = os.getenv('BRAND_NAME')
ENVIORNMENT_NAME = os.getenv('ENVIRONMENT_NAME')
AUTHENTICATION_API_VERSION = 1

   
class UserContext:
    _instance = None

    def __new__(cls, user_identifier: str = None, password: str = None, user_JWT: str = None):
        if cls._instance is None:
            cls._instance = super(UserContext, cls).__new__(cls)
            if user_identifier is not None and password is not None:
                cls._instance._initialize(
                    user_identifier=user_identifier, password=password)
            else:
                cls._instance._initialize(user_JWT=user_JWT)
        return cls._instance

    def _initialize(self, user_identifier: str = None, password: str = None, user_JWT: str = None):
        self.real_user_id = None
        self.real_profile_id = None
        self.effective_user_id = None
        self.effective_profile_id = None
        self.lang_code = None
        self.real_first_name = None
        self.real_last_name = None
        self.real_display_name = None
        if (user_identifier is not None and password is not None):
            self.user_JWT = None
            data = self._authenticate_by_user_identification_and_password(
                user_identifier, password)
        else:
            self.user_JWT = user_JWT
            data = self._authenticate_by_user_JWT(user_JWT=user_JWT)
        self.get_user_data_login_response(validate_jwt_response=data)

    @staticmethod
    def login_using_user_identification_and_password(user_identifier: str = None, password: str = None):
        LOGIN_USING_USER_IDENTIFICATION_AND_PASSWORD_METHOD_NAME = "login_using_user_identification_and_password"
        MiniLogger.start(LOGIN_USING_USER_IDENTIFICATION_AND_PASSWORD_METHOD_NAME, object={"username": user_identifier, "password": password})
        if UserContext._instance is None:
            if user_identifier is None:
                try:
                    user_identifier = os.getenv("PRODUCT_USER_IDENTIFIER")
                except Exception as e:
                    MiniLogger.error("Exception missing PRODUCT_USER_IDENTIFIER in .env file - ERROR - " + str(e))
            if password is None:
                try:
                    password = os.getenv("PRODUCT_PASSWORD")
                except Exception as e:
                    MiniLogger.error("Exception missing PRODUCT_PASSWORD in .env file - ERROE -" + str(e))
            if user_identifier is None or password is None or user_identifier == "" or password == "":
                # To support cases when there is no PRODUCT_USERNAME and PRODUCT_PASSWORD in the deployment.
                return None
            UserContext._instance = UserContext(
                user_identifier=user_identifier, password=password)
        user = UserContext._instance
        MiniLogger.end(LOGIN_USING_USER_IDENTIFICATION_AND_PASSWORD_METHOD_NAME,object={"user": str(user)})
        return user

    @staticmethod
    def login_using_jwt(user_JWT: str = None):
        LOGIN_USING_JWT_METHOD_NAME = "login_using_jwt"
        MiniLogger.start(LOGIN_USING_JWT_METHOD_NAME ,object={"user_JWT": user_JWT})
        if UserContext._instance is None and user_JWT is not None:
            UserContext._instance = UserContext(user_JWT=user_JWT)
        user = UserContext._instance
        MiniLogger.end(LOGIN_USING_JWT_METHOD_NAME,object={"user": str(user)})
        return user

    def _set_real_user_id(self, user_id: int) -> None:
        _SET_REAL_USER_ID_METHOD_NAME = "_set_real_user_id"
        MiniLogger.start(_SET_REAL_USER_ID_METHOD_NAME,object={"user_id": user_id})
        self.real_user_id = user_id
        MiniLogger.end(_SET_REAL_USER_ID_METHOD_NAME)

    def _set_real_profile_id(self, profile_id: int) -> None:
        _SET_REAL_PROFILE_ID_METHOD_NAME = "_set_real_profile_id"
        MiniLogger.start(_SET_REAL_PROFILE_ID_METHOD_NAME,object={"profile_id": profile_id})
        self.real_profile_id = profile_id
        MiniLogger.end(_SET_REAL_PROFILE_ID_METHOD_NAME)

    def get_real_user_id(self) -> int:
        GET_REAL_USER_ID_METHOD_NAME = "get_real_user_id"
        MiniLogger.start(GET_REAL_USER_ID_METHOD_NAME)
        MiniLogger.end(GET_REAL_USER_ID_METHOD_NAME,object={"user_id": self.real_user_id})
        return self.real_user_id

    def get_real_profile_id(self) -> int:
        GET_REAL_PROFILE_ID_METHOD_NAME = "get_real_profile_id"
        MiniLogger.start(GET_REAL_PROFILE_ID_METHOD_NAME)
        MiniLogger.end(GET_REAL_PROFILE_ID_METHOD_NAME,object={"user_id": self.real_profile_id})
        return self.real_profile_id

    def get_curent_lang_code(self) -> str:
        GET_CURENT_LANG_CODE_METHOD_NAME = "get_curent_lang_code"
        MiniLogger.start(GET_CURENT_LANG_CODE_METHOD_NAME)
        MiniLogger.end(GET_CURENT_LANG_CODE_METHOD_NAME,object={"language": self.lang_code})
        return self.lang_code

    def _set_current_lang_code(self, language: LangCode) -> None:
        _SET_CURRENT_LANG_CODE_METHOD_NAME = "_set_current_lang_code"
        MiniLogger.start(_SET_CURRENT_LANG_CODE_METHOD_NAME,object={"language": language.value})
        self.lang_code = language.value
        MiniLogger.end(_SET_CURRENT_LANG_CODE_METHOD_NAME)

    def _set_real_first_name(self, first_name: str) -> None:
        _SET_REAL_FIRST_NAME_METHOD_NAME = "_set_real_first_name"
        MiniLogger.start(_SET_REAL_FIRST_NAME_METHOD_NAME,object={"first_name": first_name})
        self.real_first_name = first_name
        MiniLogger.end(_SET_REAL_FIRST_NAME_METHOD_NAME)

    def _set_real_last_name(self, last_name: str) -> None:
        _SET_REAL_LAST_NAME_METHOD_NAME = "_set_real_last_name"
        MiniLogger.start(_SET_REAL_LAST_NAME_METHOD_NAME,object={"first_name": last_name})
        self.real_last_name = last_name
        MiniLogger.end(_SET_REAL_LAST_NAME_METHOD_NAME)

    def get_real_first_name(self) -> str:
        GET_REAL_FIRST_NAME_METHOD_NAME = "get_real_first_name"
        MiniLogger.start(GET_REAL_FIRST_NAME_METHOD_NAME)
        MiniLogger.end(GET_REAL_FIRST_NAME_METHOD_NAME,object={"first_name": self.real_first_name})
        return self.real_first_name

    def get_real_last_name(self) -> str:
        GET_REAL_LAST_NAME_METHOD_NAME = "get_real_last_name"
        MiniLogger.start(GET_REAL_LAST_NAME_METHOD_NAME)
        MiniLogger.end(GET_REAL_LAST_NAME_METHOD_NAME,object={"last_name": self.real_last_name})
        return self.real_last_name

    def _set_real_name(self, name: str) -> None:
        _SET_REAL_NAME_METHOD_NAME = "_set_real_name"
        MiniLogger.start(_SET_REAL_NAME_METHOD_NAME,object={"first_name": name})
        self.real_display_name = name
        MiniLogger.end(_SET_REAL_NAME_METHOD_NAME)

    def get_real_name(self) -> str:
        GET_REAL_NAME_METHOD_NAME = "get_real_name"
        MiniLogger.start(GET_REAL_NAME_METHOD_NAME)
        MiniLogger.end(GET_REAL_NAME_METHOD_NAME,object={"first_name": self.real_first_name})
        return self.real_display_name

    def get_user_JWT(self) -> str:
        return self.user_JWT

    def get_effective_user_id(self) -> int:
        return self.effective_user_id

    def get_effective_profile_id(self) -> int:
        return self.effective_profile_id

    def _set_effective_user_id(self, user_id: int) -> None:
        self.effective_user_id = user_id

    def _set_effective_profile_id(self, profile_id: int) -> None:
        self.effective_profile_id = profile_id

    def get_effective_subscription_id_by_profile_id(self, profile_id: int) -> None:
        # connection = Connector.connect("user_subscription_view")
        # cursor = connection.cursor()
        # query="""SELECT subscription_id FROM subscription_user.subscription_user_view
        # JOIN profile_user.profile_user_table ON profile_user_table.user_id = subscription_user_view.user_id
        # WHERE profile_user_table.profile_id=%s"""
        # cursor.execute(query, (profile_id,))
        # subscription_id=cursor.fetchone()
        # return subscription_id[0]
        return 5
    
    def _authenticate_by_user_identification_and_password(self, user_identifier: str, password: str) -> str:
        _AUTHENTICATE_BY_USER_IDENTIFICATION_AND_PASSWORD_METHOD_NAME = "_authenticate_by_user_identification_and_password"
        MiniLogger.start(_AUTHENTICATE_BY_USER_IDENTIFICATION_AND_PASSWORD_METHOD_NAME,object={"email": user_identifier, "password": password})
        try:
            url_circlez = OurUrl()
            url_jwt = url_circlez.endpoint_url(
                brand_name=BRAND_NAME,
                environment_name=ENVIORNMENT_NAME,
                component_name=component_name_enum.ComponentName.AUTHENTICATION.value,
                entity_name=entity_name_enum.EntityName.AUTH_LOGIN.value,
                version=AUTHENTICATION_API_VERSION,
                action_name=action_name_enum.ActionName.LOGIN.value
            )
            data = {"user_identifier": user_identifier, "password": password}
            headers = {"Content-Type": "application/json"}
            output = requests.post(
                url=url_jwt, data=json.dumps(data, separators=(",", ":")), headers=headers
            )
            if output.status_code != HTTPStatus.OK:
                MiniLogger.info(_AUTHENTICATE_BY_USER_IDENTIFICATION_AND_PASSWORD_METHOD_NAME + " output.status_code != HTTPStatus.OK " + output.text)
                raise Exception(output.text)
            self.user_JWT = output.json()["data"]["token"]
            MiniLogger.end(_AUTHENTICATE_BY_USER_IDENTIFICATION_AND_PASSWORD_METHOD_NAME,object={"user_JWT": self.user_JWT })
            return output
        except Exception as exception:
            MiniLogger.error(
                "Error(Exception): user-context-remote-python _authenticate() " + str(exception))
            MiniLogger.end(_AUTHENTICATE_BY_USER_IDENTIFICATION_AND_PASSWORD_METHOD_NAME)
            raise

    def _authenticate_by_user_JWT(self, user_JWT: str) -> str:
        _AUTHENTICATE_BY_USER_JWT_METHOD_NAME = "_authenticate_by_user_JWT"
        MiniLogger.start(_AUTHENTICATE_BY_USER_JWT_METHOD_NAME,object={"user_JWT": user_JWT})
        url_circlez = OurUrl()
        authentication_login_validate_jwt_url = url_circlez.endpoint_url(
            brand_name=BRAND_NAME,
            environment_name=ENVIORNMENT_NAME,
            component_name=component_name_enum.ComponentName.AUTHENTICATION.value,
            entity_name=entity_name_enum.EntityName.AUTH_LOGIN.value,
            version=AUTHENTICATION_API_VERSION,
            action_name=action_name_enum.ActionName.VALIDATE_JWT.value
        )
        data = {"userJWT": user_JWT}
        headers = {"Content-Type": "application/json"}
        output = requests.post(
            url=authentication_login_validate_jwt_url, data=json.dumps(data, separators=(",", ":")), headers=headers
        )
        if output.status_code != HTTPStatus.OK:
            MiniLogger.info(
                "user-context-remote-python-package _authenticate_by_user_JWT() output.status_code != HTTPStatus.OK " + output.text)
            raise Exception(output.text)
        MiniLogger.end(_AUTHENTICATE_BY_USER_JWT_METHOD_NAME, object={"validate_jwt_response": output})
        return output

    def get_user_data_login_response(self, validate_jwt_response: str) -> None:
        if "userDetails" in validate_jwt_response.json()["data"]:
            userDetails = validate_jwt_response.json()["data"]["userDetails"]

            if "profileId" in userDetails:
                profile_id = userDetails["profileId"]
                self._set_real_profile_id(int(profile_id))
                self._set_effective_profile_id(int(profile_id))

            if "userId" in userDetails:
                user_id = userDetails["userId"]
                self._set_effective_user_id(int(user_id))
                self._set_real_user_id(int(user_id))

            if "lang_code" in userDetails:
                lang_code = userDetails["lang_code"]
                self._set_current_lang_code(lang_code)

            if "firstName" in userDetails:
                first_name = userDetails["firstName"]
                self._set_real_first_name(first_name)

            if "lastName" in userDetails:
                last_name = userDetails["lastName"]
                self._set_real_last_name(last_name)

            if self.real_first_name is not None and self.real_last_name is not None:
                name = first_name + " " + last_name
            else:
                # If first_name and last_name are not available, use the email as the name
                name = userDetails.get("email", None)

            self._set_real_name(name)


# from #logger_local.#loggerComponentEnum import #loggerComponentEnum
# from #logger_local.#logger import #logger

# USER_CONTEXT_LOCAL_PYTHON_COMPONENT_ID = 197
# USER_CONTEXT_LOCAL_PYTHON_COMPONENT_NAME = "User Context python package"
# DEVELOPER_EMAIL = "idan.a@circ.zone"
# obj = {
#     'component_id': USER_CONTEXT_LOCAL_PYTHON_COMPONENT_ID,
#     'component_name': USER_CONTEXT_LOCAL_PYTHON_COMPONENT_NAME,
#     'component_category': #loggerComponentEnum.ComponentCategory.Code.value,
#     'developer_email': DEVELOPER_EMAIL
# }
# #logger = #logger.create_#logger(object=obj)

    # Commented as we get the decoded user_user_JWT from the authentication service and the user-context do not have access to th JWT_SECRET_KEY
    # def get_user_json_by_user_user_JWT(self, user_JWT: str) -> None:
    #     if user_JWT is None or user_JWT == "":
    #         raise Exception(
    #             "Your .env PRODUCT_NAME or PRODUCT_PASSWORD is wrong")
    #     #logger.start(object={"user_JWT": user_JWT})
    #     try:
    #         secret_key = os.getenv("JWT_SECRET_KEY")
    #         if secret_key is not None:
    #             decoded_payload = jwt.decode(user_JWT, secret_key, algorithms=[
    #                                          "HS256"], options={"verify_signature": False})
    #             self.profile_id = int(decoded_payload.get('profileId'))
    #             self.user_id = int(decoded_payload.get('userId'))
    #             self.language = decoded_payload.get('language')
    #             #logger.end()
    #     except jwt.ExpiredSignatureError as e:
    #         # Handle token expiration
    #         #logger.exception(object=e)
    #         print("Error:JWT token has expired.", sys.stderr)
    #         #logger.end()
    #         raise
    #     except jwt.InvalidTokenError as e:
    #         # Handle invalid token
    #         #logger.exception(object=e)
    #         print("Error:Invalid JWT token.", sys.stderr)
    #         #logger.end()
    #         raise
