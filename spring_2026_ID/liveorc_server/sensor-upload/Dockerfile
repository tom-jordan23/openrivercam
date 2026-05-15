FROM python:3.12-slim

RUN useradd --create-home --shell /bin/bash --uid 1001 app
WORKDIR /app

RUN pip install --no-cache-dir 'fastapi==0.115.*' 'uvicorn[standard]==0.32.*'

COPY app.py /app/app.py
RUN chown -R app:app /app

USER app
EXPOSE 8001

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8001", "--log-level", "info"]
