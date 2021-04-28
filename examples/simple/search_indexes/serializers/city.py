from rest_framework import serializers

from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents import CityDocument

__all__ = ('CityDocumentSerializer',)


class CityDocumentSerializer(DocumentSerializer):
    """Serializer for city document."""

    es_id = serializers.SerializerMethodField()

    class Meta:
        """Meta options."""

        document = CityDocument
        fields = (
            'id',
            'name',
            'info',
            'country',
            'location',
            'capital',
            'boolean_list',
            'datetime_list',
            'float_list',
            'integer_list',
            'es_id',
        )

    def get_es_id(self, obj):
        if hasattr(obj.meta, 'id'):
            return obj.meta.id
        return None
