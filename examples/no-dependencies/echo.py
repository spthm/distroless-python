import argparse
import asyncio
from asyncio import StreamReader, StreamWriter


async def echo(r: StreamReader, w: StreamWriter):
    try:
        data = await r.readline()
        while data:
            if data.strip() == b"stop":
                break
            w.write(data)
            data = await r.readline()
    finally:
        w.close()


async def listen(host: str, port: int):
    listener = await asyncio.start_server(echo, host=host, port=port)
    return listener


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8888)
    args = parser.parse_args()

    loop = asyncio.new_event_loop()
    listener = loop.run_until_complete(listen(args.host, args.port))

    try:
        print(f"listening on {args.host}:{args.port}")
        loop.run_forever()
    except KeyboardInterrupt:
        listener.close()


if __name__ == "__main__":
    main()
