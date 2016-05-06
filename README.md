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

### Initilize DB
Start local mysql server with database name: `provisioning` as root with no password. 

Here's how to do it with Docker: 

Please have docker-machine up and running.

```sh
$ docker run -p 3306:3306 -P --name skykit-commander-mysql -e MYSQL_DATABASE=provisioning -e MYSQL_ALLOW_EMPTY_PASSWORD=yes -d mysql:5.6
```


### Run Back-End
Make sure your virtualenv is activated and has the requirements installed before this step.
```sh
(venv)$ python manage.py serve dispatch.yaml
```

### Bootstrap back-end: 
After starting the server, hit `localhost:8080/api/v1/seed/<user_first>/<user_last>`
You will see a message explaining that the seed script has started in the background,
and a subsequent message expalining when the seed script has finished.

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
$ gulp test
```
