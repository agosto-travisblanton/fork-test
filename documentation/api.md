FORMAT: 1A
HOST: https://skykit-display-device-int.appspot.com

# Skykit Provisioning API

## Group Displays

### GET /api/v1/displays
Retrieve all displays (managed and unmanaged) from Skykit Provisioning

+ Request (application/json)

    + Headers

            Accept: application/json
            Authorization: 6C346588BD4C6D722A1165B43C51C



+ Response 200 (application/json)

    + Headers


    + Body

            {
                "paging": {
                    "has_next": false, 
                    "has_prev": false, 
                    "next_cursor": null, 
                    "prev_cursor": null
                }, 
                "objects": [
                    {
                        "key": "ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyFAsSB0Rpc3BsYXkYgICAgJnOlAkM", 
                        "gcm_registration_id": "c098d70a8d78a6dfa6df76dfas7", 
                        "annotated_location": "Agosto HQ Reception Area", 
                        "annotated_user": "administrator@skykit.com", 
                        "firmware_version": "Google_Panther.4920.24.26", 
                        "boot_mode": "Verified", 
                        "platform_version": "6946.55.0 (Official Build) stable-channel panther", 
                        "os_version": "43.0.2357.81", 
                        "org_unit_path": "/Beta/Agosto Internal", 
                        "mac_address": "54271e6950ed", 
                        "serial_number": "E3MSCX012112", 
                        "api_key": "6a5cb915-68b9-4474-bd5f-5e6ac4ba4a63", 
                        "status": "DEPROVISIONED", 
                        "updated": "2015-07-30 19:06:23", 
                        "managed_display": true, 
                        "device_id": "964f4e0b-a06a-4ba8-97ab-5db2ba9f9cbd", 
                        "kind": "admin#directory#chromeosdevice", 
                        "created": "2015-07-30 19:06:21", 
                        "notes": "Some notes about the device from Directory API.", 
                        "ethernet_mac_address": "c454443bebe3", 
                        "last_sync": "2015-07-16T19:09:02.108Z", 
                        "last_enrollment_time": "2014-08-06T19:27:01.969Z", 
                        "model": "ASUS Chromebox",
                        "tenant": {
                            "updated": "2015-07-08 21:27:32", 
                            "name": "Foobar", 
                            "created": "2015-07-02 20:32:48", 
                            "content_server_url": "https://skykit-contentmanager-int.appspot.com", 
                            "chrome_device_domain": "foobar.com", 
                            "tenant_code": "foobar", 
                            "active": true, 
                            "admin_email": "admin@foobar.com"
                        } 
                    },
                    ...
                ]
            }


+ Response 403 (application/json)

    + Headers

    + Body

            {
                "error": "HTTP request API token is invalid."
            }


### GET /api/v1/displays?macAddress={mac_address}
Retrieve a specific Skykit display by MAC address.

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
                "paging": {
                    "has_next": false, 
                    "has_prev": false, 
                    "next_cursor": null, 
                    "prev_cursor": null
                }, "objects": [
                    {
                        "gcm_registration_id": "c098d70a8d78a6dfa6df76dfas7", 
                        "annotated_location": "Agosto HQ Reception Area", 
                        "annotated_user": "administrator@skykit.com", 
                        "firmware_version": "Google_Panther.4920.24.26", 
                        "boot_mode": "Verified", 
                        "platform_version": "6946.55.0 (Official Build) stable-channel panther", 
                        "os_version": "43.0.2357.81", 
                        "org_unit_path": "/Beta/Agosto Internal", 
                        "mac_address": "54271e6950ed", 
                        "serial_number": "E3MSCX012112", 
                        "api_key": "6a5cb915-68b9-4474-bd5f-5e6ac4ba4a63", 
                        "status": "DEPROVISIONED", 
                        "updated": "2015-07-30 19:06:23", 
                        "managed_display": true, 
                        "key": "ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyFAsSB0Rpc3BsYXkYgICAgJnOlAkM", 
                            "tenant": {"updated": "2015-07-08 21:27:32", 
                            "name": "Foobar", 
                            "created": "2015-07-02 20:32:48", 
                            "content_server_url": "https://skykit-contentmanager-int.appspot.com", 
                            "chrome_device_domain": "foobar.com", 
                            "tenant_code": "foobar", 
                            "active": true, 
                            "admin_email": "admin@foobar.com"
                        }, 
                        "device_id": "964f4e0b-a06a-4ba8-97ab-5db2ba9f9cbd", 
                        "kind": "admin#directory#chromeosdevice", 
                        "created": "2015-07-30 19:06:21", 
                        "notes": "", 
                        "ethernet_mac_address": "c454443bebe3", 
                        "last_sync": "2015-07-16T19:09:02.108Z", 
                        "last_enrollment_time": "2014-08-06T19:27:01.969Z", 
                        "model": "ASUS Chromebox"
                    }
                ]
            }



+ Response 403 (application/json)

    + Headers

    + Body

            {
                "error": "HTTP request API token is invalid."
            }


## Group Devices

### GET /api/v1/devices
Retrieve all devices from Skykit Provisioning

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
