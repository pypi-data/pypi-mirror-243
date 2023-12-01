import logging

from requests import Session
from requests.adapters import HTTPAdapter, Retry

from MSApi.exceptions import *
from MSApi.properties import *
import requests
import urllib.parse

from datetime import datetime

ms_url = "https://api.moysklad.ru/api/remap/1.2"


def error_handler(response: requests.Response, expected_code=200):
    code = response.status_code
    if code == expected_code:
        return

    raise MSApiHttpException(response)


def string_to_datetime(string):
    value = datetime.strptime('%Y-%m-%d %H:%M:%S.%f', string + "000")
    return value


def caching(f):
    cache = [None]

    def decorate(cls, *args, cached=False, **kwargs):
        if cached is True:
            if cache[0] is None:
                cache[0] = list(f(cls, *args, **kwargs))
            return (a for a in cache[0])
        else:
            return f(cls, *args, **kwargs)

    return decorate


class Authorizer:
    token = None

    @classmethod
    def login(cls, login: str, password: str, session=Session()):
        import base64
        auch_base64 = base64.b64encode(f"{login}:{password}".encode('utf-8')).decode('utf-8')

        response = session.post(f"{ms_url}/security/token",
                                headers={"Authorization": f"Basic {auch_base64}", "Accept-Encoding": "gzip"})
        error_handler(response, 201)
        cls.token = str(response.json()["access_token"])

    @classmethod
    def is_auch(cls) -> bool:
        return cls.token is not None


def _create_session():
    session = Session()
    session.mount('https://',
                  HTTPAdapter(max_retries=Retry(total=10, status_forcelist=[500, 503])))
    return session


class MSLowApi:
    __session = _create_session()
    __authorizer = Authorizer()

    @classmethod
    def set_access_token(cls, access_token):
        cls.__authorizer.token = access_token

    @classmethod
    def login(cls, login: str, password: str):
        cls.__authorizer.login(login, password, cls.__session)

    @classmethod
    def check_login(cls, f):
        if cls.__authorizer.is_auch():
            raise MSApiException("Login first")
        return f

    @classmethod
    def get_json_by_href(cls, href):
        response = cls._auch_get_by_href(href)
        error_handler(response)
        return response.json()

    @classmethod
    # @check_login
    def auch_post(cls, request, **kwargs):
        logging.debug(f"MSApi POST: {request}")
        request = urllib.parse.quote(request)
        return cls.__session.post(f"{ms_url}/{request}",
                                  headers={"Authorization": f"Bearer {cls.__authorizer.token}",
                                           "Content-Type": "application/json", "Accept-Encoding": "gzip"},
                                  **kwargs)

    @classmethod
    def auch_get(cls, request, **kwargs):
        logging.debug(f"MSApi GET: {request}")
        urllib.parse.quote(request)
        return cls._auch_get_by_href(f"{ms_url}/{request}", **kwargs)

    @classmethod
    def auch_put(cls, request, **kwargs):
        logging.debug(f"MSApi PUT: {request}")
        request = urllib.parse.quote(request)
        return cls.__session.put(f"{ms_url}/{request}",
                                 headers={"Authorization": f"Bearer {cls.__authorizer.token}",
                                          "Content-Type": "application/json", "Accept-Encoding": "gzip"},
                                 **kwargs)

    @classmethod
    # @check_login
    def _auch_get_by_href(cls, request,
                          limit: int = None,
                          offset: int = None,
                          search: Search = None,
                          orders: Order = None,
                          filters: Filter = None,
                          expand: Expand = None, **kwargs):
        params = []
        if limit is not None:
            params.append("limit={}".format(limit))
        if offset is not None:
            params.append("offset={}".format(offset))
        if search is not None:
            params.append(str(search))
        if filters is not None:
            params.append(str(filters))
        if orders is not None:
            params.append(str(orders))
        if expand is not None:
            params.append(str(expand))
        params_str = ""
        if params:
            params_str = f"?{'&'.join(params)}"

        return cls.__session.get(f"{request}{params_str}",
                                 headers={"Authorization": f"Bearer {cls.__authorizer.token}",
                                          "Content-Type": "application/json", "Accept-Encoding": "gzip"},
                                 **kwargs)

    @classmethod
    def gen_objects(cls, request, obj, limit: int = None, expand: Expand = None, **kwargs):

        local_limit = 1000
        if limit is not None and limit < 1000:
            local_limit = limit

        if expand is not None:
            local_limit = 100

        offset = 0
        while True:
            response = cls.auch_get(request, limit=local_limit, offset=offset, expand=expand, **kwargs)
            error_handler(response)
            row_counter = 0
            for row in response.json().get('rows'):
                yield obj(row)
                row_counter += 1
            if row_counter == 0:
                break
            offset += local_limit
            if limit is None:
                continue
            limit -= local_limit
            if limit < local_limit:
                local_limit = limit
            if local_limit == 0:
                break
