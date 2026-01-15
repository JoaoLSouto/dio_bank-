from ..app import ma

class UserSchema(ma.Schema):
    class Meta:
        fields=("id", "username", "role_id")