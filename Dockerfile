FROM python:3.12-slim-bookworm
RUN mkdir /rag-data
WORKDIR /code
COPY . .
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -U pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y build-essential \
    && apt-get autoremove -y
CMD ["python", "/code/src/app.py"]