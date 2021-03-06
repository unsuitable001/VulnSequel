FROM wnameless/oracle-xe-11g-r2

RUN mkdir /devrepo

VOLUME /devrepo

COPY . /devrepo

WORKDIR /devrepo

RUN set -ex \
    && DEBIAN_FRONTEND=noninteractive \
    apt-get update -y -qq \
    && apt-get upgrade -y -qq \
	&& apt-get install -y -qq python3 python3-pip

RUN set -ex \
    pip3 install -r requirements.txt

EXPOSE 5000
