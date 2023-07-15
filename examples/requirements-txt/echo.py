import argparse

from flask import Flask


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    app = Flask(__name__)

    @app.route("/echo/<path>")
    def echo(path):
        return path

    app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
