from .exception_handler import exception_handler
from .common import (
    build_input_schema_from_strada_param_definitions,
    hydrate_input_fields,
    validate_http_input,
    fill_path_params,
)
import requests


class GmailCustomHttpActionBuilder:
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

    def set_headers(self, headers):
        self._instance.headers = headers
        return self

    def set_path_params(self, path_params):
        self._instance.path = path_params
        return self

    def set_query_params(self, params):
        self._instance.query = params
        return self

    def set_body(self, body):
        self._instance.body = body
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = GmailCustomHttpAction()
        return self._instance


class GmailCustomHttpAction:
    def __init__(self):
        self.param_schema_definition = None
        self.url = None
        self.method = None
        self.token = None
        self.headers = "{}"
        self.path = "{}"
        self.query = "{}"
        self.body = "{}"

    @exception_handler
    def execute(self, **kwargs):
        validate_http_input(self.param_schema_definition, **kwargs)

        path_params = hydrate_input_fields(
            self.param_schema_definition, self.path, **kwargs
        )
        headers = hydrate_input_fields(
            self.param_schema_definition, self.headers, **kwargs
        )
        query_params = hydrate_input_fields(
            self.param_schema_definition, self.query, **kwargs
        )
        body = hydrate_input_fields(self.param_schema_definition, self.body, **kwargs)

        headers["Authorization"] = f"Bearer {self.token}"

        url = fill_path_params(self.url, path_params)

        if self.method == "post":
            response = requests.post(
                url, headers=headers, params=query_params, json=body
            )
            return response.json()
        elif self.method == "get":
            response = requests.get(url, headers=headers, params=query_params)
            return response.json()
        elif self.method == "put":
            response = requests.put(
                url, headers=headers, params=query_params, json=body
            )
            return response.json()
        elif self.method == "delete":
            response = requests.delete(url, headers=headers, params=query_params)
            return response.json()

    @staticmethod
    def prepare(data):
        builder = GmailCustomHttpActionBuilder()
        return (
            builder.set_param_schema(data["param_schema_definition"])
            .set_url(data["url"])
            .set_method(data["method"])
            .set_token(data["access_token"])
            .set_path_params(data.get("path", "{}"))
            .set_headers(data.get("headers", "{}"))
            .set_query_params(data.get("query", "{}"))
            .set_body(data.get("body", "{}"))
            .build()
        )
