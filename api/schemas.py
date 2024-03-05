# api/schemas.py
from marshmallow import Schema, fields, validate

class ItemSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(max=255))
    id = fields.Int(required=True, validate=validate.Range(min=0))
    age = fields.Int(required=True, validate=validate.Range(min=15))