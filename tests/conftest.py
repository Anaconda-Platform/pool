import pytest


@pytest.fixture(scope="function")
def pkg_mirror(tmpdir):
    channel = tmpdir.mkdir('main').mkdir('pkgs')
    for platform in ('linux-64', 'win-64', 'osx-64'):
        channel.mkdir(platform)

    # return channel's directory name as str:w
    return channel.dirname

