# No-dependencies

If you require only Python and its Standard Library, simply `COPY` your Python files into the image in your `Dockerfile`.

For the example in this directory,

```shell
$ docker build -t distroless-python-tcp-echo:3.11 .
[+] Building 0.9s (8/8) FINISHED
 => [internal] load build definition from Dockerfile
...
 => => naming to docker.io/library/distroless-python-tcp-echo:3.11
$ docker run --rm -p 8888:8888 distroless-python-tcp-echo:3.11
listening on 0.0.0.0:8888
```

(Hit Ctrl+C to quit.)

And in a separate shell (assuming MacOS - for other OSs, try `netcat`),

```shell
$ echo "hello" | nc 127.0.0.1 8888
hello
```
