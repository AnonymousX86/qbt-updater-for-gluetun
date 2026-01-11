FROM python:3.14-slim

WORKDIR /qbt-updater

COPY ./requirements.txt /qbt-updater/

RUN python3 -m pip install --no-cache-dir --upgrade --root-user-action ignore -r requirements.txt

COPY ./app /qbt-updater/app/

CMD [ "python3", "-OO", "-u", "/qbt-updater/app/main.py" ]
