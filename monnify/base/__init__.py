import requests
from requests.exceptions import RequestException
import hmac
import hashlib
import json
from base64 import b64encode
from datetime import datetime

from monnify.exceptions import (
    UnprocessableRequestException,
    GatewayException,
    DuplicateInstanceException,
    InvalidDataException,
    GlobalException
)


class Base:
    """The base monnify classes from which other classes inherits

    Raises:
        DuplicateInstanceException: This is thrown when two instances of different enviroments or API key are created

        InvalidDataException: This is thrown when the class is instantiated with invalid data

        UnprocessableRequestException: This is thrown when the API request cannot be processed

        GatewayException: This is thrown when there's a server error with the API

        RequestException: This is thrown when there's an issue with the API request
    Returns:
        _type_: An instance of Base
    """    

    _instance = []
    __TOKENCONFIG = {"ISTOKENSET":False,"TOKENEXPIRATION":None,"TOKEN":None, "THRESHOLD":500}

    def __new__(cls, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"):
        """_summary_

        Args:
            API_KEY (str): _description_. Merchant API Key.
            SECRET_KEY (str): _description_. Merchant Secret Key.
            ENV (str): _description_. API environment, defaults to "SANDBOX".

        Raises:
            DuplicateInstanceException

        Returns:
            _type_: Instance of Base clase
        """        
        if len(cls._instance) == 0:
            instance = super().__new__(cls)
            instance.__init__(API_KEY, SECRET_KEY, ENV)
            cls._instance.append(instance)
            return instance
        elif cls._instance and (
            cls._instance[0].__env != ENV or cls._instance[0].__api_key != API_KEY
        ):
            raise DuplicateInstanceException(
                "You can't instantiate multiple classes with different environments"
            )
        else:
            instance = super().__new__(cls)
            instance.__init__(API_KEY, SECRET_KEY, ENV)
            return instance

    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:
        """Initialises the Base class

        Args:
            API_KEY (str): _description_. Merchant API Key.
            SECRET_KEY (str): _description_. Merchant Secret Key.
            ENV (str): _description_. API environment, defaults to "SANDBOX".

        Raises:
            InvalidDataException
        """        


        self.__headers = {"Content-Type": "application/json"}

        if API_KEY is None or SECRET_KEY is None:
            raise InvalidDataException(
                "Cannot instantiate base class without API or Secret key"
            )
        elif ENV == "SANDBOX":
            if API_KEY.strip().startswith("MK_TEST") is False:
                raise InvalidDataException(
                    "Can only use test API_KEY for sandbox environment"
                )
            else:
                self.__env = "SANDBOX"
                self.__api_key = API_KEY.strip()
                self.__secret_key = SECRET_KEY.strip()
                self.__base_url = "https://sandbox.monnify.com"
        elif ENV == "LIVE":
            if API_KEY.strip().startswith("MK_PROD") is False:
                raise InvalidDataException(
                    "Can only use live API_KEY for live environment"
                )
            else:
                self.__env = "LIVE"
                self.__api_key = API_KEY.strip()
                self.__secret_key = SECRET_KEY.strip()
                self.__base_url = "https://api.monnify.com"
        else:
            raise InvalidDataException(
                "Unkwown environment supplied, either supply 'SANDBOX' or 'LIVE'"
            )

    def __set_token(self, token: str, expiry_time: int) -> None:
        """
        Sets the access token and its expiration time
        """
        self.__TOKENCONFIG["TOKEN"] = token
        self.__TOKENCONFIG["TOKENEXPIRATION"] = expiry_time
        self.__TOKENCONFIG["ISTOKENSET"] = True


    def get_auth_token(self, cache: bool=True) -> tuple:
        """Retrieves access token from Monnify

        Raises:
            UnprocessableRequestException: This is thrown when the API request cannot be processed
            GatewayException: This is thrown when there's a server error with the API
            RequestException: This is thrown when there's an issue with the API request
            Exception: A general exception

        Returns:
            _type_: A tuple of API status code, and a json response
        """

        if (cache is True and 
            self.__TOKENCONFIG["ISTOKENSET"] is True and 
            self.__TOKENCONFIG["TOKENEXPIRATION"] > int(datetime.now().timestamp())):
            return 200, {"accessToken":self.__TOKENCONFIG["TOKEN"],
                         "expiresIn":(self.__TOKENCONFIG["TOKENEXPIRATION"]-int(datetime.now().timestamp()))}
        
        auth_string = self.__api_key + ":" + self.__secret_key
        base64_hash = b64encode(auth_string.encode("ascii")).decode()
        self.__headers["Authorization"] = f"Basic {base64_hash}"
        url = self.__base_url + "/api/v1/auth/login"
        data = {}
        try:
            response = requests.post(
                url=url, headers=self.__headers, data=json.dumps(data)
            )
            if response.status_code == 200:
                resp = response.json()
                token = resp['responseBody']['accessToken']
                expiry = resp['responseBody']['expiresIn']
                if cache is True and expiry >= self.__TOKENCONFIG["THRESHOLD"]:
                    new_expiry =int(datetime.now().timestamp()) + expiry
                    self.__set_token(token, new_expiry)
                return response.status_code, {"accessToken":token,
                                              "expiresIn":expiry}
            
            elif response.status_code >= 400 and response.status_code < 500:
                raise UnprocessableRequestException(response.text, response.status_code)
            
            elif response.status_code >= 500:
                raise GatewayException(response.text, response.status_code)
            else:
                raise RequestException(response.status_code, response.text)
        except Exception as e:
            raise GlobalException(e)

    @classmethod  
    def reset_token_config(cls):
        """
        Resets the token configuration
        """
        cls.__TOKENCONFIG["TOKEN"] = None
        cls.__TOKENCONFIG["TOKENEXPIRATION"] = None
        cls.__TOKENCONFIG["ISTOKENSET"] = False
    
    @classmethod
    def update_token_threshold(cls, threshold: int):
        """
        Updates the token threshold
        """
        if int(threshold) < 0:
            raise InvalidDataException("Threshold must be a positive integer")
        cls.__TOKENCONFIG["THRESHOLD"] = int(threshold)
        cls.reset_token_config()


    def do_get(self: object, url_path: str, authorization: str=None) -> tuple:
        """A low level GET request to the Monnify API

        Args:
            self (object): The class instance
            url_path (str): The API url being requested
            authorization (str): A bearer token for authorizing the request

        Raises:
            UnprocessableRequestException: This is thrown when the API request cannot be processed
            GatewayException: This is thrown when there's a server error with the API
            RequestException: This is thrown when there's an issue with the API request
            Exception: A general exception

        Returns:
            tuple: API status code, and a json response
        """    

        url: str = self.__base_url + url_path
        headers: dict = self.__headers
        if authorization is None:
            _, authorization = self.get_auth_token()
            authorization = authorization["accessToken"]
        headers["Authorization"] = f"Bearer {authorization}"

        try:
            response = requests.get(url=url, headers=headers)
            if response.status_code == 200:
                return response.status_code, response.json()
            elif response.status_code >= 400 and response.status_code < 500:
                raise UnprocessableRequestException(response.text, response.status_code)
            elif response.status_code >= 500:
                raise GatewayException(response.text, response.status_code)
            else:
                raise RequestException(response.status_code, response.text)
        except Exception as e:
            raise GlobalException(e)


    def do_post(self: object, url_path: str, data: dict, authorization: str=None) -> tuple:
        """A low level POST request to the Monnify API

        Args:
            self (object): The class instance
            url_path (str): The API url being requested
            authorization (str): A bearer token for authorizing the request
            data (dict): A dictionary of request payload to be sent to the API

        Raises:
            UnprocessableRequestException: _description_
            GatewayException: _description_
            RequestException: _description_
            Exception: _description_

        Returns:
            tuple: API status code, and a json response
        """ 

        url: str = self.__base_url + url_path
        headers: dict = self.__headers
        if authorization is None:
            _, authorization = self.get_auth_token()
            authorization = authorization["accessToken"]
        headers["Authorization"] = f"Bearer {authorization}"

        try:
            response = requests.post(url=url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                return response.status_code, response.json()
            elif response.status_code >= 400 and response.status_code < 500:
                raise UnprocessableRequestException(response.text, response.status_code)
            elif response.status_code >= 500:
                raise GatewayException(response.text, response.status_code)
            else:
                raise RequestException(response.status_code, response.text)
        except Exception as e:
            raise GlobalException(e)


    def do_put(self: object, url_path: str, data: dict, authorization: str=None) -> tuple:
        """A low level PUT request to the Monnify API

        Args:
            self (object): The class instance
            url_path (str): The API url being requested
            authorization (str): A bearer token for authorizing the request
            data (dict): A dictionary of request payload to be sent to the API

        Raises:
            UnprocessableRequestException: _description_
            GatewayException: _description_
            RequestException: _description_
            Exception: _description_

        Returns:
            tuple: API status code, and a json response
        """ 

        url: str = self.__base_url + url_path
        headers: dict = self.__headers
        if authorization is None:
            _, authorization = self.get_auth_token()
            authorization = authorization["accessToken"]
        headers["Authorization"] = f"Bearer {authorization}"

        try:
            response = requests.put(url=url, headers=headers, data=json.dumps(data))
            if response.status_code == 200:
                return response.status_code, response.json()
            elif response.status_code >= 400 and response.status_code < 500:
                raise UnprocessableRequestException(response.text, response.status_code)
            elif response.status_code >= 500:
                raise GatewayException(response.text, response.status_code)
            else:
                raise RequestException(response.status_code, response.text)
        except Exception as e:
            raise GlobalException(e)


    def do_delete(self: object, url_path: str, authorization: str=None) -> tuple:
        """A low level Delete request to the Monnify API

        Args:
            self (object): The class instance
            url_path (str): The API url being requested
            authorization (str): A bearer token for authorizing the request

        Raises:
            UnprocessableRequestException: This is thrown when the API request cannot be processed
            GatewayException: This is thrown when there's a server error with the API
            RequestException: This is thrown when there's an issue with the API request
            Exception: A general exception

        Returns:
            tuple: API status code, and a json response
        """        

        url: str = self.__base_url + url_path
        headers: dict = self.__headers
        if authorization is None:
            _, authorization = self.get_auth_token()
            authorization = authorization["accessToken"]
        headers["Authorization"] = f"Bearer {authorization}"

        try:
            response = requests.delete(url=url, headers=headers)
            if response.status_code == 200:
                return response.status_code, response.json()
            elif response.status_code >= 400 and response.status_code < 500:
                raise UnprocessableRequestException(response.text, response.status_code)
            elif response.status_code >= 500:
                raise GatewayException(response.text, response.status_code)
            else:
                raise RequestException(response.status_code, response.text)
        except Exception as e:
            raise GlobalException(e)


    def compare_hash(self: object, payload: bytes, monnify_signature: str) -> bool:
        """
        Webhook signature comparison utility

        Args:
            self (object): The class instance
            payload (bytes): Webhook payload in byte sent from Monnify
            monnify_signature (str): A string of the webhook hash from Monnify

        Returns:
            bool: A boolean value denoting if there's a match between the computed hash and Monnify's
        """        

        secret_key_bytes: bytes = self.__secret_key.encode("utf-8")
        hash_in_bytes: bytes = hmac.new(
            secret_key_bytes, msg=payload, digestmod=hashlib.sha512
        )
        hash_in_hex: str = hash_in_bytes.hexdigest()
        return hmac.compare_digest(hash_in_hex, monnify_signature)
