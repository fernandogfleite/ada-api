from api.apps.classroom.models.classroom import (
    Period
)

from rest_framework import serializers


class PeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs['start_date'] > attrs['end_date']:
            raise serializers.ValidationError(
                {
                    'detail': 'A data de início não pode ser maior que a data de fim'
                }
            )

        if self.instance:
            if Period.objects.filter(
                year=attrs['year'],
                semester=attrs['semester']
            ).exclude(
                id=self.instance.id
            ).exists():
                raise serializers.ValidationError(
                    {
                        'detail': 'Esse semestre já foi cadastrado para esse ano'
                    }
                )
        else:
            if Period.objects.filter(
                year=attrs['year'],
                semester=attrs['semester']
            ).exists():
                raise serializers.ValidationError(
                    {
                        'detail': 'Esse semestre já foi cadastrado para esse ano'
                    }
                )

        return attrs
