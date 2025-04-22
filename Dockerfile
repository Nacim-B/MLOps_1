FROM python:3.12-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Copy pyproject and install deps
COPY pyproject.toml /app/
RUN poetry install --no-root --no-interaction --no-ansi


COPY src/ /app/src/

ENV PYTHONPATH=/app/src

WORKDIR /app/src/mlops_project

CMD ["python3", "train_pipeline.py"]