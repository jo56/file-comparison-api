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

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY src src
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["uvicorn main:app --reload"]
