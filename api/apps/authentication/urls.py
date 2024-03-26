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
    path(
        'me/',
        user.UserDetailView.as_view(),
        name='user_detail'
    ),
    path(
        'me/change-password/',
        user.UserChangePasswordView.as_view(),
        name='user_change_password'
    ),
    path(
        'confirm/<str:token>/',
        user.UserConfirmView.as_view(),
        name='confirm_user'
    ),
    path(
        'resend-confirm/',
        user.UserResendConfirmView.as_view(),
        name='resend_confirm_user'
    ),
    path(
        'token/',
        TokenObtainPairView.as_view(serializer_class=JWTSerializer),
        name='token_obtain_pair'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        'password_reset/',
        reset_password_request_token,
        name="reset_password"
    ),
    path(
        'password_reset/confirm/',
        reset_password_confirm,
        name="reset_password_confirm"
    ),
    path(
        'student/register/',
        user.StudentRegisterViewSet.as_view({'post': 'create'}),
        name='register_student'
    ),
    path(
        'teacher/register/',
        user.TeacherRegisterViewSet.as_view({'post': 'create'}),
        name='register_teacher'
    ),
    path(
        'secretary/register/',
        user.SecretaryRegisterViewSet.as_view({'post': 'create'}),
        name='register_secretary'
    ),
    path(
        'teachers/',
        user.ListTeachersView.as_view(),
        name='list_teachers'
    ),
]
