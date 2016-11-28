# SkyKit Provisioning API #
___________________________________________________________________________________________________

## Deployment to App Engine INT Environment ##

snapdeploy: `python manage.py snapdeploy --ignore-branch -A skykit-display-device-int --oauth2`

[SkyKit Provisioning INT](https://skykit-display-device-int.appspot.com/#)

## Deployment to App Engine PROD Environment ##

snapdeploy: `python manage.py snapdeploy --ignore-branch -A skykit-provisioning --oauth2`

[SkyKit Provisioning](https://skykit-provisioning.appspot.com/#)

### Setup requirements

```sh
$ virtualenv -p python venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

### Initilize SQL DB
Start local mysql server with database name: `provisioning` as root with no password. 

Here's how to do it with Docker: 

[Docker for Mac](https://docs.docker.com/docker-for-mac/) is the recommened tool to use to setup Docker on Mac. 

After installation, make sure docker for mac is running by examining your toolbar for a whale icon.

After, open up a terminal and run `docker ps`. You should see a table with the list of running containers (this will be 0 intitially).
 
To create a container with a mysql instance, run:

```sh
$ docker run -p 3306:3306 -P --name skykit-provisioning-mysql -e MYSQL_DATABASE=provisioning -e MYSQL_ALLOW_EMPTY_PASSWORD=yes -d mysql:5.6
```


<b>Make sure to pip install `mysql-python` if you do not already have it</b>
Then, start up the backend:
```sh
(venv)$ python manage.py serve dispatch.yaml
```

Finally, run a migration to setup tables/schema via hitting `localhost:8080/proofplay/api/v1/seed/<number_of_days_back_to_post>/<number_of_times_a_day>`

### Run Back-End
Make sure your virtualenv is activated and has the requirements installed before this step.
```sh
(venv)$ python manage.py serve dispatch.yaml
```

### Bootstrap back-end: 
First, clear datastore: `dev_appserver.py . --clear_datastore=yes`.
After starting the server with `python manage.py serve dispatch.yaml`, hit `localhost:8080/internal/v1/seed/<user_first>/<user_last>`. (e.g. `localhost:8080/internal/v1/seed/daniel/ternyak`
This should correspond to your agosto email address. 
You will see a message explaining that the seed script has started in the background,
and a subsequent message explaining when the seed script has finished.

### Bootstrap Proof of Play back-end: 
After starting the server, hit `localhost:8080/proofplay/api/v1/seed/<number_of_days_back_to_post>/<number_of_times_a_day>`
You will see a message explaining that the seed script has started in the background.
A message will print to the terminal after all tasks have completed. 

### Test Back-End
After following the directions found <a href="https://sites.google.com/a/dev.agosto.com/skykit/tenant-provisioning/testing">here</a>
```sh
$ ./manage.py pytest --cov-report=term --cov-report=html --cov=. tests/
```

### Run Front-End
```sh
$ npm install
$ bower install
$ gulp serve
```

### Test Front-End
```sh
$ karma start
OR 
$ karma start --file services
OR 
$ karma start --file services/some-service.js
OR 
$ npm run test
```
