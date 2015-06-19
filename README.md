# SkyKit Display Device Management #

## API ##

### Register Device ###

![Screen Shot 2015-06-19 at 2.33.43 PM.png](https://bitbucket.org/repo/L8AoyM/images/1866246453-Screen%20Shot%202015-06-19%20at%202.33.43%20PM.png)

with the following payload:
{
"macAddress": "c45444596b9b",
"gcm_registration_id": "blah blah",
"tenant_code": "some_tenant"
}

Returns the following uri in **Location** of header:

https://skykit-display-device-int.appspot.com/api/v1/devices/ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyGwsSDkNocm9tZU9zRGV2aWNlGICAgICAgIAKDA


![Screen Shot 2015-06-19 at 2.34.39 PM.png](https://bitbucket.org/repo/L8AoyM/images/255446442-Screen%20Shot%202015-06-19%20at%202.34.39%20PM.png)


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