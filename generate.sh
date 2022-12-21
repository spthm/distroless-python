set -eux

for py in 3.7 3.8 3.9 3.10 3.11; do
    name="python:${py}-slim-bullseye"
    docker pull "$name"
    digest=$(docker inspect --format='{{index .RepoDigests 0}}' "$name")

    python generate.py \
        --py "$py" \
        --image-name "$name" \
        --image-digest "$digest" \
        --outfile "${py}/Dockerfile"
done
