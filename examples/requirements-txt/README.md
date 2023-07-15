# Using a `requirements.txt`

If you have dependencies on Python packages outside of the standard library, run a multi-stage build as in the `Dockerfile` in this directory.

The build process has two stages,

1. We use the corresponding `python` image to create a virtual environment, into which our dependencies are installed.
2. We `COPY` this virtual environment to our runtime `distroless-python` image, and set its `python` as the `ENTRYPOINT`.

For the example in this directory,

```shell
$ docker build -t distroless-python-http-echo:3.11 .
[+] Building 0.9s (8/8) FINISHED
 => [internal] load build definition from Dockerfile
...
 => => naming to docker.io/library/distroless-python-http-echo:3.11
$ docker run --rm -p 8080:8080 distroless-python-http-echo:3.11
listening on 0.0.0.0:8080
```

(Hit Ctrl+C to quit.)

And in a separate shell,

```shell
$ curl -X GET 127.0.0.1:8080/echo/hello-world
hello-world
```
