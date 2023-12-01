import json
import os
import re
import pandas as pd

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from movva_tools.constants import BaseEnum, GoogleSheets
from movva_tools.utils import (
    replace_newline_character_for_space, strip_whitespaces
)


# If modifying scopes, delete the file token.json.


class GoogleSheetsIntegration:

    def __init__(self, link, spreadsheet_page):
        self._link = link
        self.spreadsheet_page = spreadsheet_page
        self.service = None
        self._secret_manager_service = None
        self._spreadsheet_id = None
        self._spreadsheet_data = None
        self._scope = GoogleSheets.READ_ONLY_SCOPE

    def check_data(self):
        """
            Verifica se as informações necessárias para a classe
            foram informadas.
        """
        if not self._link or not self._spreadsheet_id or not self.spreadsheet_page:
            raise Exception('The spreadsheet link, name and id must be informed')

    def __extract_id_from_google_sheets_link(self):
        """
            Extrai o id do link da planilha do Google através do
            padrão de expressão regular
        """

        pattern = r'/d/([a-zA-Z0-9-_]+)'

        # Procura pelo padrão no link fornecido
        match = re.search(pattern, self._link)

        # Se houver uma correspondência, retorna o ID encontrado, caso contrário, retorna None
        if match:
            return match.group(1)
        else:
            raise Exception('Planilha não encontrada.')

    def __fetch_credentials_data(self):

        environment = None
        token_path = None
        creds_path = os.environ.get('CREDENTIALS_API_GOOGLE_SHEETS', None)

        if not creds_path:
            token_path = os.environ.get('TOKEN_LOCAL_PATH', '')
            creds_path = os.environ.get('CREDENTIALS_LOCAL_PATH', None)
            environment = 'local'
        else:
            token_path = os.environ.get('TOKEN_API_GOOGLE_SHEETS', None)
            environment = 'production'

        if not creds_path or not token_path:
            raise ConnectionError('As credenciais da API do Google Sheets não foram informadas.')

        return creds_path, token_path, environment

    def _validate_google_sheets_token(self, creds, creds_path, gsheets_token_path, environment):
        if environment == 'local':
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.

            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                # if creds and creds.expired and creds.refresh_token:
                #     creds.refresh(Request())
                # else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_path, self._scope
                )
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                print('Openning token.json file...')
                with open(gsheets_token_path, 'w') as token:
                    token.write(creds.to_json())

        else:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

        return creds

    def __authorize_google_sheets(self):
        """
            Cria/carrega credenciais de acesso da API do Google Sheets
            e inicia a conexão com a API.
        """
        creds_path, token_path, environment = self.__fetch_credentials_data()
        creds = None

        if environment != 'local':

            gsheets_token_path = json.loads(
                token_path
            )

            creds = Credentials.from_authorized_user_info(
                gsheets_token_path, self._scope
            )
        else:
            gsheets_token_path = token_path

            if os.path.exists(gsheets_token_path):
                creds = Credentials.from_authorized_user_file(
                    gsheets_token_path, self._scope
                )

        creds = self._validate_google_sheets_token(
            creds, creds_path, gsheets_token_path, environment
        )

        # Create Google Sheets connection
        service = build('sheets', 'v4', credentials=creds)

        return service

    def read_sheet_data(self, end_selection: str = None) -> list:
        """
            Lê e armazena em uma estrutura de listas o conteúdo da planilha.
        """

        self._spreadsheet_id = self.__extract_id_from_google_sheets_link()

        self.check_data()

        self.service = self.__authorize_google_sheets()

        # Call the Sheets API
        end_selection = end_selection if end_selection else 'BZ'
        sheet = self.service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=self._spreadsheet_id,
            range=f'{self.spreadsheet_page}!A1:{end_selection}'
        ).execute()

        values = result.get('values', [])

        if not values:
            raise Exception('Planilha sem informação.')

        self._spreadsheet_data = values

        return values


