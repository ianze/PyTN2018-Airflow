Intro
=====
Airflow in dockerized version to be used during PyTN 2018 tutorial.

Inspired by https://github.com/puckel/docker-airflow/

Prerequisites
=============

Install Docker: https://docs.docker.com/install/

Install docker-compose: https://docs.docker.com/compose/install/

There are 3 ports that will be exposed by the service: 8080 5555 8793
Please ensure those ports are not used on your system before following the instruction.

Instructions:
=============

1. Clone the repo.

2. Run:

```
docker-compose up
```
You can optionally add `-d` flag if you prefer it to run in the background.

3.Verify you can access Airflow UI at: http://localhost:8080

Alternative Installation:
=========================

In case of WiFi issues at the venue or just slow installation.

We will have several USB drives in the class.

1. Copy the .tar files from USB drive. 

2. For each file run:

```
docker load --input <file-name>
```

3. Navigate back to the repo directory. Follow steps 2 and 3 from above. 

Tutorial:
=========

The dags directory is where you will put the DAGS you will create. It is mapped into /usr/local/airflow/dags in the containers.

Put files your DAGS create locally in the container in /tmp/work

Consult the solutions directory or DAG examples if you need to.
