from .exception_handler import exception_handler
import openai as OpenAIApi
from .common import (
    build_input_schema_from_strada_param_definitions,
    hydrate_input_fields,
    validate_http_input,
    fill_path_params,
)
import requests


class CustomPromptActionBuilder:
    def __init__(self):
        self._instance = None

    def set_api_key(self, api_key):
        self._get_instance().api_key = api_key
        return self

    def set_model(self, model):
        self._get_instance().model = model
        return self

    def set_prompt(self, prompt):
        self._get_instance().prompt = prompt
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = CustomPromptAction()
        return self._instance


class CustomPromptAction:
    def __init__(self):
        self.api_key = None
        self.model = None
        self.prompt = None

    def execute(self, input_text: str):
        if not (self.api_key and self.prompt):
            raise Exception("Incomplete setup: Make sure to set api_key and prompt.")

        OpenAIApi.api_key = self.api_key
        chat_completion = OpenAIApi.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"{self.prompt}. input_text: `{input_text}`",
                }
            ],
        )

        return chat_completion.choices[0].message.content

    @staticmethod
    def prepare(data):
        builder = CustomPromptActionBuilder()
        return (
            builder.set_api_key(data["api_key"])
            .set_model(data["model"])
            .set_prompt(data["prompt"])
            .build()
        )


class SummarizeTextActionBuilder:
    def __init__(self):
        self._instance = None

    def set_api_key(self, api_key):
        self._get_instance().api_key = api_key
        return self

    def set_model(self, model):
        self._get_instance().model = model
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = SummarizeTextAction()
        return self._instance


class SummarizeTextAction:
    def __init__(self):
        self.api_key = None
        self.model = None

    def execute(self, input_text: str):
        if not self.api_key:
            raise Exception("Incomplete setup: Make sure to set api_key.")

        OpenAIApi.api_key = self.api_key

        # We specify a prompt that instructs the model to summarize the input text.
        chat_completion = OpenAIApi.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Please summarize the following text: `{input_text}`",
                }
            ],
        )

        return chat_completion.choices[0].message.content

    @staticmethod
    def prepare(data):
        builder = SummarizeTextActionBuilder()
        return builder.set_api_key(data["api_key"]).set_model(data["model"]).build()


class SentimentAnalysisActionBuilder:
    def __init__(self):
        self._instance = None

    def set_api_key(self, api_key):
        self._get_instance().api_key = api_key
        return self

    def set_model(self, model):
        self._get_instance().model = model
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = SentimentAnalysisAction()
        return self._instance


class SentimentAnalysisAction:
    def __init__(self):
        self.api_key = None
        self.model = None

    def execute(self, input_text: str):
        if not self.api_key:
            raise Exception("Incomplete setup: Make sure to set api_key.")

        OpenAIApi.api_key = self.api_key

        # Prompt instructs the model to classify the sentiment of the input text.
        chat_completion = OpenAIApi.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Classify the sentiment of the following text as either positive or negative: `{input_text}`",
                }
            ],
        )

        response_content = chat_completion.choices[0].message.content.lower()

        if "positive" in response_content:
            return "positive"
        elif "negative" in response_content:
            return "negative"
        else:
            return "neutral"

    @staticmethod
    def prepare(data):
        builder = SentimentAnalysisActionBuilder()
        return builder.set_api_key(data["api_key"]).set_model(data["model"]).build()


class ClassifyTextActionBuilder:
    def __init__(self):
        self._instance = None

    def set_api_key(self, api_key):
        self._get_instance().api_key = api_key
        return self

    def set_model(self, model):
        self._get_instance().model = model
        return self

    def set_labels(self, labels):
        self._get_instance().labels = labels.split(",")
        return self

    def build(self):
        return self._get_instance()

    def _get_instance(self):
        if self._instance is None:
            self._instance = ClassifyTextAction()
        return self._instance


class ClassifyTextAction:
    def __init__(self):
        self.api_key = None
        self.model = None
        self.labels = []

    def execute(self, input_text: str):
        if not (self.api_key and self.labels):
            raise Exception("Incomplete setup: Make sure to set api_key and labels.")

        OpenAIApi.api_key = self.api_key

        labels_str = ", ".join(self.labels)
        # Prompt instructs the model to classify the input_text into one of the given labels.
        chat_completion = OpenAIApi.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": f"Classify the following text into one of these categories: {labels_str}. Text: `{input_text}`",
                }
            ],
        )

        response_content = chat_completion.choices[0].message.content.lower()

        for label in self.labels:
            if label.lower() in response_content:
                return label

        return "Unable to classify"

    @staticmethod
    def prepare(data):
        builder = ClassifyTextActionBuilder()
        return (
            builder.set_api_key(data["api_key"])
            .set_model(data["model"])
            .set_labels(data["labels"])
            .build()
        )


class OpenAICustomHttpActionBuilder:
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
            self._instance = OpenAICustomHttpAction()
        return self._instance


class OpenAICustomHttpAction:
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
        builder = OpenAICustomHttpActionBuilder()
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
