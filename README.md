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


### Run Back-End
Make sure your virtualenv is activated and has the requirements installed before this step.
```sh
(venv)$ python manage.py serve dispatch.yaml
```

### Bootstrap back-end: 
After starting the server, hit `localhost:8080/api/v1/seed`
You will see a message explaining that the seed script has started in the background,
and a subsequent message expalining when the seed script has finished.

<b>NOTE</b>: you will need to edit the username associated with the seed script to match your agosto domain.
Edit the following: `handlers.dev_handlers.USER_EMAIL`

### Test Back-End
After following the directions found <a href="https://sites.google.com/a/dev.agosto.com/skykit/tenant-provisioning/testing">here</a>
```sh
$ ./manage.py pytest --cov-report=term --cov-report=html --cov=. tests/
```
### Run Front-End

```sh
$ npm install
$ gulp serve
```

### Test Front-End

```sh
$ gulp test
```

To update coverage
```sh
$ gulp build
```

### Setup Local MySQL instance (only needed if you will be doing proof of play related testing)

```sh
$ brew install mysql
$ mysql.server start
$ CREATE DATABASE provisioning;
```
