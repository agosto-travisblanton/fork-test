from models import ChromeOsDevice, PlayerCommandEvent

query = ChromeOsDevice.query().order(ChromeOsDevice.created)
devices = query.fetch(5)
print 'Device count = ' + str(len(devices))
i = 0
for device in devices:
    i += 1
    payload = 'some-command'.format(i)
    gcm_registration_id = 'gcm-registration-id-{0}'.format(i)
    event = PlayerCommandEvent.create(device_urlsafe_key=device.key.urlsafe(),
                                      payload=payload, gcm_registration_id=gcm_registration_id)

    event.put()
    print 'Added ' + payload + ' event to ' + device.key.urlsafe()
    payload = 'another-command'.format(i)
    gcm_registration_id = 'gcm-registration-id-{0}'.format(i)
    event = PlayerCommandEvent.create(device_urlsafe_key=device.key.urlsafe(),
                                      payload=payload, gcm_registration_id=gcm_registration_id)
    event.player_has_confirmed = True
    event.put()
    print 'Added ' + payload + ' event to ' + device.key.urlsafe()
    payload = 'yet-another-command'.format(i)
    gcm_registration_id = 'gcm-registration-id-{0}'.format(i)
    event = PlayerCommandEvent.create(device_urlsafe_key=device.key.urlsafe(),
                                      payload=payload, gcm_registration_id=gcm_registration_id)

    event.player_has_confirmed = True
    event.put()
    print 'Added ' + payload + ' event to ' + device.key.urlsafe()
