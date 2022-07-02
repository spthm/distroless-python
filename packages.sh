# Usage,
#   docker run --rm -it --entrypoint /bin/sh -v $(pwd)packages.sh:/tmp/packages.sh python:3.9-slim-bullseye /tmp/packages.sh

set -eu

depsdir="$(mktemp -d)"
trap 'rm -rf -- "$depsdir"' EXIT

# This script attempts to find all packages the python binaries depend on.
# First,
#   * find all shared object dependencies with ldd; then
#   * ignore anything in /usr/local, because they came from the Python install
#     itself, and we will handle that separately; then
#   * find the packages providing those objects with dpkg.
find /usr/local/ -type f -executable -exec ldd {} \; 2>&1 \
| sed --quiet 's/.* => \(.*\.so[^[:space:]]*\).*/\1/p' \
| grep --invert-match /usr/local \
| sort --unique \
| xargs dpkg --search \
| awk -F ': ' '{print $1}' \
> "$depsdir/direct"

echo "Found direct dependencies:"
cat "$depsdir/direct"

# Now,
#   * find, recursively, all dependencies of those packages.
# It's useful to see the full output from apt-cache depends before we select only
# the packages we want. We limit ourselves to only required dependencies that are
# already installed.
cat "$depsdir/direct" \
| xargs apt-cache depends --recurse --installed -o APT::Cache::ShowOnlyFirstOr=true --no-breaks --no-conflicts --no-enhances --no-recommends --no-replaces --no-suggests \
> "$depsdir/rdepends"

echo "\nFound resolved dependencies:"
cat "$depsdir/rdepends"

# Now,
#   * get just the packages (drop the dependency information); then
#   * remove some things we don't actually want in the final image.
# This set of exlcuded packages requires some manual tweaking, based on the output of
# the previous step! We remove,
#   * debconf, because we do not support package installation in the final image;
#   * dpkg, ditto, and because it is only required by readline-common;
#   * perl-base, because it is only required by debconf;
#   * readline-common, because it only includes documentation (nb: we must copy its
#     copyright notice over); and
#   * tar, because it is only required by dpkg.
exclude="-e debconf -e dpkg -e perl-base -e readline-common -e tar"
grep "^\w" "$depsdir/rdepends" \
| sort --unique \
| grep --invert-match --fixed-strings $exclude \
> "$depsdir/all"

echo "\nFinal set of packages to install:"
cat "$depsdir/all"
