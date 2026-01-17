from ..app import ma
from marshmallow import fields
from ..models.user import User


class UserSchema(ma.SQLAlchemySchemaAutoSchema):
    class Meta:
        model = User
        include_fk = True


class CreateUserSchema(ma.Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    password = fields.Integer(required=True, strict=True)
