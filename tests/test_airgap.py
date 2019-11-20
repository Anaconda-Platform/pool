import pytest
import os
from ruamel_yaml import YAML
from repo_mirror.airgap import _default_mirror_configs


def test__default_mirror_configs_exception():
    """tests exception raised"""
    with pytest.raises(FileNotFoundError):
        _default_mirror_configs("./not-exist", "DEBUG")


def test__default_mirror_configs_jinja(tmpdir):
    """test jinja parsing is correct/valid"""
    ll = "DEBUG"
    mirror_dir = tmpdir.mkdir("mirror_dir").strpath
    configs = _default_mirror_configs(mirror_dir, ll)

    for conf in configs:
        assert os.path.exists(conf)
        with open(conf, 'r') as fp:
           yaml = YAML().load(fp)
           assert yaml["mirror_dir"].startswith(mirror_dir)
           assert yaml["log_dir"].startswith(mirror_dir)
           assert yaml["log_level"] == ll

