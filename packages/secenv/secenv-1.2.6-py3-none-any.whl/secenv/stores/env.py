import os
from . import StoreInterface, cached, ask_secret, SecretNotFoundError, generate_secret


class Store(StoreInterface):
    def __init__(self, name, infos):
        self.name = name

    def gen_parser(self, parser):
        parser.add_argument("secret")

    @cached
    def read_secret(self, secret):
        res = os.getenv(secret)
        if res:
            return res
        else:
            raise SecretNotFoundError(self.name, secret)

    def fill_secret(self, secret, generate=None):
        if generate:
            secret_value = generate_secret(generate)
        else:
            secret_value = ask_secret(self.name, secret)
        os.environ[secret] = secret_value
