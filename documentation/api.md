FORMAT: 1A
HOST: https://skykit-display-device-int.appspot.com

# Skykit Provisioning API

## Group Devices

### GET /api/v1/devices
Retrieve all *managed* devices from Skykit Provisioning

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
            
### GET /api/v1/devices?pairingCode={pairing_code}
Retrieve a specific *unmanaged* Skykit device/display by pairing code.

+ Parameters

    + pairing_code: `7eb8-50d2-1c04-dc36` (required, string) - The code displayed by player following unmanaged device registration.



+ Request

    + Headers

            Accept: application/json
            Authorization: 6C346588BD4C6D722A1165B43C51C



+ Response 200

    + Headers

            content-type: application/json
            cache-control: no-cache

    + Body

            {
				"apiKey": "a0f518aebfd04a7196df7a6c8b2aa29c",
				"isUnmanagedDevice": "true",
				"macAddress": "38b1db95806d",
				"pairingCode": "7eb8-50d2-1c04-dc36",
				"key": "ah1kZXZ-c2t5a2l0LWRpc3BsYXktZGV2aWNlLWludHIbCxIOQ2hyb21lT3NEZXZpY2UYgICAgICAwAoM",
				"gcmRegistrationId": "cf70a8d78a6dfa6df76df049",
				"created": "2015-11-03 18:19:20",
				"updated": "2015-11-03 18:19:20"
			}


+ Response 403

    + Headers

            content-type: text/html; charset=utf-8
            cache-control: no-cache

    + Body

            {
                "error": "403 Forbidden"
            }

+ Response 404

    + Headers

            content-type: text/html; charset=utf-8
            cache-control: no-cache

    + Body

            {
                "error": "404 Not Found"
            }


### GET /api/v1/devices?macAddress={mac_address}
Retrieve a specific Skykit device/display by MAC address.

+ Parameters

    + mac_address: `38b1db95806d` (required, string) - The device's MAC address for wireless or Ethernet networking.



+ Request

    + Headers

            Accept: application/json
            Authorization: 6C346588BD4C6D722A1165B43C51C



+ Response 200

    + Headers

            content-type: application/json
            cache-control: no-cache

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


+ Response 403

    + Headers

            content-type: text/html; charset=utf-8
            cache-control: no-cache

    + Body

            {
                "error": "403 Forbidden"
            }

+ Response 404

    + Headers

            content-type: text/html; charset=utf-8
            cache-control: no-cache

    + Body

            {
                "error": "404 Not Found"
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

    + Body

            {
                "error": "HTTP request API token is invalid."
            }


### PUT /api/v1/devices/{urlsafe_key}

Update Skykit device/display information.


+ Parameters

    + urlsafe_key: `ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyGwsSDkNocm9tZU9zRGV2aWNlGICAgID4woQKDA` (required, string) - The device's entity key.

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

+ Response 204 (application/json)

    + Headers

            Alternate-Protocol: 443:quic,p=1
            Cache-Control: no-cache

+ Response 403 (application/json)

    + Headers

    + Body

            {
                "error": "HTTP request API token is invalid."
            }
			
+ Response 422 (text/html)

    + Headers

    + Body

            Unable to retrieve Chrome OS device by device id: {directory_api_device_id}


## Group Tenants

### GET /api/v1/tenants
Retrieve all tenants from Skykit Provisioning

+ Request (application/json)

    + Headers

            Accept: application/json
            Authorization: 6C346588BD4C6D722A1165B43C51C



+ Response 200 (application/json)

    + Headers


    + Body

            [
               {
                  "updated":"2015-07-07 18:23:24",
                  "name":"DemoAgostoQA",
                  "created":"2015-07-07 18:08:25",
                  "content_server_url":"https://skykit-display-int.appspot.com/content",
                  "chrome_device_domain":"skykit.com",
                  "key":"ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyOwsSEVRlbmFudEVudGl0eUdyb3VwIhF0ZW5hbnRFbnRpdHlHcm91cAwLEgZUZW5hbnQYgICAgOCslAkM",
                  "tenant_code":"demoagostoqa",
                  "active":true,
                  "admin_email":"skdqa@demo.agosto.com"
               },
               ...
            ]

+ Response 403 (application/json)

    + Headers

    + Body

            {
                "error": "HTTP request API token is invalid."
            }
