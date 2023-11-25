import requests
import json
from .exception_handler import exception_handler
from .common import (
    basic_auth_str,
    build_input_schema_from_strada_param_definitions,
    hydrate_input_fields,
    validate_http_input,
)
import requests


class GetActionBuilder:
    def __init__(self):
        self._instance = GetAction()

    def set_base_url(self, base_url):
        self._instance.base_url = base_url
        return self

    def set_endpoint(self, endpoint):
        self._instance.endpoint = endpoint
        return self

    def set_headers(self, headers):
        self._instance.headers = json.loads(headers)
        return self

    def set_params(self, params):
        self._instance.params = json.loads(params)
        return self

    def build(self):
        return self._instance


class GetAction:
    def __init__(self):
        self.base_url = None
        self.endpoint = None
        self.headers = {}
        self.params = {}

    def execute(self):
        url = f"{self.base_url}/{self.endpoint}"
        response = requests.get(url, headers=self.headers, params=self.params)
        return response.json()

    @staticmethod
    def prepare(data):
        builder = GetActionBuilder()
        return (
            builder.set_base_url(data["base_url"])
            .set_endpoint(data["endpoint"])
            .set_headers(data["headers"])
            .set_params(data["params"])
            .build()
        )


class PatchActionBuilder:
    def __init__(self):
        self._instance = PatchAction()

    def set_base_url(self, base_url):
        self._instance.base_url = base_url
        return self

    def set_endpoint(self, endpoint):
        self._instance.endpoint = endpoint
        return self

    def set_headers(self, headers):
        self._instance.headers = json.loads(headers)
        return self

    def build(self):
        return self._instance


class PatchAction:
    def __init__(self):
        self.base_url = None
        self.endpoint = None
        self.headers = {}

    def execute(self, payload):
        url = f"{self.base_url}/{self.endpoint}"
        response = requests.patch(url, headers=self.headers, json=payload)
        return response.json()

    @staticmethod
    def prepare(data):
        builder = PatchActionBuilder()
        return (
            builder.set_base_url(data["base_url"])
            .set_endpoint(data["endpoint"])
            .set_headers(data["headers"])
            .build()
        )


class PostActionBuilder:
    def __init__(self):
        self._instance = PostAction()

    def set_base_url(self, base_url):
        self._instance.base_url = base_url
        return self

    def set_endpoint(self, endpoint):
        self._instance.endpoint = endpoint
        return self

    def set_headers(self, headers):
        self._instance.headers = json.loads(headers)
        return self

    def build(self):
        return self._instance


class PostAction:
    def __init__(self):
        self.base_url = None
        self.endpoint = None
        self.headers = {}

    def execute(self, payload):
        url = f"{self.base_url}/{self.endpoint}"
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    @staticmethod
    def prepare(data):
        builder = PostActionBuilder()
        return (
            builder.set_base_url(data["base_url"])
            .set_endpoint(data["endpoint"])
            .set_headers(data["headers"])
            .build()
        )


class PutActionBuilder:
    def __init__(self):
        self._instance = PutAction()

    def set_base_url(self, base_url):
        self._instance.base_url = base_url
        return self

    def set_endpoint(self, endpoint):
        self._instance.endpoint = endpoint
        return self

    def set_headers(self, headers):
        self._instance.headers = json.loads(headers)
        return self

    def build(self):
        return self._instance


class PutAction:
    def __init__(self):
        self.base_url = None
        self.endpoint = None
        self.headers = {}

    def execute(self, payload):
        url = f"{self.base_url}/{self.endpoint}"
        response = requests.put(url, headers=self.headers, json=payload)
        return response.json()

    @staticmethod
    def prepare(data):
        builder = PutActionBuilder()
        return (
            builder.set_base_url(data["base_url"])
            .set_endpoint(data["endpoint"])
            .set_headers(data["headers"])
            .build()
        )


