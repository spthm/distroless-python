FROM distroless-python:3.11-bullseye

# Don't buffer STDOUT, this is a demo. This may have a negative
# performance impact in real-world applications.
ENV PYTHONUNBUFFERED 1

COPY echo.py /app/
WORKDIR /app

CMD [ "echo.py", "--host", "0.0.0.0"]
