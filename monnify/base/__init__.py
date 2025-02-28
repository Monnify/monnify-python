import requests
import hmac
import hashlib


class Base:
    
    def __init__(
        self: object, API_KEY: str = None, SECRET_KEY: str = None, ENV: str = "SANDBOX"
    ) -> None:

        self.__headers = {"Content-Type": "application/json"}

        if API_KEY is None or SECRET_KEY is None:
            raise Exception("Cannot instantiate base class without API or Secret key")
        elif ENV == "SANDBOX":
            if API_KEY.strip().startswith() != "MK_TEST":
                raise Exception("Can only use test API_KEY for sandbox environment")
            else:
                self.__env = "SANDBOX"
                self.__api_key = API_KEY.strip()
                self.__secret_key = SECRET_KEY.strip()
                self.__base_url = "https://sandbox.monnify.com"
        elif ENV == "LIVE":
            if API_KEY.strip().startswith() != "MK_PROD":
                raise Exception("Can only use live API_KEY for live environment")
            else:
                self.__env = "LIVE"
                self.__api_key = API_KEY.strip()
                self.__secret_key = SECRET_KEY.strip()
                self.__base_url = "https://api.monnify.com"
        else:
            raise Exception(
                "Unkwown environment supplied, either supply 'SANDBOX' or 'LIVE'"
            )

    def do_get(self: object, url_path: str, authorization: str) -> tuple:
        url: str = self.__base_url + url_path
        headers: dict = self.__headers
        headers["Authorization"] = f"Bearer {authorization}"
        try:
            response = requests.get(url=url, headers=headers)
            return response.status_code, response.json()
        except Exception as e:
            print(e)
            raise Exception(e)

    def do_post(self: object, url_path: str, authorization: str, data: dict) -> tuple:
        url: str = self.__base_url + url_path
        headers: dict = self.__headers
        headers["Authorization"] = f"Bearer {authorization}"
        try:
            response = requests.post(url=url, headers=headers, data=data)
            return response.status_code, response.json()
        except Exception as e:
            print(e)
            raise Exception(e)

    def do_put(self: object, url_path: str, authorization: str, data: dict) -> tuple:
        url: str = self.__base_url + url_path
        headers: dict = self.__headers
        headers["Authorization"] = f"Bearer {authorization}"
        try:
            response = requests.put(url=url, headers=headers, data=data)
            return response.status_code, response.json()
        except Exception as e:
            print(e)
            raise Exception(e)

    def do_delete(self: object, url_path: str, authorization: str) -> tuple:
        url: str = self.__base_url + url_path
        headers: dict = self.__headers
        headers["Authorization"] = f"Bearer {authorization}"
        try:
            response = requests.delete(url=url, headers=headers)
            return response.status_code, response.json()
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
