from abc import ABC, abstractmethod
import os
import requests


class BaseSlackNotification(ABC):
    """
        Classe base que implementa os métodos fundamentais e configuração de webhook
        para enviar as notificações ao canal do slack.
    """

    def __init__(
        self, title, data,
        emoji=True,
        extra_params=None
    ):
        self.title = title
        self.emoji = emoji
        self.data = data
        self.extra_params = extra_params
        self.response = None

        self._payload = {}
        self._webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
        self._app = 'Cópia e Agendamento de Fluxos'

    @property
    def payload(self):
        """
            Retorna o payload que será enviado na requisição ao webhook do slack.
        """
        return self._payload

    def slack_payload_initialization(self):
        self._payload.update(
            {'blocks': []}
        )

    def slack_payload_header(self):

        header_obj = {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": self.title,
                "emoji": self.emoji
            }
        }

        return header_obj

    def slack_application_content(self):
        return {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Aplicação:* {self._app}"
                }
            ]
        }

    def validate_content_fields(self):

        mandatory_keys = ['type']
        declared_fields = ['fields', 'text']

        error = ''
        for payload_content in self._payload['blocks']:

            if not set(mandatory_keys).issubset(set(payload_content.keys())) or type(payload_content) != dict: # noqa
                error += 'Content must be a dict and must have "type" as key\n'
            if not any(field in declared_fields for field in payload_content):
                error += f'No declared fields found. Choices are: {declared_fields}'  # noqa
            if error:
                raise Exception(error)

    def send_slack_message(self):
        headers = {
            "content-type": "application/json"
        }
        data = dict(
            text='' if not self.extra_params else self.extra_params,
            **self._payload
        )

        response = requests.post(
            self._webhook_url,
            json=data,
            headers=headers,
            timeout=25
        )
        return response

    @abstractmethod
    def _build_notification_content(self):
        """
            Método que implementa as particularidades dos alertas de
            acordo com os parâmetros passados.
            - Deve ser obrigatoriamente sobrescrito.
        """
        raise NotImplementedError('This method must be overwritten.')

    def send_notification(self):

        self.slack_payload_initialization()

        self._build_notification_content()

        self.validate_content_fields()

        self.response = self.send_slack_message()


class SlackFlowSchedulledNotification(BaseSlackNotification):

    def slack_organization_content(self):
        return {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Organização:* {self.data['organization']['name']}\n *slug:* {self.data['organization']['slug']}" # noqa
                }
            ]
        }

    def slack_flow_content(self):
        return {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Fluxo:* {self.data['flow']['name']}\n *criado em:* {self.data['flow']['created_on']}" # noqa
                }
            ]
        }

    def slack_flow_revision_content(self):
        return {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Revisão do Fluxo:* {self.data['flow_revision']['revision']}\n *criado em:* {self.data['flow_revision']['created_on']}" # noqa
                }
            ]
        }

    def slack_campaign_content(self):
        return {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Campanha:* {self.data['campaign']['name']}\n *criada em:* {self.data['flow']['created_on']}" # noqa
                }
            ]
        }

    def slack_campaign_event_content(self):
        return {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Agendamento da Campanha:* {self.data['campaign_event']['config_time']}\n *criado em:* {self.data['campaign_event']['created_on']}" # noqa
                }
            ]
        }

    def slack_group_content(self):
        return {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": f"*Grupo de Contatos:* {self.data['group']['name']}"  # noqa
                }
            ]
        }

    def _build_notification_content(self):
        self._payload['blocks'].extend(
            [
                self.slack_payload_header(),
                self.slack_application_content(),
                self.slack_organization_content(),
                self.slack_flow_content(),
                self.slack_flow_revision_content(),
                self.slack_campaign_content(),
                self.slack_campaign_event_content(),
                self.slack_group_content()
            ]
        )
