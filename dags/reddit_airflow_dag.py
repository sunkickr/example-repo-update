"""
Advanced_Pipeline
DAG file auto-generated by AstroBuild.
"""
import time
from datetime import datetime

import pandas as pd
import praw
from airflow.decorators import dag, task
from airflow.models import Variable
from airflow.utils import timezone
from airflow.utils.dates import days_ago
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table

reddit = praw.Reddit(
    client_id="x-dpX0AWNAdQNxi_iYuZZQ",
    client_secret="CduG38KSUf-oyA_wlO_RLOrujRZUtQ",
    user_agent="Learn About AIrflow",
)

subreddits = [
    'dataengineering',
    'data',
    'datascience',
    'learnpython',
    'ETL', 
    'dataengineeringjobs',
    'BigDataJobs',
    'BigDataETL',
    'dataanalysis',
    'DataScienceJobs', 
    'MachineLearning'
]

@aql.dataframe()
def find_airflow_posts_func():
    keyword = "airflow"
    posts = []

    for sub in subreddits:
        for post in reddit.subreddit(sub).new(limit=100):
            if keyword in post.title.lower() or keyword in post.selftext.lower():
                posts.append([post.title, post.score, post.id, post.url, post.num_comments, post.selftext, post.created, post.subreddit.display_name])

    posts = pd.DataFrame(posts, columns=['title', 'score', 'id', 'url', 'num_comments', 'body', 'created', 'subreddit',])

    return posts

@aql.run_raw_sql(conn_id='david_snowflake')
def insert_into_snowflake_func(find_airflow_posts: Table):
    return """insert into REDDIT_AIRFLOW
    select * from {{find_airflow_posts}};
    """

@aql.run_raw_sql(conn_id='david_snowflake')
def delete_duplicate_posts_func():
    return """BEGIN
        create or replace transient table duplicate_holder as (
            SELECT 
                title,
                score,
                id,
                url,
                num_comments,
                body,
                created,
                subreddit,
                ROW_NUMBER() OVER (
                    PARTITION BY 
                        title, 
                        id
                    ORDER BY 
                        num_comments desc
                ) as row_num
            FROM 
                REDDIT_AIRFLOW
        );

        delete from duplicate_holder where row_num > 1;

        alter table duplicate_holder
        drop column row_num;

        -- time to use a transaction to insert and delete
        begin transaction;

        -- insert single copy
        alter table REDDIT_AIRFLOW SWAP WITH duplicate_holder;

        -- we are done
        commit;

        drop table duplicate_holder;
    END;
    """

@dag(schedule_interval="@daily", start_date=datetime(2022, 7, 27), catchup=False, tags=[])
def Advanced_Pipeline():
    find_airflow_posts = find_airflow_posts_func()
    insert_into_snowflake_func(find_airflow_posts) >> delete_duplicate_posts_func()

dag_obj = Advanced_Pipeline()