"""
basic sql dag
"""
import json
from datetime import datetime

from airflow.decorators import dag
from astro import sql as aql
from airflow.decorators import dag, task


@aql.run_raw_sql(conn_id='david_snowflake')
def run_sql():
    return """select * from REDDIT_AIRFLOW;
    """
@aql.run_raw_sql(conn_id='david_snowflake')
def run_sql_2():
    return """select * from REDDIT_DATA;
    """


@task()
def basic_python():
    """
    #### Extract task
    
    A simple "extract" task to get data ready for the rest of the
    pipeline. In this case, getting data is simulated by reading from a
    hardcoded JSON string.
    """
    data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'

    order_data_dict = json.loads(data_string)
    print(order_data_dict)

    total_order_value = 0

    for value in order_data_dict.values():
            total_order_value += value
            print(total_order_value)


@dag(schedule_interval="@daily", start_date=datetime(2022, 7, 27), catchup=False, tags=[])
def basic_sql():
    run_sql() >> run_sql_2() >> basic_python() >> basic_python()
    # basic_python() >> run_sql()

dag_obj = basic_sql()
