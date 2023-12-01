import json
import pandas as pd
from sqlalchemy import desc
from typing import Tuple

from movva_tools.models.campaign_models import (
    RapidProCampaignEvents, RapidProCampaigns
)
from movva_tools.models.channel_models import RapidProChannel
from movva_tools.notifications import SlackFlowSchedulledNotification
from movva_tools.models.user_models import RapidProUser
from movva_tools.models.organization_models import RapidProOrganization
from movva_tools.models.contacts_models import RapidProContactGroups
from movva_tools.models.flow_models import (
    RapidProFlowChannelDependencies, RapidProFlowFieldDependencies,
    RapidProFlowFlowLabelDependencies, RapidProFlowGroupDependencies,
    RapidProFlowLabel, RapidProFlows,
    RapidProFlowsFlowLabels, RapidProFlowsRevision
)

from movva_tools.serializers import CampaingEventSerializer
from movva_tools.serializers import ContactGroupSerializer
from movva_tools.serializers import FlowRevisionSerializer
from movva_tools.serializers import OrganizationSerializer
from movva_tools.serializers import CampaignSerializer
from movva_tools.serializers import FlowSerializer

from movva_tools.services.base_service import BaseService
from movva_tools.services.api_token_service import APITokenService
from movva_tools.services.campaign_service import CampaingService
from movva_tools.services.contacts_service import ContactService
from movva_tools.services.organization_service import OrganizationService
from movva_tools.services.user_service import UserService

from movva_tools.constants import MAX_NAME_LEN
from movva_tools.constants import Flow, FlowType, GoFlowTypes
from movva_tools.decorators import ensure_transaction
from movva_tools.exceptions import ObjectDoesNotExistException

from movva_tools.utils import DATE_FORMAT, TIME_FORMAT, json_representation, serialize
from movva_tools.utils import break_list_into_groups, datetime_string_parser
from movva_tools.validators import FlowNameValidator
from movva_tools.integrations.google_integration import FlowGoogleSheets


class FlowService(BaseService):

    def __init__(self, db_connection=None) -> None:

        super().__init__(db_connection=db_connection)

        # model table entities
        self.flow = RapidProFlows
        self.flow_revision = RapidProFlowsRevision
        self.org = RapidProOrganization

        # services
        self.user_service = UserService(
            db_connection=self.db_connection
        )
        self.organization_service = OrganizationService(
            db_connection=self.db_connection
        )

    def __set_default_flow_metadata(self):

        return {
            "results": [],
            "dependencies": [],
            "waiting_exit_uuids": [],
            "parent_refs": []
        }

    def __set_initial_flow_revision_definition(self, flow: RapidProFlows):
        return {
            Flow.DEFINITION_NAME: flow.name,
            Flow.DEFINITION_UUID: str(flow.uuid),
            Flow.DEFINITION_SPEC_VERSION: Flow.CURRENT_SPEC_VERSION,
            Flow.DEFINITION_LANGUAGE: Flow.BASE_LANGUAGE,
            Flow.DEFINITION_TYPE: GoFlowTypes.TYPE_MESSAGE,
            Flow.DEFINITION_NODES: [],
            Flow.DEFINITION_UI: {},
            Flow.DEFINITION_REVISION: 1,
            Flow.DEFINITION_EXPIRE_AFTER_MINUTES: Flow.EXPIRES_AFTER_MINUTES
        }

    def __set_flow_revision_definition(
        self, flow: RapidProFlows, setted_definition: json
    ):

        setted_definition[Flow.DEFINITION_NAME] = flow.name
        setted_definition[Flow.DEFINITION_REVISION] = 1
        setted_definition[Flow.DEFINITION_UUID] = str(flow.uuid)

        return setted_definition

    def is_valid_name(cls, name: str) -> bool:
        try:
            FlowNameValidator()(value=name)
            return True
        except Exception:
            return False

    def get_flow_by_name(self, flow_name: str):

        flow = self.db_connection.session.query(self.flow).filter_by(
            name=flow_name
        ).first()

        if flow:
            return flow
        else:
            raise ObjectDoesNotExistException(dababase_object=self.flow)

    def get_flow_by_id(self, flow_id: int):

        flow = self.db_connection.session.query(self.flow).filter_by(
            id=flow_id
        ).first()

        if flow:
            return flow
        else:
            raise ObjectDoesNotExistException(dababase_object=self.flow)

    def create_flow_revision(
        self, flow: RapidProFlows, user: RapidProUser,
        setted_definition: json = None
    ):
        if setted_definition:
            definition = self.__set_flow_revision_definition(
                flow, setted_definition=setted_definition
            )
        else:
            definition = self.__set_initial_flow_revision_definition(flow=flow)

        new_flow_revision = self.flow_revision(
            created_by_id=user.id,
            flow_id=flow.id,
            definition=definition
        )

        self.add(new_flow_revision)
        self.flush()
        return new_flow_revision

    def _create_flow(
        self,
        user: RapidProUser,
        org: RapidProOrganization,
        flow_name: str,
        flow_type=FlowType.TYPE_MESSAGE,
        expires_after_minutes=Flow.EXPIRES_AFTER_MINUTES
    ):

        new_flow = self.flow(
            org_id=org.id,
            created_by_id=user.id,
            name=flow_name,
            flow_type=flow_type,
            expires_after_minutes=expires_after_minutes,
            flow_metadata=self.__set_default_flow_metadata()
        )

        self.add(new_flow)
        self.flush()
        return new_flow

    def create_flow(
        self,
        org: RapidProOrganization,
        user: RapidProUser,
        flow_name: str,
        external_context: bool = True
    ):

        self.is_valid_name(flow_name)

        return self._create_flow(
            org=org,
            user=user,
            flow_name=flow_name
        )


