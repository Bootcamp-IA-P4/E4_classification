ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY . .

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"]