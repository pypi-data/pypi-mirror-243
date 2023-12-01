from movva_tools.models.flow_models import RapidProFlowsRevision
from movva_tools.serializers.base_serializer import (
    BaseSerializer, serializer_fields, date_field_format
)


class FlowRevisionSerializer(BaseSerializer):

    class Meta:
        model = RapidProFlowsRevision

    revision = serializer_fields.Integer(dump_only=True)
    created_on = date_field_format
    is_active = serializer_fields.Boolean(dump_only=True)
