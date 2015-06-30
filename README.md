# SkyKit Display Device Management #

## API ##

### Register Device ###

Using the following API call:

![Screen Shot 2015-06-19 at 2.33.43 PM.png](https://bitbucket.org/repo/L8AoyM/images/1866246453-Screen%20Shot%202015-06-19%20at%202.33.43%20PM.png)

where the following JSON is posted to the server:

{
  "macAddress": "54271e619346",
 
 "gcmRegistrationId": "8d70a8d78a6dfa6df76dfas7",

  "tenantCode": "foobar"
}

The Request header should have **6C346588BD4C6D722A1165B43C51C** as the *Authorization* key as follows:

![Screen Shot 2015-06-22 at 4.27.10 PM.png](https://bitbucket.org/repo/L8AoyM/images/2887177670-Screen%20Shot%202015-06-22%20at%204.27.10%20PM.png)


will return a `422` if failure occurs, but should, if successful:

* Return a `201 Created`; and

* Return the following uri in **location** of the header: 

https://skykit-display-device-int.appspot.com/api/v1/devices/ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyGwsSDkNocm9tZU9zRGV2aWNlGICAgICAgIAKDA

This uri, in turn, in the form of */api/v1/devices/**<device_id>***, can be used via a GET to return the device representation using the following API call:

![Screen Shot 2015-06-19 at 2.34.39 PM.png](https://bitbucket.org/repo/L8AoyM/images/255446442-Screen%20Shot%202015-06-19%20at%202.34.39%20PM.png)

where the ***<device_id>*** is something like the uuid: ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyGwsSDkNocm9tZU9zRGV2aWNlGICAgICAgIAKDA

## Vagrant ##
1. `vagrant up`
1. `vagrant ssh`
1. `cd /vagrant`
1. `dev_appserver.py .` 

## Tests ##
1. Run all:  `python manage.py pytest tests`
1. Specific: `python manage.py pytest tests/test_tenants_handler.py`


## Deployment to App Engine ##

From the project root directory: `appcfg.py --oauth2 -A skykit-display-device-int update .`