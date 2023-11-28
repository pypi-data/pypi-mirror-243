"""
Contains helpers for interacting with Skyramp mock description.
"""

from typing import List
from skyramp.service import _Service as Service
from skyramp.endpoint import _Endpoint as Endpoint
from skyramp.response import _ResponseValue as ResponseValue

class _MockDescription:
    def __init__(
            self,
            version: str,
            responses: List[ResponseValue],
            endpoints: List[Endpoint],
            services: List[Service]) -> None:
        self.version = version
        self.responses = responses
        self.endpoints = endpoints
        self.services = services

    def to_json(self):
        """
        Convert the object to a JSON string.
        """
        return {
            "version": self.version,
            "responses": self.responses,
            "services": self.services,
            "endpoints": self.endpoints,
        }
