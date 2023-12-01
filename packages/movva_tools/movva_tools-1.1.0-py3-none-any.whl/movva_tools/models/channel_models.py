import uuid
from datetime import datetime

from sqlalchemy import (
    JSON, UUID, Boolean, Column, DateTime,
    Integer, String, ForeignKey
)

from movva_tools.databases import Base
from sqlalchemy.orm import relationship


class RapidProChannel(Base):
    __tablename__ = 'channels_channel'

    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean, default=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    modified_on = Column(DateTime, default=datetime.utcnow)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4)
    channel_type = Column(String)
    name = Column(String)
    address = Column(String)
    country = Column(String)
    claim_code = Column(String)
    secret = Column(String)
    last_seen = Column(DateTime, default=datetime.utcnow)
    device = Column(String, default="")
    os = Column(String, default="")
    alert_email = Column(String, default="")
    config = Column(JSON)
    schemes = Column(String)
    role = Column(String)
    bod = Column(String, default="")
    tps = Column(Integer)
    created_by_id = Column(Integer)
    modified_by_id = Column(Integer)
    org_id = Column(Integer)
    parent_id = Column(Integer, default="")

    def __repr__(self):
        return f'uuid: {self.uuid} <{self.name}|{self.address}>'


class RapidProChannelLog(Base):
    __tablename__ = 'channels_channellog'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    url = Column(String)
    method = Column(String)
    request = Column(String)
    response = Column(String)
    response_status = Column(Integer)
    created_on = Column(DateTime, default=datetime.utcnow)
    request_time = Column(Integer)
    channel_id = Column(Integer, ForeignKey('channels_channel.id'))
    connection_id = Column(Integer)
    msg_id = Column(Integer)

    # Defina o relacionamento com RapidProChannel
    channel = relationship('RapidProChannel')

    def __repr__(self):
        return f'id: {self.id} <channel: {self.channel.name}>'