class DeleteActionBuilder:
    def __init__(self):
        self._instance = DeleteAction()

    def set_base_url(self, base_url):
        self._instance.base_url = base_url
        return self

    def set_endpoint(self, endpoint):
        self._instance.endpoint = endpoint
        return self

    def set_headers(self, headers):
        self._instance.headers = json.loads(headers)
        return self

    def build(self):
        return self._instance


class DeleteAction:
    def __init__(self):
        self.base_url = None
        self.endpoint = None
        self.headers = {}

    def execute(self):
        url = f"{self.base_url}/{self.endpoint}"
        response = requests.delete(url, headers=self.headers)
        return response.status_code

    @staticmethod
    def prepare(data):
        builder = DeleteActionBuilder()
        return (
            builder.set_base_url(data["base_url"])
            .set_endpoint(data["endpoint"])
            .set_headers(data["headers"])
            .build()
        )


class CustomHttpActionBuilder:
    def __init__(self):
        self._instance = None

    def set_param_schema(self, param_schema):
        self._get_instance().param_schema_definition = (
            build_input_schema_from_strada_param_definitions(param_schema)
        )
        return self

    def set_url(self, url):
        self._get_instance().url = url
        return self

    def set_method(self, method):
        self._get_instance().method = method
        return self

    def set_token(self, access_token):
        self._get_instance().token = access_token
        return self

    def set_api_key(self, api_key):
        self._get_instance().api_key = api_key
        return self

    def set_basic_auth(self, basic_auth):
        self._get_instance().basic_auth = basic_auth
        return self

    def set_headers(self, headers):
        self._instance.headers = headers
        return self

    def set_params(self, params):
        self._instance.params = params
        return self

    def set_body(self, body):
        self._instance.body = body
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = CustomHttpAction()
        return self._instance


class CustomHttpAction:
    def __init__(self):
        self.param_schema_definition = None
        self.url = None
        self.method = None
        self.token = None
        self.api_key = None
        self.basic_auth = None
        self.headers = "{}"
        self.params = "{}"
        self.body = "{}"

    def _get_authorization_header(self):
        if self.api_key:
            return f"{self.api_key}"
        elif self.basic_auth:
            return basic_auth_str(
                username=self.basic_auth["username"],
                password=self.basic_auth["password"],
            )
        elif self.token:
            return f"Bearer {self.token}"

    @exception_handler
    def execute(self, **kwargs):
        validate_http_input(self.param_schema_definition, **kwargs)

        headers = hydrate_input_fields(
            self.param_schema_definition, self.headers, **kwargs
        )
        query_params = hydrate_input_fields(
            self.param_schema_definition, self.params, **kwargs
        )
        body = hydrate_input_fields(self.param_schema_definition, self.body, **kwargs)

        headers["Authorization"] = self._get_authorization_header()

        if self.method == "post":
            response = requests.post(
                self.url, headers=headers, params=query_params, data=body
            )
            return response.json()
        elif self.method == "get":
            response = requests.get(self.url, headers=headers, params=query_params)
            return response.json()
        elif self.method == "put":
            response = requests.put(
                self.url, headers=headers, params=query_params, data=body
            )
            return response.json()
        elif self.method == "patch":
            response = requests.patch(
                self.url, headers=headers, params=query_params, data=body
            )
            return response.json()
        elif self.method == "delete":
            response = requests.delete(self.url, headers=headers, params=query_params)
            return response.json()

    @staticmethod
    def prepare(data):
        builder = CustomHttpActionBuilder()
        return (
            builder.set_param_schema(data["param_schema_definition"])
            .set_url(data["url"])
            .set_method(data["method"])
            .set_token(data["access_token"])
            .set_api_key(data["api_key"])
            .set_basic_auth(data["basic_auth"])
            .set_headers(data.get("headers", "{}"))
            .set_params(data.get("params", "{}"))
            .set_body(data.get("body", "{}"))
            .build()
        )
