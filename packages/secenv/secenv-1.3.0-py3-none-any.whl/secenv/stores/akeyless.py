import akeyless
import akeyless.exceptions

from . import SecretNotFoundError, StoreInterface, ask_secret, cached, generate_secret


class Store(StoreInterface):
    def __init__(self, name, infos):
        self.name = name

        host = super().get_from_config(name, "host", infos, "https://api.akeyless.io")
        access_id = super().get_from_config(name, "access_id", infos)
        access_key = super().get_from_config(name, "access_key", infos)

        configuration = akeyless.Configuration(host=host)
        api_client = akeyless.ApiClient(configuration)
        api = akeyless.V2Api(api_client)

        body = akeyless.Auth(access_id=access_id, access_key=access_key)
        res = api.auth(body)
        token = res.token

        self.api = api
        self.token = token

    def gen_parser(self, parser):
        parser.add_argument("secret")

    @cached
    def read_secret(self, secret) -> str:
        body = akeyless.GetSecretValue(names=[secret], token=self.token)
        try:
            res = self.api.get_secret_value(body)
            if not isinstance(res, dict):
                raise Exception
            if secret not in res:
                raise SecretNotFoundError(self.name, secret)
            return res[secret]
        except akeyless.exceptions.ApiException as e:
            if e.reason == "Not Found":
                raise SecretNotFoundError(self.name, secret)

    def fill_secret(self, secret, generate=None, existing=None):
        if generate:
            secret_value = generate_secret(generate)
        else:
            secret_value = ask_secret(self.name, secret, existing=existing)
        if existing:
            body = akeyless.UpdateSecretVal(name=secret, value=secret_value, token=self.token)
            self.api.update_secret_val(body)
        else:
            body = akeyless.CreateSecret(name=secret, value=secret_value, token=self.token)
            self.api.create_secret(body)
