
FROM python:3.12-slim

WORKDIR /app

ENV HOME=/app

COPY requirements.txt .

RUN apt-get update && apt-get install -y build-essential libpq-dev && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


RUN addgroup --system agrigrp && adduser --system --ingroup agrigrp cocaagri 
    
COPY . .

RUN chown -R cocaagri:agrigrp /app

USER cocaagri

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.baseUrlPath=agri-census"]