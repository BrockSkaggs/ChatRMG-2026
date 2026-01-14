# Persistence Notes

Below is the table definition for a Postgres table to hold application information related to a thread/conversation.
```
CREATE TABLE checkpoint_app_info(
	thread_id text primary key,
	thread_name varchar(255),
	user_name varchar(255),
	created_on timestamp
)
```