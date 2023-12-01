from typing import List

from movva_tools.services.base_service import BaseService
from movva_tools.exceptions import (
    ObjectDoesNotExistException,
)

from movva_tools.models.channel_models import RapidProChannel
from movva_tools.models.organization_models import RapidProOrganization


class ChannelService(BaseService):

    def __init__(self, db_connection=None) -> None:
        super().__init__(db_connection)

        # model table entities
        self.Channel = RapidProChannel

    def get_channel_by_name(self, name: str, org: RapidProOrganization):
        channel = self.db_connection.session.query(
            self.Channel
        ).filter_by(
            name=name,
            org_id=org.id
        ).first()

        if channel:
            return channel
        else:
            raise ObjectDoesNotExistException(dababase_object=self.Channel)

    def get_channel_by_id(self, id: int):
        channel = self.db_connection.session.query(
            self.Channel
        ).filter_by(
            id=id,
        ).first()

        if channel:
            return channel
        else:
            raise ObjectDoesNotExistException(dababase_object=self.Channel)

    def get_channel_by_address(self, address: str, org: RapidProOrganization):
        channel = self.db_connection.session.query(
            self.Channel
        ).filter_by(
            address=address,
            org_id=org.id
        ).first()

        if channel:
            return channel
        else:
            raise ObjectDoesNotExistException(dababase_object=self.Channel)
