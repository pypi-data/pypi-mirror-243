from datetime import timedelta
from movva_tools.models.campaign_models import RapidProCampaignEvents
from movva_tools.serializers.base_serializer import (
    BaseSerializer, serializer_fields, date_field_format
)


class CampaingEventSerializer(BaseSerializer):
    class Meta:
        model = RapidProCampaignEvents

    def __init__(self, *args, config_time, **kwargs):
        super().__init__(*args, **kwargs)
        self.config_time = config_time

    uuid = serializer_fields.UUID(dump_only=True)
    delivery_hour = serializer_fields.Integer(dump_only=True)
    offset = serializer_fields.Integer(dump_only=True)
    unit = serializer_fields.String(dump_only=True)
    created_on = date_field_format
    config_time = serializer_fields.Method("format_reference_date", dump_only=True)

    def format_reference_date(self, obj):
        if self.config_time['delivery_hour'] == -1:
            return self.config_time['delivery_time'].strftime("%d/%m/%Y %H:%M")
        else:
            return (
                self.config_time['delivery_time'] + timedelta(
                    hours=self.config_time['delivery_hour']
                )
            ).strftime("%d/%m/%Y %H:%M")
        # Aqui, você formata a data conforme necessário
        # Estou assumindo que `self.reference_date` já está em um formato de data/hora válido
