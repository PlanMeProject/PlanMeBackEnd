"""The module defines the AuthorizationViewSet class."""
import logging

from rest_framework import status, viewsets
from rest_framework.response import Response

from planmebackend.app.models import User
from planmebackend.classroom.services import (
    AuthorizationError,
    AuthorizationService,
)


class AuthorizationViewSet(viewsets.ViewSet):
    """Class definition for AuthorizationViewSet."""

    def create(self, request, *args, **kwargs):
        """Create user and return token."""
        full_url = request.data.get("full_url")
        logging.info("Full URL: " + full_url)
        if not full_url:
            return Response(
                {"error": "Full URL not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            service = AuthorizationService()
            authorization_code = service.extract_authorization_code(full_url)
            if not authorization_code:
                raise AuthorizationError("Authorization code not found in URL")

            tokens = service.exchange_code_for_token(authorization_code)
            user_profile = service.get_user_profile(tokens["access_token"])
            user_email = user_profile.get("email")
            logging.info(f"User email: {user_email}")

            user, created = User.objects.update_or_create(
                email=user_email, defaults={"email": user_email}
            )
            return Response(
                {
                    "user_id": user.id,
                    "token": tokens["access_token"],
                    "email": user_email,
                },
                status=status.HTTP_201_CREATED,
            )

        except AuthorizationError as e:
            logging.error(f"Authorization error: {e}")
            return Response(
                {"error": str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logging.error(f"Internal Server Error: {e}")
            return Response(
                {"error": "Internal Server Error", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