class FlowLabelService(BaseService):
    def __init__(self, db_connection=None) -> None:

        super().__init__(db_connection)

        # model table entities
        self.Flow = RapidProFlows
        self.Organization = RapidProOrganization
        self.FlowLabel = RapidProFlowLabel
        self.FlowsFlowLabels = RapidProFlowsFlowLabels

        # services
        self.user_service = UserService(
            db_connection=self.db_connection
        )
        self.organization_service = OrganizationService(
            db_connection=self.db_connection
        )
        self.flow_service = FlowService(
            db_connection=self.db_connection
        )

    def get_label_by_id(self, id: int):
        label = self.db_connection.session.query(self.FlowLabel).filter_by(
            id=id
        ).first()

        if label:
            return label
        else:
            raise ObjectDoesNotExistException(dababase_object=self.FlowLabel)

    def get_label_by_name(self, name: str, org_id: int):
        label = self.db_connection.session.query(self.FlowLabel).filter_by(
            name=name,
            org_id=org_id
        ).first()

        if label:
            return label
        else:
            raise ObjectDoesNotExistException(dababase_object=self.FlowLabel)

    def _create_flow_label(
        self, name: str, org: RapidProOrganization, flow: RapidProFlows
    ):

        flow_label = self.FlowLabel(
            org_id=org.id,
            name=name
        )

        self.add(flow_label)
        self.flush()

        flows_flowlabels = self.FlowsFlowLabels(
            flow_id=flow.id,
            flowlabel_id=flow_label.id
        )

        self.add(flows_flowlabels)
        self.flush()

        return flow_label

    def create(self, name: str, org: RapidProOrganization, flow: RapidProFlows):
        return self._create_flow_label(name, org, flow)


class FlowDependenciesService(BaseService):

    def __init__(self, db_connection=None) -> None:

        super().__init__(db_connection)

        # model table entities
        self.FlowChannelDependencies = RapidProFlowChannelDependencies

        self.FlowGroupDependencies = RapidProFlowGroupDependencies

        self.FlowFieldDependencies = RapidProFlowFieldDependencies

        self.FlowFlowLabelDependencies = RapidProFlowFlowLabelDependencies

    def _set_flow_dependencies(
        self,
        flow: RapidProFlows, channel: RapidProChannel,
        group: RapidProContactGroups, flowlabel: RapidProFlowLabel
    ):
        flow_channel_dependencies = self.FlowChannelDependencies(
            flow_id=flow.id,
            channel_id=channel.id
        )
        self.add(flow_channel_dependencies)

        flow_group_dependencies = self.FlowGroupDependencies(
            flow_id=flow.id,
            group_id=group.id
        )
        self.add(flow_group_dependencies)

        flow_flowlabel_dependencies = self.FlowFlowLabelDependencies(
            flow_id=flow.id,
            flowlabel_id=flowlabel.id
        )
        self.add(flow_flowlabel_dependencies)

        self.flush()

    def create(
        self, flow: RapidProFlows, channel: RapidProChannel,
        group: RapidProContactGroups, flowlabel: RapidProFlowLabel
    ):
        return self._set_flow_dependencies(flow, channel, group, flowlabel)


