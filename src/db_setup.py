from langgraph.checkpoint.postgres import PostgresSaver #Package required: https://pypi.org/project/langgraph-checkpoint-postgres/ -> pip install "psycopg[binary]"
from common import gen_postgres_conn_str

print('Setting up database...')
with PostgresSaver.from_conn_string(gen_postgres_conn_str(False)) as checkpointer:
    # Uncomment the line below to setup the database schema - Creates tables: checkpoint_blobs, checkpoint_migrations, checkpoint_writes, and checkpoints
    # checkpointer.setup()
    ...
print("DONE")