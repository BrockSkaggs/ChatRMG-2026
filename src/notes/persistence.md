# Persistence Notes

Below is the table definition for a Postgres table to hold application information related to a thread/conversation.
```
CREATE TABLE checkpoint_app_info(
	thread_id text primary key,
	thread_name varchar(255),
	user_name varchar(255),
	created_on timestamp with time zone
)
```


Determining location of Postgres configuration file
```
psql -U postgres -c "SHOW config_file;"
```

Example location: **/var/lib/postgresql/18/docker/postgresql.conf**

Edit: timezone='America/Chicago'
