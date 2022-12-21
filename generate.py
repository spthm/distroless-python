import argparse
from datetime import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape

parser = argparse.ArgumentParser()
parser.add_argument("--py", type=str, required=True, help="Python version (MAJOR.MINOR)")
parser.add_argument("--image-name", type=str, required=True, help="Base image name")
parser.add_argument("--image-digest", type=str, required=True, help="Base image digest")
parser.add_argument("--updates", type=str, help="Path to a file containing packages to update")
parser.add_argument("--outfile", type=str, required=True, help="The output file")

args = parser.parse_args()

if args.updates is not None:
    with open(args.updates) as f:
        updates = [line.strip() for line in f]
else:
    updates = []

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)

template = env.get_template("Dockerfile.slim.jinja")
d = template.render(
    python_version=args.py,
    image_name=args.image_name,
    image_id=args.image_digest,
    # image_id="python@sha256:c7f0a41c47f3581ce7032e65fee9ea1a1958fa42140404e492a5927b38b2f631",
    updates=updates,
)

with open(args.outfile, "w") as f:
    f.write(d)
    if not d.endswith("\n"):
        f.write("\n")
