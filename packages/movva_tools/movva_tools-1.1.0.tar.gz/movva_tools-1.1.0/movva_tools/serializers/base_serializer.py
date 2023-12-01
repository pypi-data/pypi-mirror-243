from marshmallow import Schema, fields

serializer_fields = fields
date_field_format = serializer_fields.DateTime(
    dump_only=True, format='%d/%m/%Y %H:%M:%S'
)


class BaseSerializer(Schema):
    pass
