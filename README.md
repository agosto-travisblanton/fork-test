# SkyKit Provisioning API #
___________________________________________________________________________________________________

## Deployment to App Engine INT Environment ##

snapdeploy: `python manage.py snapdeploy --ignore-branch -A skykit-display-device-int --oauth2`

[SkyKit Provisioning INT](https://skykit-display-device-int.appspot.com/#)

## Deployment to App Engine PROD Environment ##

snapdeploy: `python manage.py snapdeploy --ignore-branch -A skykit-provisioning --oauth2`

[SkyKit Provisioning](https://skykit-provisioning.appspot.com/#)

### Setup CloudSQL

```sh
$ brew install mysql
$ mysql.server start
$ CREATE DATABASE provisioning;
```

### Setup requirements

```sh
$ virtualenv -p python venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

Ensure that the requirements are NOT installed to /lib/usr,
as having MySQLdb in lib/usr/ will break the deployment.


### Run Back-End

```sh
$ python manage.py serve dispatch.yaml
```

### Test Back-End

```sh
$ python manage.py test
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