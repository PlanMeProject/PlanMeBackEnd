# import logging
# from urllib.parse import parse_qs, urlparse
#
# from rest_framework import status, viewsets
# from rest_framework.response import Response
#
#
# class AuthorizeSessionViewSet(viewsets.ViewSet):
#     @staticmethod
#     def extract_authorization_code(full_url):
#         parsed_url = urlparse(full_url)
#         query_params = parse_qs(parsed_url.query)
#         authorization_code = query_params.get("code", [None])[0]
#         return authorization_code
#
#     def create(self, request, *args, **kwargs):
#         full_url = request.data.get("full_url")
#         if not full_url:
#             return Response({"error": "Full URL not provided"}, status=status.HTTP_400_BAD_REQUEST)
#
#         try:
#             authorization_code = self.extract_authorization_code(full_url)
#             request.session["authorization_code"] = authorization_code
#
#             return Response(
#                 {"message": f"Authorization code received: {authorization_code}"}, status=status.HTTP_200_OK
#             )
#
#         except Exception as e:
#             logging.error(e)
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
