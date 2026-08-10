FROM python:3.12-slim

RUN useradd --create-home --shell /bin/bash --uid 1001 app
WORKDIR /app

RUN pip install --no-cache-dir 'psycopg2-binary==2.9.*' \
                               'google-api-python-client==2.198.*' \
                               'google-auth==2.56.*'

COPY app.py /app/app.py
RUN chown -R app:app /app

# Unlike sensor-upload and grafana, this service reads no 0600 privkey, so it
# drops to a non-root user. Consequence: secrets/sheets-sa.json on the host
# must be readable by uid 1001 (chown 1001:1001, chmod 0400).
USER app

CMD ["python3", "-u", "/app/app.py"]
