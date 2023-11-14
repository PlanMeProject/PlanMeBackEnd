import logging
from urllib.parse import parse_qs, urlparse

import requests
from decouple import config
from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.app.models import User


class AuthorizationViewSet(viewsets.ViewSet):
    @staticmethod
    def extract_authorization_code(full_url):
        parsed_url = urlparse(full_url)
        query_params = parse_qs(parsed_url.query)
        authorization_code = query_params.get("code", [None])[0]
        return authorization_code

    @staticmethod
    def exchange_code_for_token(authorization_code):
        token_url = config("TOKEN_URL")
        client_id = config("GOOGLE_CLIENT_ID")
        client_secret = config("GOOGLE_CLIENT_SECRET")
        redirect_uri = config("REDIRECT_URI")

        data = {
            "code": authorization_code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"(Exchange) Error fetching user profile: Status Code:"
                f" {response.status_code}, Response: {response.text}, "
                f"code: {authorization_code}"
            )

    @staticmethod
    def get_user_profile(access_token):
        url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(
                f"(Profile) Error fetching user profile: Status Code:"
                f" {response.status_code}, Response: {response.text}"
            )

    def create(self, request, *args, **kwargs):
        full_url = request.data.get("full_url")
        if not full_url:
            return Response({"error": "Full URL not provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            authorization_code = self.extract_authorization_code(full_url)
            tokens = self.exchange_code_for_token(authorization_code)
            user_profile = self.get_user_profile(tokens["access_token"])
            user_email = user_profile.get("email")

            user, created = User.objects.update_or_create(email=user_email, defaults={"email": user_email})

            request.session["access_token"] = tokens["access_token"]

            return Response({"user_id": user.id, "token": tokens["access_token"]}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logging.error(e)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
