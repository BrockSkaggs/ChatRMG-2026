# Persistence Notes

Below is the table definition for a Postgres table to hold application information related to a thread/conversation.
```
CREATE TABLE IF NOT EXISTS public.checkpoint_app_info
(
    thread_id text COLLATE pg_catalog."default" NOT NULL,
    thread_name character varying(255) COLLATE pg_catalog."default",
    user_name character varying(255) COLLATE pg_catalog."default",
    created_on timestamp with time zone,
    positive_feedback boolean,
    negative_feedback_note text COLLATE pg_catalog."default",
    CONSTRAINT checkpoint_app_info_pkey PRIMARY KEY (thread_id)
)
```


Determining location of Postgres configuration file
```
psql -U postgres -c "SHOW config_file;"
```

Example location: **/var/lib/postgresql/18/docker/postgresql.conf**

Edit: timezone='America/Chicago'
