import os
import logging
from cas_mirror.config import Config
from cas_mirror.exceptions import ConfigError
from cas_mirror.sync_pkgs import sync_pkgs
from cas_mirror.sync_files import sync_files
import tarfile


_logger = logging.getLogger(__file__)


def download_pkgs(config_file):
    # verify config; return if exception is raised
    try:
        config = Config(path=config_file)
    except ConfigError as e:
        _logger.error('Configuration Error in file {}: {}'.format(
            config_file,
            e.message
        ))
        return

    # sync packages; return if exception is raised
    try:
        sync_pkgs(config)
    except Exception as ex:
        _logger.error('Sync error: {}'.format(ex.message))
        return

    # fetch installers;
    if config.fetch_installers and config.remote_url:
        sync_files(config)
    else:
        _logger.info('Installer synchronization disabled or "remote_url" not set.')

    # return path for each mirror
    return config.mirror_dir


def platform_tarballs(output_location, source_dir):
    """
    Expect folder to contain pkgs/{platform} with subfolder for each platform
    """
    channel = os.path.split(source_dir)[1]
    for platform in os.scandir(os.path.join(source_dir,'pkgs')):
        fname = channel + '-' + platform + '.tar.gz'
        tarname = os.path.join(output_location, fname)
        with tarfile.open(tarname, 'w:gz') as tgz:
            tgz.add(platform.path, recursive=True)

    return tarname
