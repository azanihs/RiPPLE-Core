# RiPLE Server
The server component of the RiPPLE

# Getting Started

## Setting Up
After installing the Prerequisites for your system, all you will need to do is run
```bash
pip install -r requirements.txt
```

If you are using the Anaconda python distribution, the you will instead need to do:
```bash
pip install Django==1.11.4
pip install Faker==0.7.18
conda install -c anaconda mysql-connector-python
conda install -c anaconda MySQL-python
```

## Setting up the Application
Django uses [migrations](https://docs.djangoproject.com/en/1.11/topics/migrations/) in order to manage the databsae schema. For the application to work correctly, you need to ensure that the database is up to date.

### Configurating the Database connection
The database connection details are defined in `./src/ripple/settings.py` under the `DATABASE` dictionary key. Django documents the value of this key [here](https://docs.djangoproject.com/en/1.11/ref/settings/#databases). You should only need to change the `USER` and `PASSWORD` fields to match your local database credentials.

### Applying Migrations
A current limitation of the project is that the required database is not made automatically (unless using SQLite3). As such, you will need to manually create the database in your DBMS. Assuming a database name of 'ripple', mysql achieves this with:
```bash
mysql -uroot -p
CREATE DATABASE ripple;
exit;
```

### Seeding the Database
A seeder is packaged with this application to populate the database with mock data. When run, it *will not* clear the database - only add to it. It therefore may sometimes be neccesary to manually empty the database.
The seeder can be invoked with:
```bash
python manage.py seed
```

### Running the Application
Once the database connectivity is working and the migrations are applied, you can start the server with
```bash
python manage.py runserver
```

If this works, you should also create a superuser for use with your administration panel `localhost:8000/admin`.
This is achieved with `python manage.py createsuperuser`


### Automated Deployment
The automated deployment script works by simply stopping the local ripple service, subbing in the new source and then restarting the service.
It requires the following environment variables to be set:

* SERVICE_NAME: The name of the local service (eg. ripple)
* DEPLOY_PATH: The path to deploy the application to (eg. /var/www/cgi/ripple)
* SOURCE_DIR: The source location of the application (eg. ~/RiPPLE-Server-Side)
* APP_OWNER: The owner to chmod the DEPLOY_PATH to eg (user:group)

`sudo deploy.sh .production.env`, where .production.env is the configuration file to use with ripple
