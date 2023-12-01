import os
from movva_tools.models.api_token_model import RapidProApiToken

from movva_tools.services.base_service import BaseService
from temba_client.v2 import TembaClient

from movva_tools.exceptions import (
    ObjectDoesNotExistException
)


class APITokenService(BaseService):

    def __init__(self, db_connection=None) -> None:

        super().__init__(db_connection)

        # model table entities
        self.APIToken = RapidProApiToken

    def get_token_by_org_id(self, org_id):

        api_token = self.db_connection.session.query(
            self.APIToken
        ).filter_by(
            is_active=True,
            org_id=org_id
        ).first()

        if api_token:
            return api_token.key
        else:
            raise ObjectDoesNotExistException(
                dababase_object=self.APIToken
            )

    def rapidpro_api_client(self, token):
        try:
            return TembaClient(
                host=os.environ.get('RAPIDPRO_URL'),
                token=token
            )
        except Exception:
            raise Exception(
                'Não foi possível estabelecer conexão com o RapidPro.'
            )
