from api.apps.authentication.views import user
from api.apps.authentication.serializers.user import JWTSerializer

from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from django_rest_passwordreset.views import (
    reset_password_request_token,
    reset_password_confirm
)


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(
        serializer_class=JWTSerializer
    ), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password_reset/', reset_password_request_token, name="reset_password"),
    path('password_reset/confirm/', reset_password_confirm,
         name="reset_password_confirm"),
]
