set -eux

tmpdir="$(mktemp -d)"
trap 'rm -rf -- "$tmpdir"' EXIT

for py in 3.7 3.8 3.9 3.10 3.11; do
    mkdir -p "${tmpdir}/${py}"

    name="python:${py}-slim-bullseye"
    docker pull "$name"
    digest=$(docker inspect --format='{{index .RepoDigests 0}}' "$name")

    updates="${tmpdir}/${py}/updates"
    touch "$updates"
    docker run --rm -it --entrypoint /bin/sh \
        -v "${updates}:/updates" \
        -v "$(pwd)/tools/debian/list-updates.sh:/list-updates.sh:ro" \
        "${digest}" /list-updates.sh

    python generate.py \
        --py "$py" \
        --image-name "$name" \
        --image-digest "$digest" \
        --updates "$updates" \
        --outfile "${py}/Dockerfile"
done
