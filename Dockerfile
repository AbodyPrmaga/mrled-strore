ARG PYTHON_VERSION=3.13-slim

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /root/.cache/
COPY . /code

ENV SECRET_KEY "kkeBbzxjf54PuyCzPNgOJMuOKVrlMmzRF0vdb6duRgm5BPcg8v"
RUN python manage.py collectstatic --noinput || true
RUN python manage.py migrate --noinput || true
EXPOSE 8000


CMD ["python","manage.py","runserver","0.0.0.0:8000"]
