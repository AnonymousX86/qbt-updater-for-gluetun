FROM python:3.12

WORKDIR /qbt-updater

COPY ./requirements.txt /qbt-updater/

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /qbt-updater/app/

CMD [ "python", "/qbt-updater/app/main.py" ]
