from repo_mirror import mirror


def test_platform_tarballs(pkg_mirror):
    mirror.platform_tarballs('./', pkg_mirror)
    # figure out the assertions
    # remove the generated tarballs
