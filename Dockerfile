FROM python:3.12

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Expose port for FastAPI
EXPOSE 7860

# Run API server (NOT inference)
CMD ["uvicorn", "app.api:app", "--host", "0.0.0.0", "--port", "7860"]

