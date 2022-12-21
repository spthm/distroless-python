# Usage,
#   docker run --rm -it --entrypoint /bin/sh \
#     -v $(pwd)/list-updates.sh:/list-updates.sh \
#     -v /some/path/to/updates:/updates \
#     python:3.9-slim-bullseye /list-updates.sh
# It's seemingly impossible to make apt-get entirely silent, so we write the output
# to a file.
# This isn't entirely reliable, as it may include in the output only packages that were
# installed as debsecan dependencies.

set -e

apt-get update -qq -y
apt-get install -qq -y --no-install-recommends debsecan

debsecan --suite bullseye --format packages --only-fixed | tee /updates
