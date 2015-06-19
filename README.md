# SkyKit Display Device Management #

## API ##

### Register Device ###


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