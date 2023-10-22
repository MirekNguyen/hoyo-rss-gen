FROM python:3.9.18-slim

# Install the necessary locales
RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
  && localedef -i cs_CZ -f UTF-8 cs_CZ.UTF-8

WORKDIR /usr/src/app

COPY docker/requirements.txt .
COPY . /usr/src/app

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "main.py"]
CMD []
