import airflow
from airflow.operators.python_operator import PythonOperator
from airflow.models import DAG

import time
from pprint import pprint

args = {
    'owner': 'pycon',
    'start_date': airflow.utils.dates.days_ago(2)
}

dag = DAG(
    dag_id='pycon_python_operator', default_args=args,
    schedule_interval=None)


def print_context(ds, **kwargs):
    pprint("First Airflow task is running with ds: {} and kwargs: {}"
           .format(ds, kwargs))

first_task = PythonOperator(
    task_id='print_context',
    provide_context=True,
    python_callable=print_context,
    dag=dag)
