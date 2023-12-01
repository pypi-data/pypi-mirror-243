from movva_tools.models.organization_models import RapidProOrganization
from movva_tools.exceptions import ObjectDoesNotExistException
from movva_tools.services.base_service import BaseService


class OrganizationService(BaseService):

    def __init__(self, db_connection=None) -> None:
        super().__init__(db_connection)

        self.org = RapidProOrganization

    def get_org_by_name(self, org_name):

        org = self.db_connection.session.query(self.org).filter_by(
            name=org_name
        ).first()

        if org:
            return org
        else:
            raise ObjectDoesNotExistException(dababase_object=self.org)

    def get_org_by_id(self, org_id):

        org = self.db_connection.session.query(self.org).filter_by(
            id=org_id
        ).first()

        if org:
            return org
        else:
            raise ObjectDoesNotExistException(dababase_object=self.org)

    def get_token_org(self, db_connection=None):
        pass
