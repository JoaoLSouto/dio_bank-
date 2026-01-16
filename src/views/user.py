from ..app import ma
from marshmallow import fields


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "username")
        include_fk = True


class CreateUserSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    password = fields.Integer(required=True)
