from movva_tools.databases import Base

from sqlalchemy import (
    UUID, Boolean, Column, DateTime,
    Integer
)


class RapidProApiToken(Base):
    __tablename__ = 'api_apitoken'

    is_active = Column(Boolean, default=True)
    key = Column(UUID(as_uuid=True), primary_key=True)
    created = Column(DateTime)
    org_id = Column(Integer)
    role_id = Column(Integer)
    user_id = Column(Integer)

    def __repr__(self):
        return f'Api Token: {self.key} <org:{self.org.id}>'
