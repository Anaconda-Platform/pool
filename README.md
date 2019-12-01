## airgap tool ##
Tool for creating an airgapped archive of conda packages.

1. uses `cas-mirror` to sync conda packages
2. creates platform tarballs
3. uploads it to AWS s3 bucket (defaults to: airgap.svc.anaconda.com)

### create archive ###
The easiest way to use it is to `conda install` the package in a conda
environment:

```
$ conda create -nairgap -c jsandhu repo_mirror
$ conda activate airgap
$ airgap -h
```

TODO:
#. Revisit logging; not sure we need a file & stdout?
#. Finish documenting functions
#. Move conda package to a more official location
#. Generate and add md5 checksum files
#. Should we tarballs per channel as well?
#. Any other validation that we may want to do?
