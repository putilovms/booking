FROM python:3.10

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install uv

COPY . .

RUN chmod a+x /app/docker/*.sh

# CMD ["uv", "run", "gunicorn", "app.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]
