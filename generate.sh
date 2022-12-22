set -eux

tmpdir="$(mktemp -d)"
trap 'rm -rf -- "$tmpdir"' EXIT

for py in 3.7 3.8 3.9 3.10 3.11; do
    pkgs="${tmpdir}/${py}/packages"
    mkdir -p $(dirname "$pkgs")
    touch "$pkgs"

    name="python:${py}-slim-bullseye"
    docker pull "$name"
    digest=$(docker inspect --format='{{index .RepoDigests 0}}' "$name")

    docker run \
        --rm \
        -it \
        --entrypoint /bin/sh \
        -v "$(pwd)/scripts/debian/list-packages.sh:/list-packages.sh" \
        -v "$pkgs:/output" \
        "$digest" \
        /list-packages.sh

    python generate.py \
        --py "$py" \
        --image-name "$name" \
        --image-digest "$digest" \
        --package-list "$pkgs" \
        --outfile "${py}/Dockerfile"
done
