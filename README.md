## Local Setup
- Create postgres database
    - Login into postgres root user `sudo -u postgres -i`
    - Enter postgres cli `psql`
    - Create database command `create database <database_name>`
    - Exit postgres cli `\q`

- Create local user 
    - `sudo -u postgres createuser <username> `

- Start local database
    - `sudo service postgresql start`
    or
    - `sudo pg_ctlcluster 13 main start`

- Check local databases
    - `psql -l`

- Start a gunicorn server
    - `gunicorn wsgi:app`

- Run bash command on deployed node
    - `heroku run <bash command> -a sheriff-sale`

- Run heroku deployment locally
    - `heroku local web -f Procfile.windows`


## Custom Commands
- Create Database Tables
    - `flask cli create_tables`

- Drop Database Tables
    - `flask cli drop_tables`

- Create a database migration
    - `flask db migrate -m "<message>"`

- Upgrade database for migration
    - `flask db upgrade`