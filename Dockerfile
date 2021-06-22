FROM wnameless/oracle-xe-11g-r2


RUN set -ex \
    && apt-get update -y -qq \
    && apt-get upgrade -y -qq \
	&& apt-get install -y python3 python3-pip git

RUN set -ex \
    git clone https://github.com/unsuitable001/VulnSequel.git \
    cd VulnSequel \
    pip3 install -r requirements.txt

RUN mkdir /devrepo

VOLUME /devrepo

ENV LD_LIBRARY_PATH=$ORACLE_HOME/lib:LD_LIBRARY_PATH

CMD bash -C "setup.sh"

EXPOSE 5000
