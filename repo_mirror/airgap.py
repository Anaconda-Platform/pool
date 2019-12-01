import os
import time
import logging
from argparse import ArgumentParser
from jinja2 import Environment, PackageLoader
from .log import initialize_log
from .mirror import download_pkgs, platform_tarballs
from .pool import upload_files


_logger = logging.getLogger(__file__)


def _default_mirror_configs(mirror_dir: str, log_level: str) -> tuple:
    """
    Load jinja templates for configs included with the package

    :rtype: tuple
    :return: abspath to files: (anaconda.yaml, r.yaml, msys2.yaml)
    """
    env = Environment(loader=PackageLoader('repo_mirror', 'templates'))

    configs = []
    for temp in ('anaconda.yaml', 'r.yaml', 'msys2.yaml'):
        temp = env.get_template(temp)
        cf = os.path.join(mirror_dir, temp.name)

        temp.stream(mirror_dir=mirror_dir,
                    log_dir=mirror_dir,
                    log_level=log_level).dump(cf)

        configs.append(cf)

    return configs


def _parse_args():
    parser = ArgumentParser(description="create airgap archive of conda channels")

    parser.add_argument('mirror_dir',
                        nargs='?',
                        default=os.path.abspath(os.curdir),
                        help='(default: os.curdir) packages get mirrored here')
    parser.add_argument('-f',
                        '--file',
                        nargs='+',
                        dest='mirror_configs',
                        default=[],
                        help='load mirror config yaml files from this directory')
    parser.add_argument('-m',
                        '--mirror-only',
                        dest='mirror_only',
                        action='store_true',
                        default=False,
                        help='create mirror of conda packages then exit')
    parser.add_argument('-l',
                        '--log-level',
                        dest='log_level',
                        action='store',
                        default='INFO',
                        choices=['ERROR', 'WARNING', 'INFO', 'DEBUG'],
                        help='log-level of ERROR, WARNING, INFO, DEBUG.'
                             'Default is INFO.')
    parser.add_argument('-b',
                        '--aws-bucket',
                        dest='aws_bucket',
                        action='store',
                        default='airgap-tarball',
                        help='aws bucket to which the tarballs are uploaded')
    parser.add_argument('-n',
                        '--upload-folder',
                        dest='folder_name',
                        action='store',
                        default=time.strftime("%Y_%m"),
                        help='upload to this folder; mostly for testing')
    args = parser.parse_args()

    # generate default yaml config files in mirror_dir
    if not args.mirror_configs:
        args.mirror_configs = _default_mirror_configs(args.mirror_dir,
                                                      args.log_level)

    return args


def main():
    args = _parse_args()
    initialize_log(args.log_level)
    _logger.info('initialized logger')

    # TODO: this is hacky; we should fix logging in cas_mirror
    for name in ('fetch.start', 'fetch.update', 'fetch.stop'):
        lgr = logging.getLogger(name)
        lgr.setLevel(logging.ERROR)

    # mirror packages
    channels = []
    for config_file in args.mirror_configs:
        channel = download_pkgs(config_file)
        #try:
        #    channel = download_pkgs(config_file)
        #except Exception as ex:
        #    _logger.info(f'mirror of {config_file} failed')
        #    continue

        channels.append(channel)

    # verify mirror - any testing of the mirror after creation?

    # upload it to AWS
    if args.mirror_only:
        return

    # create tarball
    files_to_upload = []
    for channel in channels:
        try:
            tarname = platform_tarballs(channel)
        except Exception as ex:
            _logger.info(f'platform tar creation of {channel} failed')
            continue

        files_to_upload.append(tarname)

    # upload files
    upload_files(args.aws_bucket, files_to_upload, args.folder_name)


if __name__ == '__main__':
    main()
