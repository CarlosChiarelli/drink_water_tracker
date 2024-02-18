# Use a Python base image
FROM python:3.11.8-slim

# Install Poetry
RUN pip install poetry==1.7.1

# Environment variables
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set the working directory
WORKDIR /app

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry
RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR
# Run in PRODUCTION
# RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# Copy remaining application files
COPY . .

# Install in virtual environment
RUN poetry install 
# Run in PRODUCTION
# RUN poetry install --without dev

# Define the port the FastAPI application will expose
# EXPOSE 8000

# Command to start the application
# CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]