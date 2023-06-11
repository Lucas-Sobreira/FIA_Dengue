from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.amazon.aws.sensors.s3_key import S3KeySensor
from airflow.providers.amazon.aws.operators.s3_copy_object import S3CopyObjectOperator
from airflow.providers.amazon.aws.operators.s3_delete_objects import S3DeleteObjectsOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.S3_hook import S3Hook

default_args = {
    'owner': 'grupo_fia',
    'depends_on_past': False,
    'start_date': datetime(2022, 8, 15),
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    # dag_id='dengue_update',
    dag_id="teste_dag_01",
    schedule_interval='0 7 * * *',
    catchup=False,
    default_args=default_args
)

start = DummyOperator(
    task_id='start',
    dag=dag)

def teste_arquivo():
    # Upload generated file to Minio
    s3 = S3Hook('minio_s3')
    s3.load_file("/usr/local/airflow/dags/projeto_dengue/teste.txt",
                    key=f"teste_01.txt",
                    bucket_name="raw")

teste = PythonOperator(
                task_id='teste_arquivo', 
                python_callable=teste_arquivo,
                dag=dag)

finish = DummyOperator(
    task_id='finish',
    dag=dag)


# start >> python_task_01 >> python_task_02 >> finish

start >> teste >> finish