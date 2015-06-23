FORMAT: 1A
HOST: https://skykit-display-device-int.appspot.com

# Skykit Device Management API

## Group Devices

### GET /api/v1/devices
Retrieve all devices from Skykit Device Management

+ Request (application/json)

    + Headers

            Accept: application/json
            Authorization: 6C346588BD4C6D722A1165B43C51C



+ Response 200 (application/json)

    + Headers


    + Body

            [
				{
					"status": "ACTIVE", 
					"lastSync": "2015-06-22T18:31:42.678Z", 
					"kind": "admin#directory#chromeosdevice", 
					"ethernetMacAddress": "3863bb98f675", 
					"macAddress": "38b1db95806d", 
					"orgUnitPath": "/Agosto/Beta/Fairchild Semi", 
					"serialNumber": "5CD45183S6", 
					"annotatedUser": "fairchild@skykit.com", 
					"bootMode": "Verified", 
					"etag": "\"MO4FtId2-yiZq_-3TpU3AZTf2Ak/q2J1QVycAwick78q5218-w2DMgw\"", 
					"deviceId": "e80a9161-4367-4189-be90-450e5e29501b", 
					"lastEnrollmentTime": "2015-05-07T21:15:17.285Z", 
					"platformVersion": "6812.88.0 (Official Build) stable-channel zako", 
					"model": "HP Chromebox CB1-(000-099) / HP Chromebox G1", 
					"osVersion": "42.0.2311.153", 
					"firmwareVersion": ""
				},
				... 
			]

+ Response 403 (application/json)

    + Headers


    + Body

            {
                "error": "HTTP request API token is invalid."
            }

### GET /api/v1/devices?macAddress={mac_address}
Retrieve a specific Skykit device/display by MAC address.

+ Parameters

    + mac_address: `38b1db95806d` (required, string) - The device's MAC address for wireless or Ethernet networking.

+ Request (application/json)

    + Headers

            Accept: application/json
            Authorization: 6C346588BD4C6D722A1165B43C51C



+ Response 200 (application/json)

    + Headers

            Alternate-Protocol: 443:quic,p=1
            Cache-Control: no-cache

    + Body

            {
				"status": "ACTIVE", 
				"lastSync": "2015-06-22T18:31:42.678Z", 
				"kind": "admin#directory#chromeosdevice", 
				"ethernetMacAddress": "3863bb98f675", 
				"macAddress": "38b1db95806d", 
				"orgUnitPath": "/Agosto/Beta/Fairchild Semi", 
				"serialNumber": "5CD45183S6", 
				"annotatedUser": "fairchild@skykit.com", 
				"bootMode": "Verified", 
				"etag": "\"MO4FtId2-yiZq_-3TpU3AZTf2Ak/q2J1QVycAwick78q5218-w2DMgw\"", 
				"deviceId": "e80a9161-4367-4189-be90-450e5e29501b", 
				"lastEnrollmentTime": "2015-05-07T21:15:17.285Z", 
				"platformVersion": "6812.88.0 (Official Build) stable-channel zako", 
				"model": "HP Chromebox CB1-(000-099) / HP Chromebox G1", 
				"osVersion": "42.0.2311.153", 
				"firmwareVersion": ""
			}


+ Response 403 (application/json)

    + Headers


    + Body

            {
                "error": "HTTP request API token is invalid."
            }


### GET /api/v1/devices/{urlsafe_key}

+ Parameters

    + urlsafe_key: `ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyGwsSDkNocm9tZU9zRGV2aWNlGICAgID4woQKDA` (required, string) - The device's entity key.

+ Request (application/json)

    + Headers

            Accept: application/json
            Authorization: 6C346588BD4C6D722A1165B43C51C



+ Response 200 (application/json)

    + Headers


    + Body

            {
				"status": "ACTIVE", 
				"lastSync": "2015-06-22T18:31:42.678Z", 
				"kind": "admin#directory#chromeosdevice", 
				"ethernetMacAddress": "3863bb98f675", 
				"tenantCode": "some_tenant 3", 
				"macAddress": "38b1db95806d", 
				"orgUnitPath": "/Agosto/Beta/Fairchild Semi", 
				"serialNumber": "5CD45183S6", 
				"updated": "2015-06-22 21:01:17", 
				"gcmRegistrationId": "blah blah 3", 
				"created": "2015-06-22 21:01:17", 
				"annotatedUser": "fairchild@skykit.com", 
				"bootMode": "Verified", 
				"etag": "\"MO4FtId2-yiZq_-3TpU3AZTf2Ak/q2J1QVycAwick78q5218-w2DMgw\"", 
				"deviceId": "e80a9161-4367-4189-be90-450e5e29501b", 
				"lastEnrollmentTime": "2015-05-07T21:15:17.285Z", 
				"platformVersion": "6812.88.0 (Official Build) stable-channel zako", 
				"model": "HP Chromebox CB1-(000-099) / HP Chromebox G1", 
				"osVersion": "42.0.2311.153", 
				"firmwareVersion": ""
			}
			
+ Response 403 (application/json)

    + Headers

            Content-Type: application/json

    + Body

            {
                "error": "HTTP request API token is invalid."
            }
			

### POST /api/v1/devices
Create and register a Skykit device/display.

+ Request (application/json)

    + Headers

            Accept: application/json
            Authorization: 6C346588BD4C6D722A1165B43C51C

    + Body

            {
				"macAddress":"38b1db95806d",
				"gcmRegistrationId":"blah blah 3",
				"tenantCode":"some_tenant 3"
			}

+ Response 201 (application/json)

    + Headers

            Location: https://skykit-display-device-int.appspot.com/api/v1/devices/ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyGwsSDkNocm9tZU9zRGV2aWNlGICAgID4woQKDA
            Alternate-Protocol: 443:quic,p=1
            Cache-Control: no-cache
			
+ Response 403 (application/json)

    + Headers

            Content-Type: application/json

    + Body

            {
                "error": "HTTP request API token is invalid."
            }
