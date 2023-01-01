import argparse

from jinja2 import Environment, FileSystemLoader, select_autoescape

parser = argparse.ArgumentParser()
parser.add_argument("--py", type=str, required=True, help="Python version (MAJOR.MINOR)")
parser.add_argument("--image-name", type=str, required=True, help="Base image name")
parser.add_argument("--image-digest", type=str, required=True, help="Base image digest")
parser.add_argument("--package-list", type=str, required=True, help="Path to a file containing the list of packages")
parser.add_argument("--outfile", type=str, required=True, help="The output file")

args = parser.parse_args()

with open(args.package_list) as f:
    packages = [line.strip() for line in f]

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)

template = env.get_template("Dockerfile.bullseye.jinja")
d = template.render(
    python_version=args.py,
    image_name=args.image_name,
    image_id=args.image_digest,
    packages=packages,
)

with open(args.outfile, "w") as f:
    f.write(d)
    if not d.endswith("\n"):
        f.write("\n")
