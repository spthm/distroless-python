import argparse
import urllib.request
import urllib.response
from datetime import datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


_here = Path(__file__).parent

class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, url, fp, errcode, errmsg, headers, data=None):
        # Return the initial 302 response so we can examine its Location header.
        return urllib.response.addinfourl(fp, headers, url, errcode)


def _resolve_snapshot_timestamp(prefix: str) -> str:
    """Return the most recent snapshot timestamp for a snapshot.debian URL.

    The prefix should be of the form http[s]://snapshot.debian.org/archive/*
    """
    now = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    # Trailing slash is important, otherwise we'll receive a 308 to the URL
    # with the trailing slash!
    req = urllib.request.Request(f"{prefix}/{now}/", method="HEAD")
    response = urllib.request.build_opener(_NoRedirect()).open(req)
    assert response.status == 302

    *_, timestamp = response.headers["location"].rstrip("/").split("/")
    return timestamp


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


debian_timestamp = _resolve_snapshot_timestamp(
    "https://snapshot.debian.org/archive/debian/"
)
security_timestamp = _resolve_snapshot_timestamp(
    "https://snapshot.debian.org/archive/debian-security/"
)
sources = env.get_template("debian.sources.jinja")
render = sources.render(
    suite=args.suite,
    debian_timestamp=debian_timestamp,
    security_timestamp=security_timestamp,
)
_write_render(render, _here / args.py / "debian.sources")
