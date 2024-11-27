FROM python:3.13-slim-bullseye

WORKDIR /app

COPY Pipfile Pipfile.lock /app/

RUN pip install pipenv && \
    pipenv install --system --deploy --ignore-pipfile

COPY . /app

EXPOSE 5000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000"]