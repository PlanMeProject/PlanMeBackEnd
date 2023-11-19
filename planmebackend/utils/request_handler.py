"""The module for handling HTTP requests."""
import logging

import requests


class HTTPRequestHandler:
    """The class for handling HTTP requests."""

    @staticmethod
    def make_request(method, url, headers=None, data=None):
        """Make a HTTP request."""
        try:
            response = requests.request(
                method, url, headers=headers, data=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP Request Error: {e.response.text}")
            raise Exception(f"HTTP Request failed: {e.response.text}")
