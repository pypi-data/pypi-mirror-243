from movva_tools.models.flow_models import RapidProFlows
from movva_tools.serializers.base_serializer import (
    BaseSerializer, serializer_fields, date_field_format
)


class FlowSerializer(BaseSerializer):

    class Meta:
        model = RapidProFlows

    uuid = serializer_fields.UUID(dump_only=True)
    name = serializer_fields.String(dump_only=True)
    is_active = serializer_fields.Boolean(dump_only=True)
    created_on = date_field_format
