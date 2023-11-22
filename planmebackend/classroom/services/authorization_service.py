"""The module defines the AuthorizationService class."""
from urllib.parse import parse_qs, urlparse

from django.conf import settings

from planmebackend.utils.request_handler import HTTPRequestHandler


class AuthorizationError(Exception):
    """Custom Exception for authorization errors."""


class AuthorizationService:
    """Class definition for AuthorizationService."""

    @staticmethod
    def extract_authorization_code(full_url):
        """Extract authorization code from full url."""
        parsed_url = urlparse(full_url)
        query_params = parse_qs(parsed_url.query)
        return query_params.get("code", [None])[0]

    @staticmethod
    def exchange_code_for_token(authorization_code):
        """Exchange user authorization code for token."""
        token_url = settings.TOKEN_URL
        data = {
            "code": authorization_code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": "https://planme.vercel.app/google-auth",
            "grant_type": "authorization_code",
        }
        return HTTPRequestHandler.make_request("POST", token_url, data=data)

    @staticmethod
    def get_user_profile(access_token):
        """Get user profile."""
        url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        return HTTPRequestHandler.make_request("GET", url, headers=headers)
