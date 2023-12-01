from movva_tools.services.base_service import BaseService
from movva_tools.models.contacts_models import (
    RapidProContactFields,
    RapidProContactGroups, RapidProContactGroupsContacts
)
from movva_tools.exceptions import ObjectDoesNotExistException


class ContactService(BaseService):

    def __init__(self, db_connection=None) -> None:

        super().__init__(db_connection)

        # model table entities
        self.ContactFields = RapidProContactFields
        self.ContactGroups = RapidProContactGroups
        self.ContactGroupsContacts = RapidProContactGroupsContacts

    def get_contact_by_id(self, id):
        pass

    def get_contact_group_by_id(self, id):
        contact_group = self.db_connection.session.query(
            self.ContactGroups
        ).filter_by(
            id=id
        ).first()

        if contact_group:
            return contact_group
        else:
            raise ObjectDoesNotExistException(
                dababase_object=self.ContactGroups
            )

    def get_contact_group_by_name(self, name, org_id):
        contact_group = self.db_connection.session.query(
            self.ContactGroups
        ).filter_by(
            name=name,
            org_id=org_id
        ).first()

        if contact_group:
            return contact_group
        else:
            raise ObjectDoesNotExistException(
                dababase_object=self.ContactGroups
            )

    def get_contacts_from_groups_by_group_id(self, id):
        pass

    def get_contact_groups_contact_by_contact_id(self, contact_id):
        pass

    def get_contacfield_by_label(self, org, label):
        contact_field = self.db_connection.session.query(
            self.ContactFields
        ).filter_by(
            label=label,
            org_id=org.id
        ).first()

        if contact_field:
            return contact_field
        else:
            raise ObjectDoesNotExistException(
                dababase_object=self.ContactFields
            )
