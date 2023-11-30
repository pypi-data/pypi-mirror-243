from enum import Enum


def escape(s) -> str:
    s = repr(str(s))
    if "$" in s and s[0] == '"':
        # "$" -> "\$"
        s = s.replace("$", "\\$")
    if "\\'" in s and s[0] == "'":
        # '\'' -> ''"'"''
        # close single-quote and put double-quote around
        s = s.replace("\\'", "'\"'\"'")
    return s


def gen_uid(store, secret_def):
    # 1) sort the keys in 'secret_def' so, if the function is called again
    # and Python doesn't sort keys the same way, it doesn't matter
    sorted_keys = list(secret_def)
    sorted_keys.sort()

    # 2) ignore the 'key' and 'store' parameters as they are not used to retrieve
    # a secret directly
    # > 'store' is used in another way to specify where to retrieve the secret from
    # > 'key' is used to extract data from an already retrieved secret
    filtered_keys = [secret_def[k] for k in sorted_keys if k not in ["key", "store", "sensitive"]]

    # 3) generate the final string used as the unique ID
    return "-".join([store] + filtered_keys)


def yes_no(ask):
    return input(ask + " [yN] ").lower() in ["y", "yes"]


class SecretNotFoundError(Exception):
    def __init__(self, store, secret):
        super().__init__(f"Secret '{secret}' not found in store '{store}'")


class SecretTypeNotValidError(Exception):
    def __init__(self, type):
        super().__init__(f"Secret type '{type}' is not valid")


class SecretGenerationError(Exception):
    def __init__(self, msg):
        super().__init__(msg)


class SecretType(Enum):
    PASSWORD = "password"
    DUMMY = "dummy"

    @classmethod
    def from_config(cls, config):
        if "type" not in config:
            raise Exception("Secret generation config is missing 'type' field")

        for t in cls:
            if config["type"] == t.value:
                return (t, config)
        raise SecretTypeNotValidError(config["type"])
