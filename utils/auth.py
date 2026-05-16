from rest_framework import status
from rest_framework.response import Response

class AuthRet:
  def __init__(self, is_auth, response=None, user=None):
    self.is_auth = is_auth
    self.response = response
    self.user = user

def authorize_user(user_model, user_info):
  if not user_info:
    return AuthRet(
      is_auth=False,
      response=Response(
        {"detail": "user field missing."},
        status=status.HTTP_400_BAD_REQUEST
      ))
  
  username = user_info.get("username")
  password = user_info.get("password")
  if not username or not password:
    return AuthRet(
      is_auth=False,
      response=Response(
        {"detail": "[username, password] fields missing in user"},
        status=status.HTTP_400_BAD_REQUEST,
      ))
  
  try:
    user = user_model.objects.get(username=username)
    if not user.check_password(password):
      return AuthRet(
        is_auth=False,
        response=Response(
          {"detail": "Password is incorrect."},
          status=status.HTTP_400_BAD_REQUEST,
        ),
      )
  except:
    return AuthRet(
      is_auth=False,
      response=Response(
        {"detail": "User Not found."}, status=status.HTTP_404_NOT_FOUND
      ))
  
  return AuthRet(is_auth=True, user=user)
