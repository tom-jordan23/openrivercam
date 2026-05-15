FROM python:3.12-slim

RUN useradd --create-home --shell /bin/bash --uid 1001 app
WORKDIR /app

RUN pip install --no-cache-dir 'psycopg2-binary==2.9.*'

COPY app.py /app/app.py
RUN chown -R app:app /app

USER app

CMD ["python3", "-u", "/app/app.py"]
