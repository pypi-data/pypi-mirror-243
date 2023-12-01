from datetime import datetime
import uuid

from movva_tools.databases import Base
from movva_tools.constants import EventMode
from sqlalchemy import (
    UUID, Boolean, Column, DateTime,
    Integer, String,
)


class RapidProCampaigns(Base):
    __tablename__ = 'campaigns_campaign'

    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    created_on = Column(DateTime, default=datetime.utcnow)
    modified_on = Column(DateTime, default=datetime.utcnow)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    name = Column(String)
    is_archived = Column(Boolean)
    created_by_id = Column(Integer)
    group_id = Column(Integer)
    modified_by_id = Column(Integer)
    org_id = Column(Integer)

    def __init__(self, created_by_id, org_id, group_id, name):

        super().__init__()
        self.created_by_id = created_by_id
        self.modified_by_id = created_by_id
        self.org_id = org_id
        self.group_id = group_id
        self.name = name
        self.is_archived = False
        self.is_active = True

    def __repr__(self):
        return f'<{self.uuid}:{self.name}>'


class RapidProCampaignEvents(Base):
    __tablename__ = 'campaigns_campaignevent'

    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    created_on = Column(DateTime, default=datetime.utcnow)
    modified_on = Column(DateTime, default=datetime.utcnow)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    offset = Column(Integer)
    unit = Column(String)
    start_mode = Column(String)
    event_type = Column(String)
    message = Column(String)
    delivery_hour = Column(Integer)
    campaign_id = Column(Integer)
    created_by_id = Column(Integer)
    flow_id = Column(Integer)
    modified_by_id = Column(Integer)
    relative_to_id = Column(Integer)

    def __init__(
        self, created_by_id,
        offset, unit, event_type,
        campaign_id, flow_id,
        relative_to_id,
        message='', delivery_hour=-1,
    ):
        self.created_by_id = created_by_id
        self.modified_by_id = created_by_id
        self.is_active = True
        self.start_mode = EventMode.INTERRUPT

        self.offset = offset
        self.unit = unit
        self.event_type = event_type

        self.campaign_id = campaign_id
        self.flow_id = flow_id
        self.relative_to_id = relative_to_id
        self.message = message
        self.delivery_hour = delivery_hour

    def __repr__(self):
        return f'<{self.uuid}>'
