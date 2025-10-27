# Use official Python image
FROM python:3.12-slim

# Install dependencies for Chromium
RUN apt-get update && apt-get install -y \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libxi6 \
    libxss1 \
    libx11-xcb1 \
    libxtst6 \
    libatk1.0-0 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    xdg-utils \
    wget \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Set environment variable for Chromium path (needed for Selenium)
ENV CHROME_PATH=/usr/bin/chromium

# Set working directory
WORKDIR /app

# Copy your project
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Command to run tests
CMD ["pytest",  "-vv", "--html=report.html"]
