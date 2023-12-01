from movva_tools.models.campaign_models import RapidProCampaigns
from movva_tools.serializers.base_serializer import (
    BaseSerializer, serializer_fields, date_field_format
)


class CampaignSerializer(BaseSerializer):

    class Meta:
        model = RapidProCampaigns

    uuid = serializer_fields.UUID(dump_only=True)
    name = serializer_fields.String(dump_only=True)
    created_on = date_field_format
    is_active = serializer_fields.Boolean(dump_only=True)
