from .utils import with_tmp_dir, with_tmp_conf, write, skip_unimplemented_test

import secenv


@with_tmp_dir
def test_no_config():
    secenv.load_config()
    assert secenv.no_config_available


@with_tmp_conf
def test_empty_config(config):
    config.flush()
    secenv.load_config()
    assert secenv.no_config_available


@with_tmp_conf
def test_validate_store_no_type_no_extend(config):
    config_as_py = {"stores": {"my_store": {}}}
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert errors
    assert "Store 'my_store' contains neither 'type' nor 'extends' keys" in errors


@with_tmp_conf
def test_validate_store_no_type_inexistent_extends(config):
    config_as_py = {"stores": {"my_store": {"extends": "nothing"}}}
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert errors
    assert "Store 'my_store' extends an inexistent store 'nothing'" in errors


@with_tmp_conf
def test_validate_store_both_type_and_extends(config):
    config_as_py = {"stores": {"my_store": {"extends": "something", "type": "something"}}}
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert errors
    assert "Store 'my_store' contains both 'type' and 'extends' keys" in errors


@with_tmp_conf
def test_validate_store_type_ok(config):
    config_as_py = {"stores": {"my_store": {"type": "something"}}}
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert errors == []


@with_tmp_conf
def test_validate_store_extends_ok(config):
    config_as_py = {"stores": {"extending": {"extends": "extended"}, "extended": {"type": "type"}}}
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert errors == []


@with_tmp_conf
def test_validate_secret_missing_store(config):
    config_as_py = {
        "secrets": [{"secret": "my_secret"}],
    }
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert "Secret 0 doesn't contain the 'store' key" in errors


@with_tmp_conf
def test_validate_secret_missing_secret(config):
    config_as_py = {
        "secrets": [{"store": "inexistent"}],
    }
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert "Secret 0 doesn't contain the 'secret' key" in errors


@with_tmp_conf
def test_validate_secret_inexistent_store(config):
    config_as_py = {
        "secrets": [{"secret": "my_secret", "store": "inexistent"}],
    }
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert "Secret 0 references an inexistent store 'inexistent'" in errors


@with_tmp_conf
def test_validate_secret_generate_no_type(config):
    config_as_py = {
        "secrets": [{"generate": {}}],
    }
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert "Secret 0 generation doesn't have a type" in errors


@with_tmp_conf
def test_validate_secret_ok(config):
    config_as_py = {
        "stores": {"my_store": {"type": "my_type"}},
        "secrets": [
            {
                "secret": "my_secret",
                "store": "my_store",
                "generate": {"type": "my_type"},
            },
        ],
    }
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert errors == []


@with_tmp_conf
def test_validate_context_extends_inexistent(config):
    config_as_py = {"contexts": {"ctx": {"extends": ["inexistent"]}}}
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert "Context 'ctx' extends an inexistent context 'inexistent'" in errors


@with_tmp_conf
def test_validate_context_extends_ok(config):
    config_as_py = {"contexts": {"extended": {}, "extending": {"extends": ["extended"]}}}
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert errors == []


@with_tmp_conf
def test_validate_context_vars_missing_store_secret_keys(config):
    config_as_py = {"contexts": {"ctx": {"vars": {"VAR": {}}}}}
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert "Secret 'ctx/VAR' doesn't contain the 'store' key" in errors
    assert "Secret 'ctx/VAR' doesn't contain the 'secret' key" in errors


@with_tmp_conf
def test_validate_context_vars_key_wrong_type(config):
    config_as_py = {"contexts": {"ctx": {"vars": {"VAR": {"key": True}}}}}
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert "Secret 'ctx/VAR' defines 'key' with wrong type '<class 'bool'>' (expects 'str')" in errors


@with_tmp_conf
def test_validate_context_vars_sensitive_wrong_type(config):
    config_as_py = {"contexts": {"ctx": {"vars": {"VAR": {"sensitive": 42}}}}}
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert "Secret 'ctx/VAR' defines 'sensitive' with wrong type '<class 'int'>' (expects 'bool')" in errors


@with_tmp_conf
def test_validate_context_vars_store_not_found(config):
    config_as_py = {"contexts": {"ctx": {"vars": {"VAR": {"store": "inexistent"}}}}}
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert "Secret 'ctx/VAR' references an inexistent store 'inexistent'" in errors


@with_tmp_conf
def test_validate_context_vars_ok(config):
    config_as_py = {
        "stores": {"my_store": {"type": "ok"}},
        "contexts": {"ctx": {"vars": {"VAR": {"store": "my_store", "secret": "sec"}, "VAR2": "ok"}}},
    }
    write(config, config_as_py)

    errors = secenv.validate_config()
    assert errors == []
