# Distroless containers for Python

WIP repo for creating [distroless][distroless] or distroless-like containers for multiple Python versions.
Currently only Python 3.9 Dockerfiles exist, which you can [already get][distroless-python3] from the official distroless images!

## Distroless-ish

These images include the `dash` shell, since in general a shell is needed by elements of `os.system`, and by any code that runs `subprocess.run()` and friends with `shell=True`.
The image necessarily comes with a Python interpreter binary, from which arbitrary commands may be executed even without a shell installed, so inclusion of `dash` is not less secure _per se_.
See also a [related discussion][distroless-python-shell] on Google's distroless repo.

## Python support

Python 3.9.

### Standard Library

The following Python standard library packages and binaries are missing from these images,

* idle[lib]
* [lib]2to3
* ensurepip
* tkinter
* turtle
* turtledemo

`tk` support is not provided by the installed system packages, hence `idle`, `tkinter` and `turtle*` are also removed;
this is similar to the `python3.9-minimal` and `libpython3.9-stdlib` packages in Debian bullseye, and (hence) to Google's distroless Python image.

`ensurepip` is removed as, by design, packages should not be installed into the image with `pip`;
`python3.9-minimal` and `libpython3.9-stdlib` also do not provide `ensurepip`.

`[lib]2to3` is not expected to be used, and again is also missing from `python3.9-minimal` and `libpython3.9-stdlib`.

### `manylinux20XX` Compatibility

Images have partial [`manylinux2010`][manylinux2010-policy] and [`manylinux2014`][manylinux2014-policy] compatibility.
The following libraries are omitted on the basis that they are not typically used in a distroless context and are non-negligible in size.
See also a [related discussion][docker-official-python-manylinux] on the Docker Official Images for Python.

#### GL libraries

* libgl1
* libglib2.0-0

#### X11 libraries

* libice6
* libsm6
* libx11-6
* libxext6
* libxrender1

## Licence

Files in this repository are under AGPLv3.
Pre-built images (not yet available) are licensed separately.

View license information for [Python 3][py3-licence].

As with all Docker images, these likely also contain other software which may be under other licenses (such as Bash, etc from the base distribution, along with any direct or indirect dependencies of the primary software being contained).

Some additional license information which was able to be auto-detected might be found in [the `repo-info` repository's `python/` directory][docker-python-repoinfo].

As for any pre-built image usage, it is the image user's responsibility to ensure that any use of this image complies with any relevant licenses for all software contained within.

[distroless]: https://github.com/GoogleContainerTools/distroless
[distroless-python3]: https://github.com/GoogleContainerTools/distroless/tree/main/experimental/python3
[distroless-python-shell]: https://github.com/GoogleContainerTools/distroless/issues/601
[manylinux2010-policy]: https://peps.python.org/pep-0571/#the-manylinux2010-policy
[manylinux2014-policy]: https://peps.python.org/pep-0599/#the-manylinux2014-policy
[docker-official-python-manylinux]: https://github.com/docker-library/python/issues/750
[py3-licence]: https://docs.python.org/3/license.html
[docker-python-repoinfo]: https://github.com/docker-library/repo-info/tree/master/repos/python
