from langgraph.checkpoint.postgres import PostgresSaver #Package required: https://pypi.org/project/langgraph-checkpoint-postgres/ -> pip install "psycopg[binary]"
import psycopg
from psycopg.rows import dict_row
from typing import Optional

from common import gen_postgres_conn_str, dashgpt_engine

def run_db_setup():
    with PostgresSaver.from_conn_string(gen_postgres_conn_str()) as checkpointer:
        # Uncomment the line below to setup the database schema - Creates tables: checkpoint_blobs, checkpoint_migrations, checkpoint_writes, and checkpoints
        # checkpointer.setup()
        print('Database setup complete.')

def gen_checkpointer(use_sqlalchemy_engine: Optional[bool] = True):
    conn = None
    if use_sqlalchemy_engine:
        conn = dashgpt_engine.connect()
    else:
        conn = psycopg.connect(gen_postgres_conn_str(False), autocommit=True, row_factory=dict_row)    
    return PostgresSaver(conn)