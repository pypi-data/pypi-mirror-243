import uuid
from movva_tools.databases import Base
from datetime import datetime

from sqlalchemy import (
    Boolean, Column, DateTime,
    Integer, String, UUID
)


class RapidProMessages(Base):
    __tablename__ = 'msgs_msg'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    text = Column(String)
    high_priority = Column(Boolean, default=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    modified_on = Column(DateTime, default=datetime.utcnow)
    sent_on = Column(DateTime, default=datetime.utcnow)
    queued_on = Column(DateTime, default=datetime.utcnow)
    direction = Column(String)
    status = Column(String)
    visibility = Column(String)
    msg_type = Column(String)
    msg_count = Column(Integer)
    error_count = Column(Integer)
    next_attempt = Column(DateTime, default=datetime.utcnow)
    external_id = Column(UUID(as_uuid=True))
    attachments = Column(String)
    msg_metadata = Column('metadata', String)
    broadcast_id = Column(Integer)
    channel_id = Column(Integer)
    contact_id = Column(Integer)
    contact_urn_id = Column(Integer)
    org_id = Column(Integer)
    topup_id = Column(Integer)
    failed_reason = Column(String)
    flow_id = Column(Integer)

    def __repr__(self):
        return f'id: {self.id} <{self.uuid}>'

