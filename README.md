# Distroless containers for Python

WIP repo for creating [distroless][distroless] or distroless-like containers for multiple Python versions.
Currently only Python 3.9 Dockerfiles exist, which you can [already get][distroless-python3] from the official distroless images!

## Licence

Files in this repository are under AGPLv3.
Pre-built images (not yet available) are licensed separately.

View license information for [Python 3][py3-licence].

As with all Docker images, these likely also contain other software which may be under other licenses (such as Bash, etc from the base distribution, along with any direct or indirect dependencies of the primary software being contained).

Some additional license information which was able to be auto-detected might be found in [the `repo-info` repository's `python/` directory][docker-python-repoinfo].

As for any pre-built image usage, it is the image user's responsibility to ensure that any use of this image complies with any relevant licenses for all software contained within.

[distroless]: https://github.com/GoogleContainerTools/distroless
[distroless-python3]: https://github.com/GoogleContainerTools/distroless/tree/main/experimental/python3
[py3-licence]: https://docs.python.org/3/license.html
[docker-python-repoinfo]: https://github.com/docker-library/repo-info/tree/master/repos/python
