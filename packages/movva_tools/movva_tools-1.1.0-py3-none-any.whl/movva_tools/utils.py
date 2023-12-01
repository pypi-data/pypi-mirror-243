from datetime import datetime
import pandas as pd
from more_itertools import chunked
from typing import Dict, List, Union
import json

DATE_FORMAT = "%d/%m/%Y"
TIME_FORMAT = "%H:%M:%S"


def set_prenome_column(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df['PRENOME'] = df['NOME'].apply(lambda x: x.split()[0])
        return df
    except KeyError:
        raise KeyError('A chave NOME é obrigatória na planilha.')


def date_formatter(df: pd.DataFrame, birth_date_column: str) -> pd.DataFrame:
    df[f'{birth_date_column}_FORMATADA'] = pd.to_datetime(
        df[birth_date_column], format='"%Y-%m-%dT%H:%M:%SZ"'
    )

    df[f'{birth_date_column}_FORMATADA'] = df[f'{birth_date_column}_FORMATADA'].astype(str)

    return df


def strip_whitespaces(data: str):
    return data.strip()


def replace_newline_character_for_space(data: str):
    return data.replace('\n', ' ')


def break_list_into_groups(input_list, chunk_size=100) -> list:
    """
        Determina uma lista que contém lotes de tamanho informado em
        chunk_size.
    """
    return list(chunked(input_list, chunk_size))


def datetime_string_parser(date_str: str, pattern: str):
    if not date_str:
        return date_str
    try:
        data = datetime.strptime(date_str, pattern)
        return data
    except ValueError:
        raise ValueError('Incorrect format of date and time.')


def json_representation(
    keys: list, serialized_data: List[Dict]
) -> Union[List[Dict], Dict]:

    result = {key: json.loads(value) for key, value in zip(keys, serialized_data)}
    return result


def serialize(serializer_class, instance, config_time=None):
    if config_time:
        serializer = serializer_class(config_time=config_time)
    else:
        serializer = serializer_class()
    return serializer.dumps(instance)