class CopyFlowAndScheduleService(BaseService):

    def __init__(self, db_connection=None) -> None:

        super().__init__(db_connection)

        # spreadsheet reader to copy flow
        self.spreadsheet_reader = FlowGoogleSheets

        # model table entities
        self.flow_revision = RapidProFlowsRevision

        # services
        self.flow_service = FlowService(
            db_connection=self.db_connection
        )
        self.flowlabel_service = FlowLabelService(
            db_connection=self.db_connection
        )
        self.organization_service = OrganizationService(
            db_connection=self.db_connection
        )
        self.user_service = UserService(
            db_connection=self.db_connection
        )
        self.api_token_service = APITokenService(
            db_connection=self.db_connection
        )
        self.contact_service = ContactService(
            db_connection=self.db_connection
        )
        self.campaign_service = CampaingService(
            db_connection=self.db_connection
        )

        # serializers
        self.FlowSerializer = FlowSerializer
        self.CampaignSerializer = CampaignSerializer
        self.OrganizationSerializer = OrganizationSerializer
        self.FlowRevisionSerializer = FlowRevisionSerializer
        self.CampaignEventSerializer = CampaingEventSerializer
        self.ContactGroupSerializer = ContactGroupSerializer

    def get_unique_name(self, org: RapidProOrganization, base_name: str):

        name = f'{base_name[:MAX_NAME_LEN]}' if len(base_name) > MAX_NAME_LEN else base_name
        qs = self.db_connection.session.query(self.flow).filter_by(
            org_id=org.id,
            is_active=True,
            name=name
        ).all()

        if qs:
            name = 'Copy_of ' + name

        return name

    def get_last_flow_revision(self, flow: RapidProFlows):

        flow_revision = self.db_connection.session.query(
            self.flow_revision
        ).order_by(
            desc(self.flow_revision.created_on)
        ).filter_by(
            flow_id=flow.id
        ).first()

        if flow_revision:
            return flow_revision
        else:
            raise ObjectDoesNotExistException(
                dababase_object=self.flow_revision
            )

    def _transfer_flow_revision_messages(
        self,
        json_string: str,
        template_data: dict,
        new_flow_data: dict,
        reader: FlowGoogleSheets
    ):
        # identificar padrão Mensagem#N, onde N é o numero da msg

        messages = zip(
            [template_data[key] for key in reader.message_columns],
            [new_flow_data[key] for key in reader.message_columns]
        )

        for actual, new in messages:
            actual = actual.replace('\n', '\\n')
            new = new.replace('\n', '\\n')
            actual = f'"{actual}"'
            new = f'"{new}"'
            json_string = json_string.replace(actual, new)

        return json_string

    def transfer_flow_revision_data(
        self, flow_json: dict,
        template_data: dict,
        new_flow_data: dict,
        spreadsheet_reader: FlowGoogleSheets
    ):

        # aqui serão chamados os métodos para cada etapa do definition
        flow_data = json.dumps(flow_json, ensure_ascii=False)

        flow_data = self._transfer_flow_revision_messages(
            json_string=flow_data,
            template_data=template_data,
            new_flow_data=new_flow_data,
            reader=spreadsheet_reader
        )
        return json.loads(flow_data)

    def set_rapidpro_client_to_organization(self, org_destination):
        api_token = self.api_token_service.get_token_by_org_id(
            org_id=org_destination.id
        )

        return self.api_token_service.rapidpro_api_client(
            token=api_token
        )

    def import_definition(
        self,
        user: RapidProUser,
        definition: json,
        flow_destination: RapidProFlows,
        spreadsheet_reader: FlowGoogleSheets,
        template_data: dict,
        new_flow_data: dict
    ):
        """
            Allows setting the definition for a flow from another definition.
            All UUID's will be remapped.
        """

        flow_revision_copy = definition.copy()

        # aqui deve entrar as modificações do flow revision
        flow_revision_copy = self.transfer_flow_revision_data(
            template_data=template_data,
            new_flow_data=new_flow_data,
            spreadsheet_reader=spreadsheet_reader,
            flow_json=flow_revision_copy
        )

        flow_revision_destination = self.flow_service.create_flow_revision(
            flow=flow_destination,
            user=user,
            setted_definition=flow_revision_copy
        )

        return flow_revision_destination

    def get_revision_definition(self, flow) -> dict:
        revision = self.get_last_flow_revision(
            flow=flow
        )

        definition = revision.definition

        return json.loads(definition)

    def _check_organization_data(
        self,
        org_flow: RapidProOrganization,
        origin_org: str
    ) -> bool:
        org_flow_name = org_flow.name
        if org_flow_name == origin_org:
            return True

        return False

    def clone_flow(
        self,
        raw_flow: dict, template: dict,
        user: RapidProUser,
        reader: FlowGoogleSheets
    ) -> Tuple[RapidProFlows, RapidProFlowsRevision, RapidProOrganization]:

        origin_organization_name = raw_flow[
            reader.FlowColumns.ORGANIZATION_OF_TEMPLATE
        ]
        destiny_organization_name = raw_flow[
            reader.FlowColumns.ORGANIZATION
        ]
        base_flow_name = raw_flow[reader.FlowColumns.TEMPLATE_FLOW]
        flow_suggested_name = raw_flow[reader.FlowColumns.FLOW]

        org_destination = self.organization_service.get_org_by_name(
            org_name=destiny_organization_name
        )

        base_flow = self.flow_service.get_flow_by_name(
            flow_name=base_flow_name
        )
        org_related_to_flow = self.organization_service.get_org_by_id(
            org_id=base_flow.org_id
        )

        if not self._check_organization_data(
            org_flow=org_related_to_flow,
            origin_org=origin_organization_name
        ):
            raise Exception(
                'A organização de origem não contém o fluxo original informado para cópia.'  # noqa
            )

        copy = self.flow_service.create_flow(
            org=org_destination,
            user=user,
            flow_name=flow_suggested_name
        )

        base_flow_json = self.get_revision_definition(
            flow=base_flow
        )

        revision = self.import_definition(
            user=user,
            definition=base_flow_json,
            flow_destination=copy,
            new_flow_data=raw_flow,
            template_data=template,
            spreadsheet_reader=reader
        )

        return copy, revision, org_destination

    def prepare_flow_copy_spreadsheet(
        self,
        registers: pd.DataFrame,
        reader: FlowGoogleSheets
    ):

        # filter lines that have data not registred.
        registers = registers[
            registers[reader.FlowColumns.UPLOAD] == 'VERDADEIRO'
        ]

        if registers.empty:
            raise Exception('Planilha sem informações.')

        registers = registers.reset_index().to_dict(orient='records')

        return registers

    def create_campaign(
        self,
        reader: FlowGoogleSheets,
        raw_flow: dict,
        flow: RapidProFlows,
        org: RapidProOrganization,
        user: RapidProUser,
        group: RapidProContactGroups
    ) -> Tuple[RapidProCampaigns, RapidProCampaignEvents, dict]:

        spreadsheet_reference_date = None
        spreadsheet_reference_hour = None
        spreadsheet_offset_hour = None
        spreadsheet_offset = None
        spreadsheet_send_time = None
        spreadsheet_label_reference_date = None

        spreadsheet_campaign_name = raw_flow[reader.FlowColumns.CAMPAING_NAME]

        try:
            spreadsheet_label_reference_date = raw_flow[
                reader.FlowColumns.LABEL_REFERENCE_DATE
            ]

            spreadsheet_reference_date = datetime_string_parser(
                date_str=raw_flow[reader.FlowColumns.REFERENCE_DATE],
                pattern=DATE_FORMAT
            )

            spreadsheet_reference_hour = datetime_string_parser(
                date_str=raw_flow[reader.FlowColumns.REFERENCE_HOUR],
                pattern=TIME_FORMAT
            )

            spreadsheet_offset_hour = datetime_string_parser(
                date_str=raw_flow[reader.FlowColumns.HOURS_FROM_REFERENCE_DATE],
                pattern=TIME_FORMAT
            )

            spreadsheet_offset = int(
                raw_flow[reader.FlowColumns.DAYS_FROM_REFERENCE_DATE]
            )
        except (Exception, ValueError, AttributeError):
            pass

        if spreadsheet_reference_date is None:
            raise Exception(
                'A data de referência não foi informada ou não está no formato dd/mm/aaaa.'
            )
        elif spreadsheet_reference_hour is None:
            raise Exception(
                'A hora de referência não foi informada ou não está no formato hh:mm:ss'
            )
        elif spreadsheet_offset_hour is None:
            raise Exception('A diferença de horas deve ser informada.')
        elif spreadsheet_offset is None:
            raise Exception('A diferença de dias deve ser informada.')
        elif spreadsheet_label_reference_date is None:
            raise Exception('A variável de data de referência deve ser informada.')

        spreadsheet_send_time = datetime_string_parser(
            date_str=raw_flow[reader.FlowColumns.SEND_TIME],
            pattern=TIME_FORMAT
        )

        campaign = self.campaign_service.create_campaign(
            name=spreadsheet_campaign_name,
            group=group,
            org=org,
            user=user
        )

        config = self.campaign_service.set_config_campaign_event(
            offset=spreadsheet_offset,
            offset_hour=spreadsheet_offset_hour,
            send_time=spreadsheet_send_time,
            reference_date=spreadsheet_reference_date,
            reference_hour=spreadsheet_reference_hour,
        )

        relative_to = self.contact_service.get_contacfield_by_label(
            org=org,
            label=spreadsheet_label_reference_date
        )

        campaign_event = self.campaign_service.create_campaign_event(  # noqa
            campaign=campaign,
            flow=flow,
            relative_to=relative_to,
            configuration=config
        )

        return campaign, campaign_event, config

    def fetch_group_name_in_spreadsheet(
        self, raw_flow: dict, reader: FlowGoogleSheets,
        organization: RapidProOrganization
    ):
        spreadsheet_group = raw_flow[reader.FlowColumns.CONTACT_GROUP]

        group = self.contact_service.get_contact_group_by_name(
            name=spreadsheet_group,
            org_id=organization.id
        )

        return group

    @ensure_transaction
    def create_sheduled_flow(
        self,
        link: str,
        page: str,
        end_selection: str = None
    ):

        reader = self.spreadsheet_reader(link, page)
        registers = reader.read_sheet_data()

        registers = self.prepare_flow_copy_spreadsheet(registers, reader)
        registers = break_list_into_groups(registers, chunk_size=2)

        with self.db_connection.session.begin():
            user = self.user_service.get_default_user()

            list_serialized_data = []
            spreadsheet_pos = []
            for raw_flow, template in registers:
                spreadsheet_pos.append(
                    {'flow': raw_flow['index'], 'template': template['index']}
                )

                flow, revision, org_destination = self.clone_flow(
                    raw_flow=raw_flow,
                    template=template,
                    user=user,
                    reader=reader
                )

                group = self.fetch_group_name_in_spreadsheet(
                    raw_flow=raw_flow,
                    reader=reader,
                    organization=org_destination
                )

                campaign, campaign_event, config_time = self.create_campaign(
                    reader=reader,
                    raw_flow=raw_flow,
                    flow=flow,
                    org=org_destination,
                    user=user,
                    group=group
                )

                serialized_data = [
                    serialize(
                        serializer_class=self.OrganizationSerializer,
                        instance=org_destination
                    ),
                    serialize(
                        serializer_class=self.FlowSerializer,
                        instance=flow
                    ),
                    serialize(
                        serializer_class=self.FlowRevisionSerializer,
                        instance=revision
                    ),
                    serialize(
                        serializer_class=self.ContactGroupSerializer,
                        instance=group
                    ),
                    serialize(
                        serializer_class=self.CampaignSerializer,
                        instance=campaign
                    ),
                    serialize(
                        serializer_class=self.CampaignEventSerializer,
                        instance=campaign_event,
                        config_time=config_time,
                    )
                ]

                keys = [
                    'organization', 'flow', 'flow_revision', 'group',
                    'campaign', 'campaign_event'
                ]

                list_serialized_data.append(
                    json_representation(keys, serialized_data)
                )

            for data in list_serialized_data:
                notificator = SlackFlowSchedulledNotification(
                    title='Fluxo Criado e Agendado!',
                    data=data
                )
                notificator.send_notification()

            reader.write_sheet_data(
                rows=spreadsheet_pos,
                value=reader.FlowColumns.CONTROL_TO_UPLOAD,
                control_column=reader.FlowColumns.UPLOAD
            )

            return list_serialized_data
