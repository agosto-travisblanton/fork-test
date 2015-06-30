FORMAT: 1A
HOST: https://skykit-display-device-int.appspot.com

# Skykit Device Management API


## Subtitle
Also Markdown *formatted*. This also includes automatic "smartypants" formatting -- hooray!

> "A quote from another time and place"

Another paragraph. Code sample:

```http
Authorization: bearer 5262d64b892e8d4341000001
```

And some code with no highlighting:

```no-highlight
Foo bar baz
```

<!-- include(example-include.md) -->

## Group Devices

### GET /api/v1/devices
Retrieve all devices from Skykit Device Management

+ Request (application/json)

    + Headers

            Accept: application/json
            Authorization: 6C346588BD4C6D722A1165B43C51C



+ Response 200 (application/json)

    + Headers

            Content-Type: application/json

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

            Content-Type: application/json

    + Body

            {
                "error": "HTTP request API token is invalid."
            }

### GET /api/v1/devices?macAddress=38b1db95806d
Retrieve a specific Skykit device/display by MAC address.

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

            Content-Type: application/json

    + Body

            {
                "error": "HTTP request API token is invalid."
            }


### GET /api/v1/devices/ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyGwsSDkNocm9tZU9zRGV2aWNlGICAgID4woQKDA

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

+ Response 201 (text/html)

    + Headers

            Location: https://skykit-display-device-int.appspot.com/api/v1/devices/ahtzfnNreWtpdC1kaXNwbGF5LWRldmljZS1pbnRyGwsSDkNocm9tZU9zRGV2aWNlGICAgID4woQKDA
            Alternate-Protocol: 443:quic,p=1
            Cache-Control: no-cache



### Create New Note [POST]
Create a new note

+ Request

    + Headers

            Content-Type: application/json

    + Body

            {
                "title": "My new note",
                "body": "..."
            }

+ Response 201

+ Response 400

    + Headers

            Content-Type: application/json

    + Body

            {
                "error": "Invalid title"
            }

## Note [/notes/{id}]
Note description

+ Parameters

    + id: `68a5sdf67` (required, string) - The note ID

+ Model

    + Headers

            Content-Type: application/json
            X-Request-ID: f72fc914
            X-Response-Time: 4ms

    + Body

            {
                "id": 1,
                "title": "Grocery list",
                "body": "Buy milk"
            }

### Get Note [GET]
Get a single note.

+ Response 200

    [Note][]

+ Response 404

    + Headers

            Content-Type: application/json
            X-Request-ID: f72fc914
            X-Response-Time: 4ms

    + Body

            {
                "error": "Note not found"
            }

### Update a Note [PUT]
Update a single note

+ Request

    + Headers

            Content-Type: application/json

    + Body

            {
                "title": "Grocery List (Safeway)"
            }

+ Response 200

    [Note][]

+ Response 404

    + Headers

            Content-Type: application/json
            X-Request-ID: f72fc914
            X-Response-Time: 4ms

    + Body

            {
                "error": "Note not found"
            }

### Delete a Note [DELETE]
Delete a single note

+ Response 204

+ Response 404

    + Headers

            Content-Type: application/json
            X-Request-ID: f72fc914
            X-Response-Time: 4ms

    + Body

            {
                "error": "Note not found"
            }

# Group Users
Group description

## User List [/users{?name,joinedBefore,joinedAfter,sort,limit}]
A list of users

+ Parameters

    + name: `alice` (string, optional) - Search for a user by name
    + joinedBefore: `2011-01-01` (string, optional) - Search by join date
    + joinedAfter: `2011-01-01` (string, optional, ) - Search by join date
    + sort: `joined` (string, optional) - Which field to sort by
        + Default: `name`
        + Members
            + `name`
            + `joined`
            + `-joined`
            + `age`
            + `-age`
            + `location`
            + `-location`
            + `plan`
            + `-plan`
    + limit: `25` (integer, optional) - The maximum number of users to return, up to `50`
      + Default: `10`

+ Model

    + Headers

            Content-Type: application/json

    + Body

            [
                {
                    "name": "alice",
                    "image": "http://example.com/alice.jpg",
                    "joined": "2013-11-01"
                },
                {
                    "name": "bob",
                    "image": "http://example.com/bob.jpg",
                    "joined": "2013-11-02"
                }
            ]

    + Schema

            <!-- include(example-schema.json) -->

### Get users [GET]
Get a list of users. Example:

```no-highlight
https://api.example.com/users?sort=joined&limit=5
```

+ Response 200

    [User List][]

# Group Tags and Tagging Long Title
Get or set tags on notes

## GET /tags
Get a list of bars

+ Response 200

## Get one tag [/tags/{id}]
Get a single tag

### GET

+ Response 200