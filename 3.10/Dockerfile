# python:3.10-slim-bullseye
FROM python@sha256:9430c5ad0286ca319db20286538d5051ad098ae3c38e530fa430953f76b710fb AS build

ENV PACKAGES \
    gcc-10-base \
    libacl1 \
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
    libpcre2-8-0 \
    libreadline8 \
    libselinux1 \
    libsqlite3-0 \
    libssl1.1 \
    libtinfo6 \
    libtirpc-common \
    libtirpc3 \
    libuuid1 \
    zlib1g

# TODO: add libdb5.3? and/or remove libgdbm6? (also change test.py!)
#
# - dash -
# os.system may need a shell, obviously as does subprocess with shell=True. This isn't
# very 'distroless', but is arguably no less secure since similar damage could be done
# with the python binary itself. See also,
#   https://github.com/GoogleContainerTools/distroless/issues/601
#
# - libc-bin -
# This gives us ldconfig, used to configure the runtime image, and makes
# ctypes.find_library() work.
#
# - ligbomp -
# A few packages expect a system install of libgomp, e.g. lightgmb,
#   https://github.com/microsoft/LightGBM/issues/4484
#
# - libstdc++6 -
# This is for manylinux2010, manylinux2014 compatibility
ENV PACKAGES_EXTRA \
    dash \
    libc-bin \
    libgomp1 \
    libstdc++6

ENV PACKAGES_COPYRIGHT \
    readline-common


RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends ${PACKAGES} ${PACKAGES_COPYRIGHT} ${PACKAGES_EXTRA}; \
    rm -rf /var/lib/apt/lists/*

# Find all the files provided by our dependency packages, and copy them to a new root
# filesystem at /tmp/rootfs.
RUN mkdir -p /tmp/rootfs
RUN set -eux; \
    echo ${PACKAGES} ${PACKAGES_EXTRA} \
    | xargs dpkg --listfiles \
    | sort --unique \
    | perl -nE 'chomp; say if -f' \
    | xargs cp --parents --archive --target-directory=/tmp/rootfs
RUN set -eux; \
    echo ${PACKAGES_COPYRIGHT} \
    | xargs dpkg --listfiles \
    | grep -i copyright \
    | perl -nE 'chomp; say if -f' \
    | xargs cp --parents --archive --target-directory=/tmp/rootfs

# Copy over the Python install. Everything in /usr/local is from Python, but we only
# want the binaries/libraries.
RUN mkdir -p /tmp/rootfs/usr/local
RUN cp --parents --archive --target-directory=/tmp/rootfs /usr/local/bin
RUN cp --parents --archive --target-directory=/tmp/rootfs /usr/local/lib

# Explicitly remove a few things that we do not expect to be required,
# and/or will not work correctly E.g. idlelib needs tk support, but
# the -slim Python images do not support tk (libtk is missing).
RUN rm -rf /tmp/rootfs/usr/local/bin/idle*; \
    rm -rf /tmp/rootfs/usr/local/bin/2to3*; \
    rm -rf /tmp/rootfs/usr/local/bin/pip*; \
    rm -rf /tmp/rootfs/usr/local/bin/wheel; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.10/ensurepip; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.10/idlelib; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.10/lib2to3; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.10/tkinter; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.10/turtle.py; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.10/turtledemo; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.10/lib-dynload/_tkinter*.so*

# The final image provides no third-party packages. Note that among
# other things, this fully removes pip: the final image is not intended
# for installation of packages.
RUN rm -rf /tmp/rootfs/usr/local/lib/python3.10/site-packages/*


FROM gcr.io/distroless/static-debian11

ENV LANG=C.UTF-8

COPY --from=build /tmp/rootfs /

# Re-generate the ldconfig cache in the final stage to pick up the libpython in
# /usr/local/lib. The /etc/ld.so.cache from the build stage may include things
# we don't copy over.
RUN /sbin/ldconfig

ENTRYPOINT [ "python" ]
