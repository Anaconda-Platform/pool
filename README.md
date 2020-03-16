## airgap tool ##
Tool for creating an airgapped archive of conda packages.

1. uses `cas-mirror` to sync conda packages
2. creates platform tarballs
3. uploads it to AWS s3 bucket (defaults to: airgap.svc.anaconda.com)

### create archive ###
The easiest way to use it is to `conda install` the package in a conda
environment:

```
$ conda create -nairgap -c jsandhu -c ae5-admin repo_mirror
$ conda activate airgap
$ airgap -h
```

__NOTE__: `cas-mirror` is pulled from `ae5-admin` and `repo_mirror` is currently hosted on `jsandhu`.
__NOTE__: `cas-mirror` raises exception for `main` channel since it adds `platform` object that does not get converted to a dict or json correctly.
The hack for now is to add following code snippet on [sync_pkgs.py#L148](https://github.com/Anaconda-Platform/cas-mirror/blob/5.3.1-dkludt/cas_mirror/sync_pkgs.py#L146)

```
    if temp_dict.get('platform'):
      temp_dict['platform'] = temp_dict['platform'].value
```
Exception raised without the fix:

```
TypeError: Object of type 'Platform' is not JSON serializable
```

To see the exception raised, run `airgap -m -f anaconda.yaml` using the following config:

```
$ cat anaconda.yaml
mirror_dir: ./main
platforms:
  - osx-64
  - win-64
  - linux-64
fetch_installers: False
verify_checksum: True
log_dir: ./
log_level: INFO
python_versions:
  - 2.7
pkg_list:
  - defaults::numbapro
channels:
  - https://repo.anaconda.com/pkgs/main
  - https://repo.anaconda.com/pkgs/pro

```




TODO:

- [ ] Revisit logging; not sure we need a file & stdout?
- [ ] Finish documenting functions
- [ ] Move conda package to a more official location
- [ ] Generate and add md5 checksum files
- [ ] Should we tarballs per channel as well?
- [ ] Any other validation that we may want to do?
