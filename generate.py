import argparse
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


_here = Path(__file__).parent

def _write_render(render: str, to: Path):
    to.parent.mkdir(parents=True, exist_ok=True)

    with open(to, "w") as f:
        f.write(render)
        if not render.endswith("\n"):
            f.write("\n")


parser = argparse.ArgumentParser()
parser.add_argument("--py", type=str, required=True, help="Python version (MAJOR.MINOR)")
parser.add_argument("--image-name", type=str, required=True, help="Base image name")
parser.add_argument("--image-digest", type=str, required=True, help="Base image digest")
parser.add_argument("--package-list", type=str, required=True, help="Path to a file containing the list of packages")
parser.add_argument("--suite", type=str, required=True, help="Debian suite")

args = parser.parse_args()

with open(args.package_list) as f:
    packages = [line.strip() for line in f]

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)

dockerfile = env.get_template(f"Dockerfile.{args.suite}.jinja")
render = dockerfile.render(
    python_version=args.py,
    image_name=args.image_name,
    image_id=args.image_digest,
    packages=packages,
)
_write_render(render, _here / args.py / "Dockerfile")


now = datetime.utcnow()
snapshot_timestamp = now.strftime("%Y%m%dT%H%M%SZ")
sources = env.get_template("debian.sources.jinja")
render = sources.render(
    suite=args.suite,
    timestamp=snapshot_timestamp,
)
_write_render(render, _here / args.py / "debian.sources")
