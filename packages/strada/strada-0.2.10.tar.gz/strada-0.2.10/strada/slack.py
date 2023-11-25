import json
from .exception_handler import exception_handler
from .common import (
    build_input_schema_from_strada_param_definitions,
    hydrate_input_fields,
    validate_http_input,
)
import requests


class PostMessageActionBuilder:
    def __init__(self):
        self._instance = None

    def set_token(self, token):
        self._get_instance().token = token
        return self

    def set_channel(self, channel):
        self._get_instance().channel = channel
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = PostMessageAction()
        return self._instance


class PostMessageAction:
    def __init__(self):
        self.token = None
        self.channel = None

    def execute(self, text):
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-type": "application/json",
        }
        payload = json.dumps({"channel": self.channel, "text": text})
        response = requests.post(
            "https://slack.com/api/chat.postMessage", headers=headers, data=payload
        )
        return response.json()

    @staticmethod
    def prepare(data):
        builder = PostMessageActionBuilder()
        return (
            builder.set_token(data["access_token"]).set_channel(data["channel"]).build()
        )


class CreateConversationActionBuilder:
    def __init__(self):
        self._instance = None

    def set_token(self, token):
        self._get_instance().token = token
        return self

    def set_is_private(self, is_private):
        self._get_instance().is_private = is_private
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = CreateConversationAction()
        return self._instance


class CreateConversationAction:
    def __init__(self):
        self.token = None
        self.is_private = None

    def execute(self, name):
        headers = {"Authorization": f"Bearer {self.token}"}
        payload = {"name": name, "is_private": self.is_private}
        response = requests.post(
            "https://slack.com/api/conversations.create",
            headers=headers,
            data=payload,
        )
        return response.json()

    @staticmethod
    def prepare(data):
        builder = CreateConversationActionBuilder()
        return (
            builder.set_token(data["access_token"])
            .set_is_private(data["is_private"])
            .build()
        )


class SlackCustomHttpGetActionBuilder:
    def __init__(self):
        self._instance = None

    def set_url(self, url):
        self._get_instance().url = url
        return self

    def set_token(self, access_token):
        self._get_instance().token = access_token
        return self

    def set_headers(self, headers):
        self._instance.headers = json.loads(headers)
        return self

    def set_params(self, params):
        self._instance.params = json.loads(params)
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = SlackCustomHttpGetAction()
        return self._instance


class SlackCustomHttpGetAction:
    def __init__(self):
        self.url = None
        self.token = None
        self.headers = {}
        self.params = {}

    def execute(self, get_payload: dict):
        self.headers["Authorization"] = f"Bearer {self.token}"

        if get_payload.get("dynamic_params"):
            for key, value in get_payload["dynamic_params"].items():
                self.params[key] = value

        if get_payload.get("dynamic_headers"):
            for key, value in get_payload["dynamic_headers"].items():
                self.headers[key] = value

        response = requests.get(
            self.url,
            headers=self.headers,
            params=self.params,
        )
        return response.json()

    @staticmethod
    def prepare(data):
        builder = SlackCustomHttpGetActionBuilder()
        return (
            builder.set_url(data["url"])
            .set_headers(data.get("headers", {}))
            .set_params(data.get("params", {}))
            .set_token(data["access_token"])
            .build()
        )


class SlackCustomHttpPostActionBuilder:
    def __init__(self):
        self._instance = None

    def set_url(self, url):
        self._get_instance().url = url
        return self

    def set_token(self, access_token):
        self._get_instance().token = access_token
        return self

    def set_headers(self, headers):
        self._instance.headers = json.loads(headers)
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = SlackCustomHttpPostAction()
        return self._instance


# SlackCustomHttpPostAction
class SlackCustomHttpPostAction:
    def __init__(self):
        self.url = None
        self.token = None
        self.headers = {}

    def execute(self, post_payload: dict):
        self.headers["Authorization"] = f"Bearer {self.token}"

        if post_payload.get("dynamic_headers"):
            for key, value in post_payload["dynamic_params"].items():
                self.params[key] = value

        if not post_payload.get("body"):
            print("Error: No 'body' provided in 'post_payload'")
            return {}

        response = requests.post(
            self.url, headers=self.headers, data=post_payload["body"]
        )
        return response.json()

    @staticmethod
    def prepare(data):
        builder = SlackCustomHttpPostActionBuilder()
        return (
            builder.set_url(data["url"])
            .set_headers(data.get("headers", {}))
            .set_token(data["access_token"])
            .build()
        )


class SlackCustomHttpActionBuilder:
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
            self._instance = SlackCustomHttpAction()
        return self._instance


class SlackCustomHttpAction:
    def __init__(self):
        self.param_schema_definition = None
        self.url = None
        self.method = None
        self.token = None
        self.headers = "{}"
        self.params = "{}"
        self.body = "{}"

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

        headers["Authorization"] = f"Bearer {self.token}"

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
        elif self.method == "delete":
            response = requests.delete(self.url, headers=headers, params=query_params)
            return response.json()

    @staticmethod
    def prepare(data):
        builder = SlackCustomHttpActionBuilder()
        return (
            builder.set_param_schema(data["param_schema_definition"])
            .set_url(data["url"])
            .set_method(data["method"])
            .set_token(data["access_token"])
            .set_headers(data.get("headers", "{}"))
            .set_params(data.get("params", "{}"))
            .set_body(data.get("body", "{}"))
            .build()
        )
