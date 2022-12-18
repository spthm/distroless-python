FROM python:3.9-slim-bullseye AS upgrades

# Python images may lag behind their Debian base images. Try to avoid building an image
# with CVEs that are already fixed in stable.

# debsecan requires Python3.9. To avoid possible issues with having both the system
# Python and a Python in /usr/local, we do this in a separate stage.
# TODO: having to do apt-get update twice wastes time. Can we do this in a
# single RUN if we just apt-get purge -y --auto-remove desecan at the end?
# TODO: this could actually be another script, updates.sh? Might make CI easier (can
# detect if there are any upgrades to install)?
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends debsecan

RUN debsecan --suite bullseye --format packages --only-fixed > /tmp/upgrades


FROM python:3.9-slim-bullseye AS build

# /tmp/upgrades may include updates to packages that were present in the upgrades stage
# only because they are debsecan dependencies. Use --only-upgrade to skip those.
COPY --from=upgrades /tmp/upgrades /tmp/upgrades
RUN set -eux; \
    apt-get update; \
    xargs --arg-file=/tmp/upgrades apt-get install -y --no-install-recommends --only-upgrade; \
    rm -rf /var/lib/apt/lists/*

# TODO: it would be better if the packages were listed directly in the Dockerfile.
# Generate Dockerfile with e.g. jinja?
COPY packages /tmp/packages
COPY packages-copyright /tmp/packages-copyright
COPY packages-extra /tmp/packages-extra

RUN set -eux; \
    apt-get update; \
    cat /tmp/packages-extra \
    | grep --invert-match -e '^#' \
    | xargs --no-run-if-empty apt-get install -y --no-install-recommends; \
    rm -rf /var/lib/apt/lists/*

# Find all the files provided by our dependency packages, and copy them to a new root
# filesystem at /tmp/rootfs.
RUN mkdir -p /tmp/rootfs
RUN set -eux; \
    cat /tmp/packages /tmp/packages-extra \
    | grep --invert-match -e '^#' \
    | xargs --no-run-if-empty dpkg --listfiles \
    | sort --unique \
    | perl -nE 'chomp; say if -f' \
    | xargs cp --parents --archive --target-directory=/tmp/rootfs
RUN set -eux; \
    xargs --arg-file /tmp/packages-copyright dpkg --listfiles \
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
    rm -rf /tmp/rootfs/usr/local/lib/python3.9/ensurepip; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.9/idlelib; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.9/lib2to3; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.9/tkinter; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.9/turtle.py; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.9/turtledemo; \
    rm -rf /tmp/rootfs/usr/local/lib/python3.9/lib-dynload/_tkinter*.so*

# The final image provides no third-party packages. Note that among
# other things, this fully removes pip: the final image is not intended
# for installation of packages.
RUN rm -rf /tmp/rootfs/usr/local/lib/python3.9/site-packages/*


FROM gcr.io/distroless/static-debian11

COPY --from=build /tmp/rootfs /

# Re-generate the ldconfig cache in the final stage to pick up the libpython in
# /usr/local/lib. The /etc/ld.so.cache from the build stage may include things
# we don't copy over.
RUN /sbin/ldconfig

ENTRYPOINT [ "python" ]
