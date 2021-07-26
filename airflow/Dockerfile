FROM python:3.7-slim-buster

RUN apt-get update -yqq \
    	&& apt-get upgrade -yqq \
    	&& apt-get install -yqq --no-install-recommends \
	apt-utils \
	build-essential \
	libffi-dev \
	libpq-dev \
	libssl-dev \
	python3-pandas \
	python3-numpy

ENV PYTHONPATH="${PYTHONPATH}:/usr/lib/python3/dist-packages"

RUN pip install -U pip setuptools wheel \
	&& pip install pyOpenSSL \
    	&& pip install apache-airflow[crypto,aws,slack,postgres]

COPY ./requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8080

COPY ./entrypoint.sh /entrypoint.sh
ENTRYPOINT [ "/entrypoint.sh" ]
