from marshmallow import Schema, fields


class LoginSchema(Schema):
    """Данная модель нужна только для описания и тестирования и описания в
    Swagger через APi валидировать через неё запрещенно!!!
    """

    login = fields.Str(required=True)
    password = fields.Str(required=True)
    ip_addr = fields.Str(required=False, load_only=True)  # IP-адрес может быть, но не обязательный

    csrf_token = fields.Str(required=False, load_only=True)  # CSRF токен
    submit = fields.Str(required=False, load_only=True)  # Submit не учитывается
