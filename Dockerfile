FROM python:3.12.3-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl ca-certificates && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    mv /root/.local/bin/uv /usr/local/bin/uv && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project configuration and requirements first
COPY pyproject.toml requirements.in ./

# Copy the source code
COPY src/ ./src/

# Install the package and its dependencies
RUN uv pip install --system --index-url https://pypi.org/simple .

# Copy the rest of the files
COPY . .

# Expose port for FastAPI
EXPOSE 8000

# COMMAND: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
CMD ["uvicorn", "cims.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]