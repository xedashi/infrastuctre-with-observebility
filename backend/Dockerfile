FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.11-slim
RUN addgroup --system appgroup && adduser --system --group appuser

WORKDIR /app 

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY . .
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
