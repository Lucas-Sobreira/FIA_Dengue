from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.amazon.aws.sensors.s3_key import S3KeySensor
from airflow.providers.amazon.aws.operators.s3_copy_object import S3CopyObjectOperator
from airflow.providers.amazon.aws.operators.s3_delete_objects import S3DeleteObjectsOperator
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.S3_hook import S3Hook

import sys
sys.path.insert(0, '/usr/local/airflow/dags/projeto_dengue')
# from projeto_dengue.coleta import coleta_dados, df_dengue, df_municipios, url
from projeto_dengue.saving_raw_old import coleta_dados, df_dengue, df_municipios, url, n_week
# from projeto_dengue.saving_raw_old import save, path


default_args = {
    'owner': 'grupo_fia',
    'depends_on_past': False,
    'start_date': datetime(2022, 8, 15),
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    # dag_id='dengue_update',
    dag_id="DAG_TESTE_DENGUE",
    # schedule_interval='0 7 * * *',
    schedule_interval='0 10 * * 6',
    catchup=False,
    default_args=default_args
)

start = DummyOperator(
    task_id='start',
    dag=dag)

python_task_01 = PythonOperator(
                task_id='coleta_dados', 
                python_callable=coleta_dados, 
                op_kwargs={'df_dengue': df_dengue, 'df_municipios': df_municipios, 'url': url, 'n_week': n_week},
                dag=dag)

# python_task_02 = PythonOperator(
#                 task_id='save_Minio', 
#                 python_callable=save, 
#                 op_kwargs={'path': path},
#                 dag=dag)

def teste_arquivo():
    # Upload generated file to Minio
    s3 = S3Hook('minio_s3')
    s3.load_file("/usr/local/airflow/dags/projeto_dengue/df_dengue.csv",
                    key=f"df_dengue.csv",
                    bucket_name="raw")

salvando = PythonOperator(
                task_id='teste_arquivo', 
                python_callable=teste_arquivo,
                dag=dag)

finish = DummyOperator(
    task_id='finish',
    dag=dag)


# start >> python_task_01 >> python_task_02 >> finish

start >> python_task_01 >> salvando >> finish