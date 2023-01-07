set -eux

tmpdir="$(mktemp -d)"
trap 'rm -rf -- "$tmpdir"' EXIT

for py in 3.7 3.8 3.9 3.10 3.11; do
    pkgs="${tmpdir}/${py}/packages"
    mkdir -p $(dirname "$pkgs")
    touch "$pkgs"

    suite="bullseye"
    name="python:${py}-slim-${suite}"
    docker pull "$name"
    digest=$(docker inspect --format='{{index .RepoDigests 0}}' "$name")

    pyv=$( \
        docker run \
            --rm \
            -it \
            "$digest" \
            python -c "from sys import version_info; print(f\"{version_info[0]}.{version_info[1]}.{version_info[2]}\")" \
        | tr -d '[:space:]')

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
        --suite "$suite" \
        --image-name "$name" \
        --image-digest "$digest" \
        --package-list "$pkgs"

    mkdir -p "${py}/rootfs/usr/local/share/doc/python${py}"
    curl "https://raw.githubusercontent.com/python/cpython/v${pyv}/LICENSE" -o "${py}/rootfs/usr/local/share/doc/python${py}/copyright"
done
