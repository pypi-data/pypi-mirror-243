from movva_tools.models.contacts_models import RapidProContactGroups
from movva_tools.serializers.base_serializer import (
    BaseSerializer, serializer_fields
)


class ContactGroupSerializer(BaseSerializer):

    class Meta:
        model = RapidProContactGroups

    uuid = serializer_fields.UUID(dump_only=True)
    name = serializer_fields.String(dump_only=True)
    is_active = serializer_fields.Boolean(dump_only=True)
