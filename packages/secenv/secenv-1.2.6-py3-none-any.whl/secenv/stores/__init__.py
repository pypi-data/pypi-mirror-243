import argparse
import importlib
import os
from abc import ABC, abstractmethod
import secrets
import string
from ..utils import (
    SecretGenerationError,
    SecretType,
    SecretTypeNotValidError,
    gen_uid,
    yes_no,
    SecretNotFoundError,
)


EnvPrefix = "SECENV"

cached_secrets = {}


def cached(fn):
    def inner(*args, **kwargs):
        # args[0] is `self`
        store = args[0].name
        cache_key = gen_uid(store, kwargs)

        if cache_key in cached_secrets:
            return cached_secrets[cache_key]

        result = fn(*args, **kwargs)
        cached_secrets[cache_key] = result

        return result

    return inner


def read_secret(store, args):
    key = None
    if "key" in args:
        key = args["key"]
        del args["key"]

    secret = store.read_secret(**args)
    if key:
        return store.filter(secret, key)
    else:
        return secret


def fill_secret(store, secret):
    secret_already_exists = False
    try:
        secret_without_keys_and_type = {k: v for k, v in secret.items() if k not in ["keys", "generate"]}
        if store.read_secret(**secret_without_keys_and_type):
            secret_already_exists = True
    except SecretNotFoundError:
        pass

    if secret_already_exists and not yes_no(
        f"Secret '{secret['secret']}' already exists in store '{store.name}', overwrite?"
    ):
        return

    if "generate" in secret:
        secret["generate"] = SecretType.from_config(secret["generate"])

    store.fill_secret(**secret)


def ask_secret(store, name, key=""):
    ask_str = f"Value for secret '{name}' in store '{store}'"
    if key:
        ask_str += f" (key: '{key}')"
    ask_str += "? "

    res = input(ask_str)

    while res.startswith("file:"):
        filename = res[5:].strip()
        if not os.path.exists(filename):
            print("File doesn't exist:", filename)
            res = input(ask_str)
            continue
        if not os.path.isfile(filename):
            print("This is not a file:", filename)
            res = input(ask_str)
            continue

        with open(filename, "r") as f:
            res = f.read()

    return res


def generate_secret(config: tuple) -> str:
    secret_type, secret_config = config

    if secret_type == SecretType.PASSWORD:
        length = int(secret_config.get("length", "24"))
        alphabets = secret_config.get("alphabets", [])
        if not alphabets:
            # We remove string.whitespace as it contains \t\r\n
            # which can break a _lot_ of things
            alphabet = string.printable.replace(string.whitespace, "")
        else:
            alphabet = ""
            string_dict = string.__dict__
            for a in alphabets:
                if a not in string_dict:
                    raise SecretGenerationError(
                        f"Alphabet not valid: '{a}' (try running 'import string; string.<alphabet>')"
                    )
                alphabet += string_dict[a]
        return "".join(secrets.choice(alphabet) for i in range(length))

    elif secret_type == SecretType.DUMMY:
        print("WARNING: using dummy password")
        return "password"

    else:
        raise SecretTypeNotValidError(secret_type)


class StoreInterface(ABC):
    @abstractmethod
    def __init__(self, name: str, infos: dict) -> None:
        """Init the store, check the provided keys, and create possible client"""
        ...

    def get_from_config(self, store: str, value: str, infos: dict, default=None) -> str:
        store_has_in_infos = lambda s: value in infos or f"{EnvPrefix}_{s}_{value}" in os.environ

        if not store_has_in_infos(store) and not ("extends" in infos and store_has_in_infos(infos["extends"])):
            if default is None:
                raise Exception(
                    f"Config error: '{value}' is required in store '{store}'" f" or {EnvPrefix}_{store}_{value} in env"
                )
            else:
                return default

        val = infos.get(value, os.getenv(f"{EnvPrefix}_{store}_{value}"))
        if not val and "extends" in infos:
            val = os.getenv(f"{EnvPrefix}_{infos['extends']}_{value}")
            if val is not None:
                return val
            if default is not None:
                return default
            raise Exception(
                f"Config error: '{value}' is required in store '{store}'" f" or {EnvPrefix}_{store}_{value} in env"
            )
        return val

    @abstractmethod
    def gen_parser(self, parser: argparse.ArgumentParser) -> None:
        """Generate the parser that reads the arguments and options"""
        ...

    @abstractmethod
    def read_secret(self, secret: str) -> str:
        """Read a secret from the desired password store"""
        ...

    @abstractmethod
    def fill_secret(self, secret: str, generate: SecretType) -> str:
        """Fill a secret in the password store"""
        ...
