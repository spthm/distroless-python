# python:3.11-slim-bullseye
FROM python@sha256:39cecc9cde774f9209ad26a0ab2dc4f5d10ba92d2913a835cebea3b402af8e8b AS build

RUN python --version && python -m sysconfig

ENV PACKAGES \
    libbz2-1.0 \
    libc6 \
    libcom-err2 \
    libcrypt1 \
    libexpat1 \
    libffi7 \
    libgcc-s1 \
    libgdbm6 \
    libgssapi-krb5-2 \
    libk5crypto3 \
    libkeyutils1 \
    libkrb5-3 \
    libkrb5support0 \
    liblzma5 \
    libncursesw6 \
    libnsl2 \
    libreadline8 \
    libsqlite3-0 \
    libssl1.1 \
    libtinfo6 \
    libtirpc3 \
    libuuid1 \
    zlib1g

# - dash -
# os.system may need a shell, obviously as does subprocess with shell=True. This isn't
# very 'distroless', but is arguably no less secure since similar damage could be done
# with the python binary itself. See also,
#   https://github.com/GoogleContainerTools/distroless/issues/601
#
# - debian-archive-keyring -
# This is for provenance of the installed packages. Our debian.sources file references
# /usr/share/keyrings/debian-archive-keyring.gpg.
#
# - libc-bin -
# This gives us ldconfig, used to configure the runtime image, and makes
# ctypes.find_library() work.
#
# - libgcc-s1 -
# This is a dependency of libstdc++6.
#
# - ligbomp -
# A few packages expect a system install of libgomp, e.g. lightgmb,
#   https://github.com/microsoft/LightGBM/issues/4484
#
# - libstdc++6 -
# This is for manylinux2010, manylinux2014 compatibility
ENV PACKAGES_EXTRA \
    dash \
    debian-archive-keyring \
    libc-bin \
    libgcc-s1 \
    libgomp1 \
    libstdc++6

ENV PACKAGES_COPYRIGHT \
    gcc-10-base \
    libtirpc-common \
    ncurses-base \
    readline-common

# We install packages from a debian snapshot archive for improved reproducibility.
RUN set -eux; \
    rm -rf /etc/apt/sources.list; \
    rm -rf /etc/apt/sources.list.d/*
COPY ./debian.sources /etc/apt/sources.list.d/debian.sources

# Download .deb files for our dependency packages, and install them to a new root
# filesystem at /tmp/rootfs.
RUN mkdir -p /tmp/rootfs; \
    mkdir -p /tmp/rootfs/var/lib/dpkg/info; \
    mkdir -p /tmp/rootfs/var/lib/dpkg/updates; \
    touch /tmp/rootfs/var/lib/dpkg/status
# We go to some effort to run a dpkg --install, rather than dpkg-deb -x, so that the
# runtime image has the correct dpkg info in /var/lib/dpkg, and so that -slim tweaks
# are applied (removing unneeded files like changelogs, etc.)
RUN set -eux; \
    rm -rf /tmp/debs; \
    mkdir /tmp/debs; \
    chown _apt:root /tmp/debs; \
    cd /tmp/debs; \
    apt-get update; \
    apt-get download ${PACKAGES} ${PACKAGES_EXTRA} ${PACKAGES_COPYRIGHT}; \
    # Based on
    #   https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=883700#10
    # --force-script-chrootless is necessary, otherwise pre- and post-installation
    # scripts fail (can't be found).
    DEBIAN_FRONTEND=noninteractive \
        dpkg \
        --force-depends \
        --force-script-chrootless \
        --root=/tmp/rootfs \
        --install /tmp/debs/*.deb; \
    rm -rf /tmp/debs; \
    rm -rf /var/lib/apt/lists/*

# Print all machine-readable licence information for the packages we are distributing.
# This is not exhaustive; not all copyright files use this format.
RUN grep -e '^Files:' -e '^License:' /tmp/rootfs/usr/share/doc/*/copyright

# Copy over the Python install. Everything in /usr/local is from Python, but we only
# want the binaries/libraries.
RUN mkdir -p /tmp/rootfs/usr/local
RUN cp --parents --archive --target-directory=/tmp/rootfs /usr/local/bin
RUN cp --parents --archive --target-directory=/tmp/rootfs /usr/local/lib

# Copy over static files we get from elsewhere, incuding the Python copyright notice.
COPY ./rootfs/ /tmp/rootfs/

# Explicitly remove a few things that we do not expect to be required,
# and/or will not work correctly E.g. idlelib needs tk support, but
# the -slim Python images do not support tk (libtk is missing).
RUN rm -rf /tmp/rootfs/usr/local/bin/idle*; \
    rm -rf /tmp/rootfs/usr/local/bin/2to3*; \
    rm -rf /tmp/rootfs/usr/local/bin/pip*; \
    rm -rf /tmp/rootfs/usr/local/bin/wheel; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.11/ensurepip; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.11/idlelib; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.11/lib2to3; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.11/tkinter; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.11/turtle.py; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.11/turtledemo; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.11/lib-dynload/_tkinter*.so*

# The final image provides no third-party packages. Note that among
# other things, this fully removes pip: the final image is not intended
# for installation of packages.
RUN rm -rf /tmp/rootfs/usr/local/lib/python3.11/site-packages/*


FROM gcr.io/distroless/static-debian11

LABEL org.opencontainers.image.licenses=GPL-3.0-or-later

ENV LANG=C.UTF-8

COPY --from=build /tmp/rootfs /

# Re-generate the ldconfig cache in the final stage to pick up the libpython in
# /usr/local/lib. The /etc/ld.so.cache from the build stage may include things
# we don't copy over.
RUN /sbin/ldconfig

ENTRYPOINT [ "python" ]
