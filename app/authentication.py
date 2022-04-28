from rest_framework.authentication import TokenAuthentication
from .models import *
from rest_framework import status, exceptions

class MyAuthentication(TokenAuthentication):
	model = Token

	def check_token(self, request):
		auth_token = request.META.get("HTTP_AUTHORIZATION")
		response = {}
		if auth_token == None or auth_token == '':
			# Token is blank or Token is required
			response['message'] = "Token is required."
			response['status'] = status.HTTP_401_UNAUTHORIZED
			raise exceptions.AuthenticationFailed(response)
		else:
			if not auth_token.startswith('Token '):
				# Token format is invalid
				response['message'] = "Token is invalid."
				response['status'] = status.HTTP_401_UNAUTHORIZED
				raise exceptions.AuthenticationFailed(response)
			# Fetching token key
			auth_token = auth_token.split(' ')
			return auth_token

	def authenticate(self, request):
		response = {}
		# Admin token authentication code
		# Calling function for checking auth token
		auth_token = self.check_token(request)

		# Checking token is valid or not
		token= Token.objects.filter(key=auth_token[1]).first()
		if not token:
			# Token value is invalid
			response['message'] = "Token is invalid."
			response['status'] = status.HTTP_401_UNAUTHORIZED
			raise exceptions.AuthenticationFailed(response)
		
		if token.user:
			if token.user.is_active == False:
				# user is blocked by admin
				response['message'] = "User is blocked."
				response['status'] = status.HTTP_401_UNAUTHORIZED
				raise exceptions.AuthenticationFailed(response)

		return self.authenticate_credentials(token)

	def authenticate_credentials(self, token):
		return (token.user, token)  