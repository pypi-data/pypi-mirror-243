from movva_tools.exceptions import ObjectDoesNotExistException
from movva_tools.models.messages_models import RapidProMessages
from movva_tools.services.base_service import BaseService


class MessageService(BaseService):
    def __init__(self, db_connection=None) -> None:

        super().__init__(db_connection=db_connection)

        # model table entities
        self.Message = RapidProMessages

    def fetch_message_by_id(self, message_id):
        message = self.db_connection.session.query(self.Message).filter_by(
            id=message_id
        ).first()

        if message:
            return message
        else:
            raise ObjectDoesNotExistException(dababase_object=self.Message)

    def fetch_messages_by_channel_and_org(self, channel_id, org_id, direction, status=None):
        if status:
            messages = self.db_connection.session.query(self.Message).filter_by(
                status=status,
                direction=direction,
                channel_id=channel_id,
                org_id=org_id
            ).all()
        else:
            messages = self.db_connection.session.query(self.Message).filter_by(
                channel_id=channel_id,
                direction=direction,
                org_id=org_id
            ).all()

        return messages if messages else []

