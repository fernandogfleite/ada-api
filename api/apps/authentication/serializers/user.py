from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers


class JWTSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_confirmed:
            raise serializers.ValidationError(
                {
                    "message": "User is not confirmed yet. Please check your email."
                }
            )

        data['is_student'] = self.user.is_student
        data['is_teacher'] = self.user.is_teacher
        data['is_secretary'] = self.user.is_secretary

        return data
