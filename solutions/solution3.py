from datetime import timedelta
import time
import zipfile
import os

import requests

import airflow
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG

from pytn_utils import RandomFailOpen

args = {
    'owner': 'pytn',
    'start_date': airflow.utils.dates.days_ago(2),
    'retries': 6,
    'retry_delay': timedelta(seconds=5),
}

dag = DAG(
    dag_id='solution3', default_args=args,
    schedule_interval=None)

# executables
def download_names():
    location = "https://www.ssa.gov/oact/babynames/state/namesbystate.zip"

    local_filename = "/tmp/work/namesbystate.zip"

    print("Starting download...")
    r = requests.get(location, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    print("Finished downloading names!")
    return local_filename


def unzip_names():
    input_file = "/tmp/work/namesbystate.zip"
    names_directory = "/tmp/work/"

    print("Unzipping input...")
    zip_ref = zipfile.ZipFile(input_file, 'r')
    zip_ref.extractall(names_directory)
    zip_ref.close()
    print("Finished!")


def find_common_for_state(ds, **kwargs):
    names_directory = "/tmp/work"
    state = kwargs['ti'].task_id.lstrip('find_common_')

    files = os.listdir(names_directory)
    names = {}

    print("Starting to find common for state {}...".format(state))
    with RandomFailOpen(os.path.join(names_directory, "{}.TXT".format(state))) as f:
        for row in f:
            _, gender, year, name, count = row.split(",")
            if name in names:
                names[name] += int(count)
            else:
                names[name] = int(count)

    common_name = sorted(names, key=names.get, reverse=True)[0]
    print("Common name is {}".format(common_name))

    return common_name


# tasks
download_task = PythonOperator(
    task_id='download',
    python_callable=download_names,
    dag=dag)


unzip_task = PythonOperator(
    task_id='unzip',
    python_callable=unzip_names,
    dag=dag)

states = ['OH', 'OK', 'MI', 'TN', 'TX', 'VT']

for state in states:
    PythonOperator(
        task_id='find_common_{}'.format(state),
        python_callable=find_common_for_state,
        provide_context=True,
        dag=dag).set_upstream(unzip_task)


# dependencies
unzip_task.set_upstream(download_task)