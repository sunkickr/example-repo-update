FROM quay.io/astronomer/astro-runtime-dev:6.1.0-alpha3

# env DAG_DIR=baz
# ENV DAG_ID=foo
# ENV EXECUTION_DATE=bar
# RUN airflow db init
# COPY run_local_dag.py .
# CMD python ./run_local_dag.py --dag_dir $DAG_DIR --dag_id $DAG_ID
# # CMD airflow dags test -S $DAG_DIR $DAG_ID $EXECUTION_DATE

# FROM docker.io/dimberman/local-airflow-test:0.0.2
# COPY requirements.txt .
# RUN  pip install --no-cache-dir -r requirements.txt