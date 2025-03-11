import requests
from requests.exceptions import RequestException
import hmac
import hashlib
import json
from base64 import b64encode

from monnify.exceptions import UnprocessableRequestException, GatewayException, DuplicateInstanceException, InvalidDataException


class Base:

    _instance = []

    def __new__(cls, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"):
        if len(cls._instance)==0:
            instance = super().__new__(cls)
            instance.__init__(API_KEY, SECRET_KEY, ENV)
            cls._instance.append(instance)
            return instance
        elif cls._instance and (cls._instance[0].__env != ENV or cls._instance[0].__api_key != API_KEY):
            raise DuplicateInstanceException("You can't instantiate multiple classes with different environments")
        else:
            instance = super().__new__(cls)
            instance.__init__(API_KEY, SECRET_KEY, ENV)
            return instance
        #     if list(cls._instances.values())[0].__env != ENV:
        #         raise DuplicateInstanceException("You can't instantiate multiple classes with different environments")
        #     return cls._instances[ENV]
        # return instance
    

    def __init__(self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX") -> None:

        self.__headers = {"Content-Type": "application/json"}

        if API_KEY is None or SECRET_KEY is None:
            raise InvalidDataException("Cannot instantiate base class without API or Secret key")
        elif ENV == "SANDBOX":
            if API_KEY.strip().startswith('MK_TEST') is False:
                raise InvalidDataException("Can only use test API_KEY for sandbox environment")
            else:
                self.__env = "SANDBOX"
                self.__api_key = API_KEY.strip()
                self.__secret_key = SECRET_KEY.strip()
                self.__base_url = "https://sandbox.monnify.com"
        elif ENV == "LIVE":
            if API_KEY.strip().startswith('MK_PROD') is False:
                raise InvalidDataException("Can only use live API_KEY for live environment")
            else:
                self.__env = "LIVE"
                self.__api_key = API_KEY.strip()
                self.__secret_key = SECRET_KEY.strip()
                self.__base_url = "https://api.monnify.com"
        else:
            raise InvalidDataException(
                "Unkwown environment supplied, either supply 'SANDBOX' or 'LIVE'"
            )
        
        

    def get_auth_token(self):

        auth_string = self.__api_key + ":" + self.__secret_key
        base64_hash = b64encode(auth_string.encode('ascii')).decode()
        self.__headers['Authorization'] = f"Basic {base64_hash}"
        url = self.__base_url + "/api/v1/auth/login"
        data = {}
        try:
            response = requests.post(url=url, headers=self.__headers, data=json.dumps(data))
            if response.status_code == 200:
                return response.status_code, response.json()
            elif response.status_code >= 400 and response.status_code < 500:
                raise UnprocessableRequestException(response.text,response.status_code)
            elif response.status_code >= 500:
                raise GatewayException(response.text,response.status_code)
            else:
                raise RequestException(response.status_code,response.text)
        except Exception as e:
            print(e)
            raise Exception(e)


    def do_get(self: object, url_path: str, authorization: str) -> tuple:
        url: str = self.__base_url + url_path
        headers: dict = self.__headers
        headers["Authorization"] = f"Bearer {authorization}"
        try:
            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                return response.status_code, response.json()
            elif response.status_code >= 400 and response.status_code < 500:
                raise UnprocessableRequestException(response.text,response.status_code)
            elif response.status_code >= 500:
                raise GatewayException(response.text,response.status_code)
            else:
                raise RequestException(response.status_code,response.text)
        except Exception as e:
            print(e)
            raise Exception(e)


    def do_post(self: object, url_path: str, authorization: str, data: dict) -> tuple:
        url: str = self.__base_url + url_path
        headers: dict = self.__headers
        headers["Authorization"] = f"Bearer {authorization}"
        try:
            response = requests.post(url=url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                return response.status_code, response.json()
            elif response.status_code >= 400 and response.status_code < 500:
                raise UnprocessableRequestException(response.text,response.status_code)
            elif response.status_code >= 500:
                raise GatewayException(response.text,response.status_code)
            else:
                raise RequestException(response.status_code,response.text)
        except Exception as e:
            print(e)
            raise Exception(e)


    def do_put(self: object, url_path: str, authorization: str, data: dict) -> tuple:
        url: str = self.__base_url + url_path
        headers: dict = self.__headers
        headers["Authorization"] = f"Bearer {authorization}"
        try:
            response = requests.put(url=url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                return response.status_code, response.json()
            elif response.status_code >= 400 and response.status_code < 500:
                raise UnprocessableRequestException(response.text,response.status_code)
            elif response.status_code >= 500:
                raise GatewayException(response.text,response.status_code)
            else:
                raise RequestException(response.status_code,response.text)
        except Exception as e:
            print(e)
            raise Exception(e)


    def do_delete(self: object, url_path: str, authorization: str) -> tuple:
        url: str = self.__base_url + url_path
        headers: dict = self.__headers
        headers["Authorization"] = f"Bearer {authorization}"
        try:
            response = requests.delete(url=url, headers=headers)
            if response.status_code == 200:
                return response.status_code, response.json()
            elif response.status_code >= 400 and response.status_code < 500:
                raise UnprocessableRequestException(response.text,response.status_code)
            elif response.status_code >= 500:
                raise GatewayException(response.text,response.status_code)
            else:
                raise RequestException(response.status_code,response.text)
        except Exception as e:
            print(e)
            raise Exception(e)

    def compare_hash(self: object, payload: bytes, monnify_signature: str) -> bool:

        secret_key_bytes: bytes = self.__secret_key.encode("utf-8")
        hash_in_bytes: bytes = hmac.new(
            secret_key_bytes, msg=payload, digestmod=hashlib.sha512
        )
        hash_in_hex: str = hash_in_bytes.hexdigest()
        return hmac.compare_digest(hash_in_hex, monnify_signature)
