FROM python:3.11-slim-bullseye AS venv

COPY requirements.txt /app/requirements.txt
RUN python -m venv --symlinks /app/venv

# Install wheel first to avoid issues with legacy 'setup.py install' method.
RUN /app/venv/bin/pip install --no-cache-dir wheel
RUN /app/venv/bin/pip install --no-cache-dir -r /app/requirements.txt

# This is not necessary, but recommended to save space, and because invocations of
# pip are not expected or supported in distroless-python runtime images. setuptools
# and wheel are also not required for this example, but consider that they may be
# needed by your applications!
RUN /app/venv/bin/pip uninstall -y pip wheel setuptools


FROM distroless-python:3.11-bullseye

# Don't buffer STDOUT, this is a demo. This may have a negative
# performance impact in real-world applications.
ENV PYTHONUNBUFFERED 1

# Use the same path in the runtime image as we used in the previous stage.
COPY --from=venv /app/venv /app/venv
COPY echo.py /app/
WORKDIR /app

# We need to override the default ENTRYPOINT to use our venv's python.
ENTRYPOINT [ "venv/bin/python", "echo.py", "--host", "0.0.0.0"]
