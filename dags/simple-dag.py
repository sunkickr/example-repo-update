from datetime import datetime
from airflow.decorators import dag
from airflow.providers.amazon.aws.operators.s3 import S3ListOperator

@dag(start_date=datetime(2021, 12, 1), schedule_interval='@daily', catchup=False)
def simple_dag():

    list_bucket = S3ListOperator(
        task_id="list_bucket",
        bucket='mikeshwe-awsbucket',
        aws_conn_id="aws_default",
        delimiter='/',
    )
simple_dag = simple_dag()