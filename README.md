# SkyKit Provisioning API #


Each GET, PUT, POST, DELETE **request header** should have **6C346588BD4C6D722A1165B43C51C** as the *Authorization* key as follows:

![Screen Shot 2015-06-22 at 4.27.10 PM.png](https://bitbucket.org/repo/L8AoyM/images/2887177670-Screen%20Shot%202015-06-22%20at%204.27.10%20PM.png)

## Create Device ##
<hr>

### POST ###

The following is an example of a **request body** JSON that could be posted to the provisioning server to create a device:

{

  "macAddress": "54271e619346",

  "gcmRegistrationId": "8d70a8d78a6dfa6df76dfas7",

  "tenantCode": "foobar"

}

The **response** will be a `422` if failure occurs, but should, if successful:

* Return a `201 Created`; and

* Return the following uri in **location** of the header: 

https://skykit-display-device-int.appspot.com/api/v1/devices/ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyGwsSDkNocm9tZU9zRGV2aWNlGICAgICAgIAKDA

This uri, in turn, in the form of */api/v1/devices/**<device_urlsafe_key>***, can be used via a GET to return the device representation using the following API call:

https://skykit-display-device-int.appspot.com/api/v1/devices/ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyVgsSEVRlbmFudEVudGl0eUdyb3VwIhF0ZW5hbnRFbnRpdHlHcm91cAwLEgZUZW5hbnQYgICAgIDyiAoMCxIOQ2hyb21lT3NEZXZpY2UYgICAgIDDlQoM

where the ***<device_urlsafe_key>*** is: ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyVgsSEVRlbmFudEVudGl0eUdyb3VwIhF0ZW5hbnRFbnRpdHlHcm91cAwLEgZUZW5hbnQYgICAgIDyiAoMCxIOQ2hyb21lT3NEZXZpY2UYgICAgIDDlQoM

## Update Device ##

### PUT ###

The Url would be for a PUT would be something like:
PUT   /api/v1/devices/<device_urlsafe_key>

where the ***<device_urlsafe_key>*** might be something like: ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyVgsSEVRlbmFudEVudGl0eUdyb3VwIhF0ZW5hbnRFbnRpdHlHcm91cAwLEgZUZW5hbnQYgICAgIDyiAoMCxIOQ2hyb21lT3NEZXZpY2UYgICAgIDDlQoM


The following is an example of a **request body** JSON that could be sent to the provisioning server to update a device:

{

  "macAddress": "54271e619346",

  "gcmRegistrationId": "8d70a8d78a6dfa6df76dfas7",

  "tenantCode": "foobar"

}


## Delete Device ##

### DELETE ###

The Url would be for a PUT would be something like:
DELETE   /api/v1/devices/<device_urlsafe_key>

where the ***<device_urlsafe_key>*** might be something like: ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyVgsSEVRlbmFudEVudGl0eUdyb3VwIhF0ZW5hbnRFbnRpdHlHcm91cAwLEgZUZW5hbnQYgICAgIDyiAoMCxIOQ2hyb21lT3NEZXZpY2UYgICAgIDDlQoM


## Get Device ##

### GET ###

The Url would be for a PUT would be something like:
PUT   /api/v1/devices/<device_urlsafe_key>

where the ***<device_urlsafe_key>*** might be something like: ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyVgsSEVRlbmFudEVudGl0eUdyb3VwIhF0ZW5hbnRFbnRpdHlHcm91cAwLEgZUZW5hbnQYgICAgMC1mwoMCxIOQ2hyb21lT3NEZXZpY2UYgICAgJCihwoM

The response JSON will include the following fields:

![Screen Shot 2015-07-07 at 2.12.53 PM.png](https://bitbucket.org/repo/L8AoyM/images/1854249404-Screen%20Shot%202015-07-07%20at%202.12.53%20PM.png)

**key** is our device key.


## Deployment to App Engine ##

From the project root directory: `appcfg.py --oauth2 -A skykit-display-device-int update .`