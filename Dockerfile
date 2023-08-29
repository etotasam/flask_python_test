FROM python:3.9-alpine

WORKDIR /flask

#! Install dependencies for Chrome and ChromeDriver
RUN apk update && apk add --no-cache \
    # chromium \
    # chromium-chromedriver \
    && rm -rf /var/cache/apk/*

#! Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#! Copy application code
COPY . .