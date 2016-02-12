import Tenant, Key, datetime

something = [
    Tenant(key=Key('TenantEntityGroup', 'tenantEntityGroup', 'Tenant', 5066549580791808), active=True,
           admin_email=u'something@gmail.com', chrome_device_domain=None, class_version=1,
           content_manager_base_url=u'https://appspot.com', content_server_url=u'https://appspot.com',
           created=datetime.datetime(2016, 2, 12, 18, 22, 5, 573073),
           domain_key=Key('Domain', 5629499534213120), name=u'one', proof_of_play_logging=False,
           tenant_code=u'one', updated=datetime.datetime(2016, 2, 12, 18, 22, 5, 573081)),
    Tenant(key=Key('TenantEntityGroup', 'tenantEntityGroup', 'Tenant', 6192449487634432), active=True,
           admin_email=u'something@gmail.com', chrome_device_domain=None, class_version=1,
           content_manager_base_url=u'https://appspot.com', content_server_url=u'https://appspot.com',
           created=datetime.datetime(2016, 2, 12, 18, 22, 31, 853127),
           domain_key=Key('Domain', 5629499534213120), name=u'onetwothree',
           notification_emails=[u'adsfasF@gmail.com'], proof_of_play_logging=True, tenant_code=u'onetwothree',
           updated=datetime.datetime(2016, 2, 12, 18, 22, 31, 853138))
]
