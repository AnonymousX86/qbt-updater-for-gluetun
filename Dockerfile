FROM python:3.12-alpine

COPY /app/entrypoint.py .
COPY /app/requirements.txt .

RUN python -m pip install -r requirements.txt

CMD [ "python", "entrypoint.py" ]
