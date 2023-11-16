import logging
from urllib.parse import parse_qs, urlparse

import requests
from django.conf import settings


class AuthorizationError(Exception):
    """Custom Exception for authorization errors."""


class AuthorizationService:
    @staticmethod
    def extract_authorization_code(full_url):
        parsed_url = urlparse(full_url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get("code", [None])[0]

    @staticmethod
    def exchange_code_for_token(authorization_code):
        token_url = settings.TOKEN_URL
        response = AuthorizationService._make_post_request(
            token_url,
            data={
                "code": authorization_code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        return response

    @staticmethod
    def get_user_profile(access_token):
        url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        return AuthorizationService._make_get_request(url, headers=headers)

    @staticmethod
    def _make_get_request(url, headers=None):
        response = requests.get(url, headers=headers)
        return AuthorizationService._handle_response(response)

    @staticmethod
    def _make_post_request(url, data, headers=None):
        response = requests.post(url, data=data, headers=headers)
        return AuthorizationService._handle_response(response)

    @staticmethod
    def _handle_response(response):
        if response.status_code == 200:
            return response.json()
        else:
            logging.error(f"API Request Error: {response.text}")
            raise AuthorizationError(f"API Request failed: {response.text}")
