from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from ..documents import LocationDocument


class LocationDocumentSerializer(DocumentSerializer):
    """Serializer for Location document."""

    class Meta:
        """Meta options."""

        # Specify the correspondent document class
        document = LocationDocument

        # List the serializer fields. Note, that the order of the fields
        # is preserved in the ViewSet.
        fields = (
            "full",
            "partial",
            "geocode",
            "slug",
            "number",
            "address",
            "town",
            "authority",
            "postcode",
            "category",
            "occupied",
            "size",
            "staff",
            "rent",
            "revenue",
            "coordinates",
        )