class FlowGoogleSheets(GoogleSheetsIntegration):

    def __init__(self, link, spreadsheet_page):
        super().__init__(link, spreadsheet_page)
        self.message_columns = None
        self._scope = GoogleSheets.DEFAULT_SCOPE

    class FlowColumns(BaseEnum):
        ORGANIZATION = 'Organização'
        ORGANIZATION_OF_TEMPLATE = 'Organização do template a copiar'
        CAMPAING_NAME = 'Campanha'
        FLOW = 'Nome do fluxo'
        SEND_DATE = 'Data de Envio'
        SEND_DAY = 'Dia da semana'
        SEND_TIME = 'Horário de Envio (Brasil)'
        REFERENCE_DATE = 'Data de referência'
        REFERENCE_HOUR = 'Hora de referência'
        DAYS_FROM_REFERENCE_DATE = 'Dias da data de referência'
        HOURS_FROM_REFERENCE_DATE = 'Horas da data de referência'
        LABEL_REFERENCE_DATE = 'Label Data de referência'
        MESSAGE_TYPE = 'Tipo de mensagem'
        TEMPLATE_FLOW = 'Template a copiar'
        MESSAGE_PATTERN = r'Mensagem#\d+'
        CONTACT_GROUP = 'Grupo'
        UPLOAD = 'Subir?'

        CONTROL_TO_UPLOAD = 'FALSO'
        CONTROL_NOT_UPLOADED = 'VERDADEIRO'

    def parse_no_newline_columns(self, columns: list):
        return [
            replace_newline_character_for_space(column) for column in columns
        ]

    def validate_message_columns(self, columns: list):
        message_columns_pattern = self.FlowColumns.MESSAGE_PATTERN

        flow_messages_list = [
            item for item in columns
            if re.search(message_columns_pattern, str(item))
        ]

        if not flow_messages_list:
            raise Exception('Não foram informadas mensagens.')

        self.message_columns = flow_messages_list
        return flow_messages_list

    def validate_spreadsheet_columns(self, columns: list):

        columns_messages = self.validate_message_columns(columns)

        flowcolumns_list = set(columns).difference(columns_messages)

        validation_columns = [
            column.value for column in self.FlowColumns
            if column.value not in
            (
                self.FlowColumns.MESSAGE_PATTERN,
                self.FlowColumns.CONTROL_TO_UPLOAD,
                self.FlowColumns.CONTROL_NOT_UPLOADED
            )
        ]

        try:
            assert all(
                column in flowcolumns_list for column in validation_columns
            )
        except Exception:
            raise Exception('As colunas esperadas da planilha não foram encontradas.')

    def read_sheet_data(self, end_selection: str = None) -> list:
        values = super().read_sheet_data(end_selection)
        columns = [strip_whitespaces(column) for column in values[0]]
        columns = self.parse_no_newline_columns(columns)
        data = pd.DataFrame(values[1:], columns=columns)

        self._spreadsheet_data = data
        self.validate_spreadsheet_columns(data.columns)

        return data

    def sheets_column(self, colunas_dataframe: int):
        if colunas_dataframe <= 0:
            raise ValueError("O número de colunas deve ser maior que zero.")

        coluna_sheets = ""
        while colunas_dataframe > 0:
            colunas_dataframe, remainder = divmod(colunas_dataframe - 1, 26)
            coluna_sheets = chr(remainder + ord('A')) + coluna_sheets

        return coluna_sheets

    def write_sheet_data(self, rows: list, value: str, control_column: str):
        """
            Escreve um valor em uma coluna específica para linhas específicas
            da planilha.
        """
        self.check_data()

        if not self.service:
            self.service = self.__authorize_google_sheets()

        sheet = self.service.spreadsheets()

        template_rows = [item['template'] for item in rows]
        flow_rows = [item['flow'] for item in rows]

        selection = template_rows + flow_rows
        selection.sort()

        # Escrever nas linhas específicas da coluna 'Feito'
        self._spreadsheet_data.loc[
            self._spreadsheet_data.index.isin(selection), control_column
        ] = value

        columns = len(self._spreadsheet_data.columns)
        cell = self.sheets_column(colunas_dataframe=columns)

        control_values = list(self._spreadsheet_data[self.FlowColumns.UPLOAD].values)
        values = []
        for value in control_values:
            values.append(
                [value]
            )

        # Escrever o DataFrame de volta na planilha
        sheet.values().update(
            spreadsheetId=self._spreadsheet_id,
            range=f'{self.spreadsheet_page}!{cell}2',
            body={'values': values},
            valueInputOption='RAW'
        ).execute()

        print(
            f'Valor "{value}" escrito na coluna "{control_column}".'
        )
