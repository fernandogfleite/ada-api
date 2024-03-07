from rest_framework.serializers import (
    RelatedField,
    ChoiceField
)

from collections import OrderedDict


class ModifiedRelatedField(RelatedField):
    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        return OrderedDict([
            (
                item.pk,
                self.display_value(item)
            )
            for item in queryset
        ])


class CustomChoiceField(ChoiceField):
    def to_representation(self, obj):
        if (obj == '' and self.allow_blank) or (obj is None):
            return None

        return {
            'value': obj,
            'label': self._choices[obj]
        }

    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return None

        try:
            return self.choice_strings_to_values[str(data)]
        except KeyError:
            self.fail('invalid_choice', input=data)
