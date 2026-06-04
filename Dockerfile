FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    wget curl gnupg unzip \
    libglib2.0-0 libnss3 libnspr4 \
    libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libdbus-1-3 \
    libxcb1 libxkbcommon0 libx11-6 \
    libxcomposite1 libxdamage1 libxext6 \
    libxfixes3 libxrandr2 libgbm1 \
    libpango-1.0-0 libcairo2 libasound2 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install crawl4ai fastapi uvicorn

RUN crawl4ai-setup

WORKDIR /app

COPY server.py .

EXPOSE 11235

CMD ["python", "server.py"]
