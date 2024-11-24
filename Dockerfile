FROM python:3.13-slim-bullseye as base

FROM base as build
RUN apt-get update && apt-get install -y --no-install-recommends gcc
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy

FROM base AS runtime
RUN apt-get update && apt-get install -y dumb-init
COPY --from=build /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

# Expose the port that FastAPI will run on
EXPOSE 8000

# Set the environment variable for FastAPI's server (production-ready)
ENV UVICORN_CMD="uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4"

# Command to run FastAPI when the container starts
CMD ["sh", "-c", "$UVICORN_CMD"]