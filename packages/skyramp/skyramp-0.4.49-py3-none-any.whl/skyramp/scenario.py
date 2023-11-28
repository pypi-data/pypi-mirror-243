"""
Contains helpers for interacting with Skyramp testing scenarios.
"""

import ctypes
import json
import os
import yaml

from skyramp.utils import _library, _call_function
from skyramp.endpoint import _Endpoint
from skyramp.test_request import _Request
from skyramp.test_assert import _Assert

class _Step:
    def __init__(self, step, max_retries=0, interval="", until="") -> None:
        self.step = step
        self.max_retries = max_retries
        self.interval = interval
        self.until = until
        self.response_value = ''
        self.response_code = 0

    def set_value(self, response_value: json):
        """
        Sets the response value for this step
        """
        self.response_value = response_value

    def get_request(self):
        """
        Gets the request value for this step
        """
        if self.step is not None and isinstance(self.step , _Request):
            if not self.step.name.startswith("requests."):
                return f"requests.{self.step.name}"
            return f"{self.step.name}"
        raise Exception("Step is not a request")

    def get_response_code(self):
        """
        Gets the response value for this step
        """
        request = self.get_request()
        return f"{request}.code"

    def get_response_value(self, json_path: str):
        """
        Gets the response value for this step
        """
        request = self.get_request()
        return f"{request}.res.{json_path}"

    def to_json(self):
        """
        Convert the object to dictionary
        """
        step_dict = self.step.to_json()

        if self.max_retries or self.interval or self.until:
            step_dict["repeat"] = {}
        if self.max_retries:
            step_dict["repeat"]["maxRetries"] = self.max_retries
        if self.interval:
            step_dict["repeat"]["interval"] = self.interval
        if self.until:
            step_dict["repeat"]["until"] = self.until
        return step_dict

class _Scenario:
    """
    Represents a testing scenario.
    """
    def __init__(self, name: str, start_at: int=1) -> None:
        self.name = name

        self.steps = []
        self.steps_v1 = []

        self.global_headers = {}

        self.services = []
        self.endpoints = []
        self.requests = []
        self.start_at = start_at

    def add_request(
        self,
        endpoint: _Endpoint,
        method_name: str,
        request_object = None,
        dynamic: bool = False,
    ) -> str:
        """
        Adds a request to this scenario.
        endpoint: The endpoint object associated with the request
        method_name: The name of the method that this request will be hitting
        request_object: Map containing request information
        dynamic: Whether or not the request_object is a dynamic script

        Returns the request name
        """
        self._build_metadata_for_endpoint(endpoint)

        for request in self.requests:
            if request["methodName"] != method_name:
                continue

            if dynamic:
                request["javascriptPath"] = request_object
                request.pop("blob", None)
            elif request_object is not None:
                request["blob"] = request_object["requestValue"]["blob"]
            self.steps += [{"requestName": request["name"]}]
            return request["name"]

    def add_request_from_file(
        self, endpoint: _Endpoint, method_name: str, request_file: str
    ) -> str:
        """
        Adds the request in the specified file to the corresponding endpoint and method.
        """
        _, file_ext = os.path.splitext(request_file)

        try:
            with open(request_file) as file:
                file_contents = file.read()
        except:
            raise Exception(f"failed to open file: {request_file}")
        # pylint: disable=duplicate-code
        dynamic = False

        if file_ext == ".json":
            data = json.loads(file_contents)
        elif file_ext in [".yaml", ".yml"]:
            data = yaml.safe_load(file_contents)
        elif file_ext == ".js":
            dynamic = True
            data = request_file
        else:
            raise Exception(
                f"unsupported file format: {file_ext}. Only JSON, YAML, and JS are supported"
            )

        return self.add_request(endpoint, method_name, data, dynamic)

    def add_assert_equal(self, value_name: str, expected_value: str):
        """
        Adds an assert equal given the value expression and expected value
        """
        assertion = f'requests.{value_name} == "{expected_value}"'
        self.steps.append({"asserts": assertion})

    def add_assert_v1(
        self,
        assert_value: str='',
        assert_expected_value: str='',
        assert_step: _Assert=None,
        max_retries: int = 0,
        interval: str= "",
        until: str=""
    ):
        """
        Adds an assert given the value expression and expected value
        """
        if assert_step is not None:
            self.steps_v1.append(_Step(assert_step, max_retries, interval, until))
        else:
            assert_step = _Assert(assert_value, assert_expected_value)
            self.steps_v1.append(_Step(assert_step, max_retries, interval, until))


    def _build_metadata_for_endpoint(self, endpoint: _Endpoint):
        if endpoint.endpoint in self.endpoints:
            return

        self.services += endpoint.services

        self.endpoints.append(endpoint.endpoint)

        mock_description_yaml = yaml.dump(endpoint.mock_description)

        func = _library.buildRequestsWrapper
        argtypes = [ctypes.c_char_p]
        restype = ctypes.c_char_p

        requests = _call_function(
            func, argtypes, restype, [mock_description_yaml.encode()], return_output=True
        )

        parsed_requests = json.loads(requests)
        self.requests.append(parsed_requests[0])

    def set_global_headers(self, headers):
        """
        Sets the global headers for this scenario
        """
        self.global_headers = headers

    def add_request_v1(
        self,
        request: _Request,
        max_retries: int = 0,
        interval: str= "",
        until: str=""
    ) -> _Step:
        """
        Adds a request to this scenario.
        endpoint: The endpoint object associated with the request
        method_name: The name of the method that this request will be hitting
        request_object: Map containing request information
        dynamic: Whether or not the request_object is a dynamic script

        Returns the request name
        """
        step = _Step(request, max_retries, interval, until)
        self.steps_v1.append(step)
        return step
    