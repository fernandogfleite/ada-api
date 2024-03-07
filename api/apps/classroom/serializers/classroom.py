from api.apps.authentication.serializers.fields.user import (
    TeacherField,
    StudentField
)
from api.apps.classroom.models.classroom import (
    Period,
    Room,
    Subject,
    SubjectPeriod,
    SubjectPeriodWeekday,
    SubjectPeriodStudent
)
from api.apps.classroom.serializers.fields.classroom import (
    PeriodField,
    SubjectField,
    SubjectPeriodField
)
from api.apps.utils.fields import CustomChoiceField

from rest_framework import serializers

from django.db import transaction


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


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Period
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        if self.instance:
            if Room.objects.filter(
                name=value
            ).exclude(
                id=self.instance.id
            ).exists():
                raise serializers.ValidationError(
                    {
                        'detail': 'Essa sala já foi cadastrada'
                    }
                )
        else:
            if Room.objects.filter(name=value).exists():
                raise serializers.ValidationError(
                    {
                        'detail': 'Essa sala já foi cadastrada'
                    }
                )

        return value


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if self.instance:
            if Subject.objects.filter(
                name=attrs.get('name', self.instance.name),
                code=attrs.get('code', self.instance.code)
            ).exclude(
                id=self.instance.id
            ).exists():
                raise serializers.ValidationError(
                    {
                        'detail': 'Essa disciplina já foi cadastrada com esse código'
                    }
                )
        else:
            if Subject.objects.filter(
                name=attrs['name'],
                code=attrs['code']
            ).exists():
                raise serializers.ValidationError(
                    {
                        'detail': 'Essa disciplina já foi cadastrada com esse código'
                    }
                )

        return attrs


class DayOfWeekSerializer(serializers.Serializer):
    weekday = CustomChoiceField(choices=SubjectPeriodWeekday.WEEKDAYS)
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if attrs['start_time'] > attrs['end_time']:
            raise serializers.ValidationError(
                {
                    'detail': 'A hora de início não pode ser maior que a hora de fim'
                }
            )

        return attrs


class SubjectPeriodSerializer(serializers.ModelSerializer):
    subject = SubjectField()
    teacher = TeacherField()
    period = PeriodField()
    days_of_week = DayOfWeekSerializer(many=True)

    class Meta:
        model = SubjectPeriod
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        extra_kwargs = {
            'days_of_week': {'write_only': True}
        }

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if self.instance:
            if SubjectPeriod.objects.filter(
                period=attrs.get('period', self.instance.period),
                subject=attrs.get('subject', self.instance.subject),
                teacher=attrs.get('teacher', self.instance.teacher)
            ).exclude(
                id=self.instance.id
            ).exists():
                raise serializers.ValidationError(
                    {
                        'detail': 'Essa disciplina já foi cadastrada para esse semestre com esse professor'
                    }
                )
        else:
            if SubjectPeriod.objects.filter(
                period=attrs['period'],
                subject=attrs['subject'],
                teacher=attrs['teacher']
            ).exists():
                raise serializers.ValidationError(
                    {
                        'detail': 'Essa disciplina já foi cadastrada para esse semestre com esse professor'
                    }
                )

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        days_of_week = validated_data.pop('days_of_week')
        subject_period = SubjectPeriod.objects.create(**validated_data)

        for day_of_week in days_of_week:
            SubjectPeriod.objects.create_subject_period_weekday(
                subject_period,
                day_of_week['weekday'],
                day_of_week['start_time'],
                day_of_week['end_time']
            )

        return subject_period

    def update(self, instance, validated_data):
        raise NotImplementedError('Não é possível atualizar uma disciplina')


class SubjectPeriodStudentSerializer(serializers.ModelSerializer):
    student = StudentField()
    subject_period = SubjectPeriodField()

    class Meta:
        model = SubjectPeriodStudent
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, attrs):
        attrs = super().validate(attrs)

        if self.instance:
            if SubjectPeriodStudent.objects.filter(
                student=attrs.get(
                    'student',
                    self.instance.student
                ),
                subject_period=attrs.get(
                    'subject_period',
                    self.instance.subject_period
                )
            ).exclude(
                id=self.instance.id
            ).exists():
                raise serializers.ValidationError(
                    {
                        'detail': 'Esse aluno já está cadastrado nessa disciplina'
                    }
                )
        else:
            if SubjectPeriodStudent.objects.filter(
                student=attrs['student'],
                subject_period=attrs['subject_period']
            ).exists():
                raise serializers.ValidationError(
                    {
                        'detail': 'Esse aluno já está cadastrado nessa disciplina'
                    }
                )

        return attrs
