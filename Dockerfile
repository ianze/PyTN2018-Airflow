FROM centos:7

ARG AIRFLOW_VERSION=1.8.2
ENV AIRFLOW_HOME /usr/local/airflow

COPY scripts/entrypoint.sh /entrypoint.sh
COPY config/airflow.cfg ${AIRFLOW_HOME}/airflow.cfg

# check that certain services have started properly
COPY scripts/check_postgres.py ${AIRFLOW_HOME}/check_postgres.py
COPY scripts/check_postgres.py ${AIRFLOW_HOME}/check_redis.py

# these are needed only to install necessary packages
COPY ./yum_requirements.txt /tmp/yum_requirements.txt

RUN  yum -y update \
    && yum -y install $(cat /tmp/yum_requirements.txt)\
    && yum -y install epel-release \
    && yum -y install python34 \
    && cd /tmp; curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"; /usr/bin/python3.4 get-pip.py \
    && yum -y install -t python-requests \
       python-psycopg2 \
    && useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow \
    && yum -y install python34-devel \
    && pip3 install Cython \
    && pip3 install pytz==2015.7 \
    && pip3 install pyOpenSSL \
    && pip3 install ndg-httpsclient \
    && pip3 install pyasn1 \
    && pip3 install apache-airflow[celery,postgres]==$AIRFLOW_VERSION \
    && pip3 install celery[redis]==3.1.17 \
    && pip3 install nose \
    && pip3 install pytest \
    && yum clean all \
    && rm -rf \
        /var/lib/apt/lists/* \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base \
    && chown -R airflow: ${AIRFLOW_HOME} \
    && mkdir -p /tmp/work/ \
    && chown -R airflow: /tmp/work \
    && chmod 755 /entrypoint.sh \
    && chmod u+w /etc/sudoers \
    && echo "ALL            ALL = (ALL) NOPASSWD: ALL" >> /etc/sudoers

EXPOSE 8080 5555 8793

USER airflow
WORKDIR ${AIRFLOW_HOME}
RUN mkdir /usr/local/airflow/logs
ENTRYPOINT ["/entrypoint.sh"]