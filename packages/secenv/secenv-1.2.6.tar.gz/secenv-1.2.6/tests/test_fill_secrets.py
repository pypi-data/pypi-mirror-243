import io
import string
from unittest import mock

import pytest
import secenv
from tests.utils import with_tmp_conf, with_tmp_dir, write


@with_tmp_conf
def test_store_not_found(config):
    config_as_py = {"secrets": [{"secret": "whatever", "store": "not_existent"}]}
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()

    with pytest.raises(SystemExit):
        secenv.fill_secrets(stores)


@with_tmp_conf
def test_stdin(config):
    config_as_py = {
        "stores": {"local": {"type": "env"}},
        "secrets": [{"secret": "STDIN", "store": "local"}],
    }
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()

    with mock.patch("sys.stdin", io.StringIO("password")):
        secenv.fill_secrets(stores)

    secret = secenv.read_secret(stores["local"], {"secret": "STDIN"})
    assert secret == "password"


@with_tmp_dir
def test_file():
    config_as_py = {
        "stores": {"local": {"type": "env"}},
        "secrets": [{"secret": "FILE", "store": "local"}],
    }
    write(open(".secenv.yml", "w"), config_as_py)
    with open("password-file", "w") as f:
        f.write("yay!")

    secenv.load_config()
    stores = secenv.find_stores()

    with mock.patch("sys.stdin", io.StringIO("file: password-file")):
        secenv.fill_secrets(stores)

    secret = secenv.read_secret(stores["local"], {"secret": "FILE"})
    assert secret == "yay!"


@with_tmp_conf
def test_generate_dummy(config):
    config_as_py = {
        "stores": {"local": {"type": "env"}},
        "secrets": [{"secret": "DUMMY", "store": "local", "generate": {"type": "dummy"}}],
    }
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    secenv.fill_secrets(stores)
    secret = secenv.read_secret(stores["local"], {"secret": "DUMMY"})
    assert secret == "password"
    for letter in secret:
        assert letter in string.printable


@with_tmp_conf
def test_generate_password_no_args(config):
    config_as_py = {
        "stores": {"local": {"type": "env"}},
        "secrets": [{"secret": "NO_ARGS", "store": "local", "generate": {"type": "password"}}],
    }
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    secenv.fill_secrets(stores)
    secret = secenv.read_secret(stores["local"], {"secret": "NO_ARGS"})
    assert len(secret) == 24
    for letter in secret:
        assert letter in string.printable


@with_tmp_conf
def test_generate_password_length(config):
    config_as_py = {
        "stores": {"local": {"type": "env"}},
        "secrets": [
            {
                "secret": "LENGTH",
                "store": "local",
                "generate": {"type": "password", "length": "8"},
            }
        ],
    }
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    secenv.fill_secrets(stores)
    secret = secenv.read_secret(stores["local"], {"secret": "LENGTH"})
    assert len(secret) == 8
    for letter in secret:
        assert letter in string.printable


@with_tmp_conf
def test_generate_password_alphabets_not_found(config):
    config_as_py = {
        "stores": {"local": {"type": "env"}},
        "secrets": [
            {
                "secret": "ALPHABETS_NOT_FOUND",
                "store": "local",
                "generate": {"type": "password", "alphabets": ["not_found"]},
            }
        ],
    }
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    with pytest.raises(Exception):
        secenv.fill_secrets(stores)


@with_tmp_conf
def test_generate_password_alphabets_default(config):
    config_as_py = {
        "stores": {"local": {"type": "env"}},
        "secrets": [
            {
                "secret": "ALPHABETS_DEFAULT",
                "store": "local",
                "generate": {"type": "password", "alphabets": []},
            }
        ],
    }
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    secenv.fill_secrets(stores)
    secret = secenv.read_secret(stores["local"], {"secret": "ALPHABETS_DEFAULT"})
    assert len(secret) == 24
    for letter in secret:
        assert letter in string.printable


@with_tmp_conf
def test_generate_password_alphabets_digits(config):
    config_as_py = {
        "stores": {"local": {"type": "env"}},
        "secrets": [
            {
                "secret": "ALPHABETS_DIGITS",
                "store": "local",
                "generate": {"type": "password", "alphabets": ["digits"]},
            }
        ],
    }
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    secenv.fill_secrets(stores)
    secret = secenv.read_secret(stores["local"], {"secret": "ALPHABETS_DIGITS"})
    assert len(secret) == 24
    for letter in secret:
        assert letter in string.digits


@with_tmp_conf
def test_generate_password_length_alphabets_digits(config):
    config_as_py = {
        "stores": {"local": {"type": "env"}},
        "secrets": [
            {
                "secret": "LENGTH_ALPHABETS_DIGITS",
                "store": "local",
                "generate": {
                    "type": "password",
                    "length": "8",
                    "alphabets": ["digits"],
                },
            }
        ],
    }
    write(config, config_as_py)

    secenv.load_config()
    stores = secenv.find_stores()
    secenv.fill_secrets(stores)
    secret = secenv.read_secret(stores["local"], {"secret": "LENGTH_ALPHABETS_DIGITS"})
    assert len(secret) == 8
    for letter in secret:
        assert letter in string.digits
