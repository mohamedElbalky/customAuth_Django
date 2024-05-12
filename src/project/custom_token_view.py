from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

class CustomTokenObtainView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        try:
            user = get_user_model().objects.get(email=request.data["email"])
        except get_user_model().DoesNotExist:
            try:
                user = get_user_model().objects.get(phone_number=request.data["email"])
            except get_user_model().DoesNotExist:
                return response
        response.data["user"] = user.id
        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        try:
            user = get_user_model().objects.get(email=request.data["email"])
        except get_user_model().DoesNotExist:
            try:
                user = get_user_model().objects.get(phone_number=request.data["email"])
            except get_user_model().DoesNotExist:
                return response
        response.data["user"] = user.id
        return response
