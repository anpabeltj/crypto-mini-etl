import sys
sys.path.insert(0, '/opt/airflow/scripts')

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import extract as e
import transform as t
import load as l

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
}


with DAG('crypto_etl_pipeline', default_args=default_args, schedule='@daily', catchup=False) as dag:
    def run_extract():
        return e.extract_crypto()

    def run_transform(**context):
        data = context['ti'].xcom_pull(task_ids='extract_crypto')
        return t.transform_crypto(data)

    def run_load(**context):
        data = context['ti'].xcom_pull(task_ids='transform_crypto')
        return l.load(data)

    extract_task = PythonOperator(
        task_id='extract_crypto',
        python_callable=run_extract
    )

    transform_task = PythonOperator(
        task_id='transform_crypto',
        python_callable=run_transform
    )

    load_task = PythonOperator(
        task_id='load_crypto',
        python_callable=run_load
    )

    extract_task >> transform_task >> load_task