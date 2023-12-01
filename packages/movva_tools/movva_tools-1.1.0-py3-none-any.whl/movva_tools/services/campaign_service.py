from datetime import timedelta, datetime
from movva_tools.constants import EventUnitTime, EventMode, EventType

from movva_tools.models.campaign_models import (
    RapidProCampaignEvents, RapidProCampaigns
)
from movva_tools.models.flow_models import RapidProFlows
from movva_tools.models.user_models import RapidProUser
from movva_tools.models.organization_models import RapidProOrganization
from movva_tools.models.contacts_models import (
    RapidProContactFields, RapidProContactGroups
)

from movva_tools.services.contacts_service import ContactService
from movva_tools.services.base_service import BaseService


class CampaingService(BaseService):

    def __init__(self, db_connection=None) -> None:

        super().__init__(db_connection)

        # services
        self.contact_service = ContactService(
            db_connection=self.db_connection
        )

        # model table entities
        self.Campaign = RapidProCampaigns
        self.CampaignEvent = RapidProCampaignEvents

    def create_campaign(
        self,
        org: RapidProOrganization,
        user: RapidProUser,
        name: str,
        group: RapidProContactGroups
    ):

        campaign = self.Campaign(
            org_id=org.id,
            created_by_id=user.id,
            name=name,
            group_id=group.id
        )

        self.add(campaign)
        self.flush()

        return campaign

    def define_delivery_hour_campaign_event(
        self, offset, reference_date, delivery_time
    ):
        return reference_date + timedelta(
            days=offset, hours=delivery_time.hour, minutes=delivery_time.minute
        )

    def fetch_reference_date_field(self, label, organization):

        return self.contact_service.get_contacfield_by_label(
            org=organization,
            label=label
        )

    def set_config_campaign_event(
        self,
        offset, offset_hour,
        send_time, reference_date,
        reference_hour,
    ):
        delivery_time = None
        unit = EventUnitTime.DAYS

        """
            Hora de envio com minutos - deslocamento em minutos
            Não é informada hora de envio - deslocamento em dias
            Informada hora de envio sem minutos - deslocamento em dia e hora
        """
        if send_time and send_time >= reference_hour:

            if send_time.minute != 0:
                unit = EventUnitTime.MINUTES
                reference_date_with_time = reference_date + timedelta(hours=reference_hour.hour, minutes=reference_hour.minute)
                offset = (offset * 24 * 60) + (offset_hour.hour * 60) + send_time.minute
                send_time = -1
                delivery_time = reference_date_with_time + timedelta(minutes=offset)
            else:
                send_time = send_time.hour
                delivery_time = reference_date + timedelta(days=offset)

        elif send_time and send_time < reference_hour:
            if send_time.minute != 0:
                unit = EventUnitTime.MINUTES
                reference_date_with_time = reference_date + timedelta(hours=reference_hour.hour, minutes=reference_hour.minute)
                offset = (offset * 24 * 60) - (offset_hour.hour * 60) - send_time.minute
                send_time = -1
                delivery_time = reference_date_with_time + timedelta(minutes=offset)
            else:
                send_time = send_time.hour
                delivery_time = reference_date + timedelta(days=offset) - timedelta(hours=offset_hour.hour)

        elif not send_time:
            send_time = -1
            delivery_time = reference_date + timedelta(days=offset)

        elif not delivery_time:
            raise Exception('Não foi possível configurar horário de envio.')

        return {
            'delivery_hour': send_time,
            'unit': unit,
            'event_type': EventType.FLOW,
            'offset': offset,
            'delivery_time': delivery_time
        }

    def create_campaign_event(
        self,
        campaign: RapidProCampaigns,
        flow: RapidProFlows,
        relative_to: RapidProContactFields,
        configuration: dict
    ):

        campaign_event = self.CampaignEvent(
            campaign_id=campaign.id,
            created_by_id=campaign.created_by_id,
            flow_id=flow.id,
            relative_to_id=relative_to.id,
            delivery_hour=configuration['delivery_hour'],
            unit=configuration['unit'],
            event_type=configuration['event_type'],
            offset=configuration['offset']
        )

        self.add(campaign_event)
        self.flush()

        return campaign_event
