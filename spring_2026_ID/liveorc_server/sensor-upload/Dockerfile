FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir 'fastapi==0.115.*' 'uvicorn[standard]==0.32.*'

COPY app.py /app/app.py

# Runs as root so uvicorn can read /certs/privkey.pem (mode 0600). Container
# surface is narrow: FastAPI app with no shell access, all file writes
# confined to UPLOAD_ROOT, no exec or subprocess calls.
EXPOSE 8443

CMD ["uvicorn", "app:app", \
     "--host", "0.0.0.0", \
     "--port", "8443", \
     "--ssl-keyfile",  "/certs/privkey.pem", \
     "--ssl-certfile", "/certs/fullchain.pem", \
     "--log-level", "info"]
