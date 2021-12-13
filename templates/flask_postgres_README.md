### Three Parts
    - Configure Postgres Credentials and Server
    - Set up Local .env file
    - Run the flask app

### Configure Postgres Credentials and Server
1. Enter the CLI and start the Postgres server:  
`sudo service postgresql start`
2. Create a new database: `createdb {name}` 
3. Access the Postgres console of that database: `psql {name}`
4. Create a user: `CREATE USER {user};`
5. Configure a password for the user: `\password {user}`
Remember the password you set
6. Create an `items` table for our database by copying and pasting the following schema: 

# This is based off the example Model for `Item` created in flask_postgres.py. Adjust the example accordingly to your specifice Model

        CREATE TABLE items( 
            sourceid serial PRIMARY KEY,
            name VARCHAR (355),
            information VARCHAR (355),
           );
7. Grant proper permissions for your user to send data into the table:  `GRANT ALL PRIVILEGES ON TABLE items TO {user};`

### Set up local .env file
1. Exit the Postgres console and create a .env file: `touch .env`
2. Edit the file to include the following:  

        POSTGRES_DB_USER="{user}"  
      
        POSTGRES_DB_PASSWORD="{password}"  
        
        POSTGRES_DB_NAME="{name}"

    Notice that we are using the database name, user, and password we created earlier to act as our environmental variables.
    This file will only be local on your machine as the .gitignore prevents it from being pushed up to the cloud.

### Run the flask app
Run the app: `python app.py`

You should now have the final REST API ready to view after following these steps. Once you are finished, don't forget to stop the postgres server with `sudo service postgresql stop`.

Below is a list of useful commands worth knowing:


## For Postgres in CLI

#### You can delete a database or kill process using the following commands.

List Current Processes: `ps -ef`

Kill Process: `sudo kill {PID}`

Delete a database: `dropdb {name}`

Exit current process: `exit`

## For Postgres Console

List tables: `\dt`

List users: `\du`

List databases: `\l`

Query Items Table: `select * from items;`

Delete a user:	`DROP ROLE {user};`
