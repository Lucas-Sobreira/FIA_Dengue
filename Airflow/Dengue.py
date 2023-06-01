from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.amazon.aws.sensors.s3_key import S3KeySensor
from airflow.providers.amazon.aws.operators.s3_copy_object import S3CopyObjectOperator
from airflow.providers.amazon.aws.operators.s3_delete_objects import S3DeleteObjectsOperator
from airflow.operators.python_operator import PythonOperator

import sys
sys.path.insert(0, '/usr/local/airflow/dags/projeto_dengue')
from projeto_dengue.coleta import coleta_dados, df_dengue, df_municipios, url

default_args = {
    'owner': 'grupo_fia',
    'depends_on_past': False,
    'start_date': datetime(2022, 8, 15),
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    dag_id='dengue_att',
    schedule_interval='0 7 * * *',
    catchup=False,
    default_args=default_args
)

start = DummyOperator(
    task_id='start',
    dag=dag)

python_task = PythonOperator(
                task_id='codigo_python', 
                python_callable=coleta_dados, 
                op_kwargs={'df_dengue': df_dengue, 'df_municipios': df_municipios, 'url': url},
                dag=dag)

finish = DummyOperator(
    task_id='finish',
    dag=dag)


start >> python_task >> finish