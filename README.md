# SkyKit Provisioning API #


Each GET, PUT, POST, DELETE **request header** should have **6C346588BD4C6D722A1165B43C51C** as the *Authorization* key as follows:

![Screen Shot 2015-06-22 at 4.27.10 PM.png](https://bitbucket.org/repo/L8AoyM/images/2887177670-Screen%20Shot%202015-06-22%20at%204.27.10%20PM.png)

## Create Device ##
___________________________________________________________________________________________________
### POST ###

The following is an example of a **request body** JSON that could be posted to the provisioning server to create a device:

{

  "macAddress": "54271e619346",

  "gcmRegistrationId": "8d70a8d78a6dfa6df76dfas7",

  "tenantCode": "foobar"

}

If successful, the response will:

* Return a `201 Created` status; and

* Return the following uri in **location** of the header: 

https://skykit-display-device-int.appspot.com/api/v1/devices/ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyGwsSDkNocm9tZU9zRGV2aWNlGICAgICAgIAKDA

This uri, in turn, in the form of */api/v1/devices/**<device_urlsafe_key>***, can be used via a GET to return the device representation using the following API call:

https://skykit-display-device-int.appspot.com/api/v1/devices/ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyVgsSEVRlbmFudEVudGl0eUdyb3VwIhF0ZW5hbnRFbnRpdHlHcm91cAwLEgZUZW5hbnQYgICAgIDyiAoMCxIOQ2hyb21lT3NEZXZpY2UYgICAgIDDlQoM

where the ***<device_urlsafe_key>*** is: ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyVgsSEVRlbmFudEVudGl0eUdyb3VwIhF0ZW5hbnRFbnRpdHlHcm91cAwLEgZUZW5hbnQYgICAgIDyiAoMCxIOQ2hyb21lT3NEZXZpY2UYgICAgIDDlQoM

### Return Codes ###
* 403 Forbidden - when api key is not in the request header.
* 400 Bad Request - when device already registered in our NDB datastore.
* 400 Bad Request - when no MAC address in request body
* 400 Bad Request - when no tenant code in request body
* 400 Bad Request - when invalid tenant in request body
* 400 Bad Request - when no GCM registration ID in request body
* 422 Unprocessable Entity - when no device not associated with this customer id
* 201 Create - when device is successfully registered in our NDB datastore



## Update Device ##
___________________________________________________________________________________________________

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

### Return Codes ###
* 404 Not Found - when Unable to retrieve Chrome OS device by the given device id
* 204 No Content - when device is successfully registered in our NDB datastore


## Delete Device ##
___________________________________________________________________________________________________

### DELETE ###

The Url would be for a PUT would be something like:
DELETE   /api/v1/devices/<device_urlsafe_key>

where the ***<device_urlsafe_key>*** might be something like: ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyVgsSEVRlbmFudEVudGl0eUdyb3VwIhF0ZW5hbnRFbnRpdHlHcm91cAwLEgZUZW5hbnQYgICAgIDyiAoMCxIOQ2hyb21lT3NEZXZpY2UYgICAgIDDlQoM


## Get Device ##
___________________________________________________________________________________________________

### GET ###

The Url would be for a PUT would be something like:
GET   /api/v1/devices/<device_urlsafe_key>

where the ***<device_urlsafe_key>*** might be something like: ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyVgsSEVRlbmFudEVudGl0eUdyb3VwIhF0ZW5hbnRFbnRpdHlHcm91cAwLEgZUZW5hbnQYgICAgMC1mwoMCxIOQ2hyb21lT3NEZXZpY2UYgICAgJCihwoM

The response JSON will include the following fields:

![Screen Shot 2015-07-07 at 2.12.53 PM.png](https://bitbucket.org/repo/L8AoyM/images/1854249404-Screen%20Shot%202015-07-07%20at%202.12.53%20PM.png)

**key** is our device key.

### Return Codes ###
* 403 Forbidden - when api key is not in the request header.
* 404 Not Found - when the device is not found in our NDB datastore.
* 400 Bad Request - when no parent tenant exists for the requested device in our NDB datastore.
* 422 Unprocessable Entity - when an error occurs posting to the GCM. 




## Get Device by MAC Address ##
___________________________________________________________________________________________________

### GET ###

The Url would be for a PUT would be something like:
GET   /api/v1/devices?macAddress=<MAC address>

where the ***<MAC address>*** might be something like: 54271e6950ed

The response JSON will include a full device representation:

![Screen Shot 2015-07-09 at 1.38.44 PM.png](https://bitbucket.org/repo/L8AoyM/images/2900401397-Screen%20Shot%202015-07-09%20at%201.38.44%20PM.png)

**key** is our device key.

### Return Codes ###
* 403 Forbidden - when api key is not in the request header.
* 404 Not Found - when unable to retrieve device from Google API or from our NDB datastore.



## Device Change Intent ##
___________________________________________________________________________________________________

### POST ###

The Url would be for a PUT would be something like:
PUT   /api/v1/devices/<device_urlsafe_key>/commands

where the ***<device_urlsafe_key>*** might be something like: ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyVgsSEVRlbmFudEVudGl0eUdyb3VwIhF0ZW5hbnRFbnRpdHlHcm91cAwLEgZUZW5hbnQYgICAgMC1mwoMCxIOQ2hyb21lT3NEZXZpY2UYgICAgJCihwoM


The request body includes the *intent* as follows:

{

  "intent": "http://skykit.com/skdchromeapp/reset"

}

### Return Codes ###
* 403 Forbidden - when api key is not in the request header.
* 404 Not Found - when the device is not found in our NDB datastore.
* 422 Unprocessable Entity - when an error occurs posting to the GCM. 




___________________________________________________________________________________________________
___________________________________________________________________________________________________

## Deployment to App Engine INT Environment ##

From the project root directory: `appcfg.py --oauth2 -A skykit-display-device-int update .`

snapdeploy: `python manage.py snapdeploy --ignore-branch -A skykit-display-device-int --oauth2`

[SkyKit Provisioning INT](https://skykit-display-device-int.appspot.com/#)

## Deployment to App Engine PROD Environment ##

From the project root directory: `appcfg.py --oauth2 -A skykit-provisioning update .`

snapdeploy: `python manage.py snapdeploy --ignore-branch -A skykit-provisioning --oauth2`

[SkyKit Provisioning](https://skykit-provisioning.appspot.com/#)

### GOTCHAS ###

Snapdeploy tags with a hash. You have to explicitly choose that hash under migrations module, otherwise you're using old code and any new migrations won't show up because you're probably still using the old tag.
 
![Screen Shot 2015-08-13 at 12.11.02 PM.png](https://bitbucket.org/repo/L8AoyM/images/288299165-Screen%20Shot%202015-08-13%20at%2012.11.02%20PM.png)