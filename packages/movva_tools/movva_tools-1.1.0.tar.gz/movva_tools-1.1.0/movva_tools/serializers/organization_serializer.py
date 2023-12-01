from movva_tools.models.organization_models import RapidProOrganization
from movva_tools.serializers.base_serializer import (
    BaseSerializer, serializer_fields
)


class OrganizationSerializer(BaseSerializer):
    class Meta:
        model = RapidProOrganization

    uuid = serializer_fields.UUID(dump_only=True)
    name = serializer_fields.String(dump_only=True)
    slug = serializer_fields.String(dump_only=True)
