from google.appengine.api import urlfetch

__author__ = 'Christopher Bartling <chris.bartling@agosto.com>'


class ChromeOsDevicesApi(object):
    """ Facade encapsulating the Directory API of the Admin SDK. """

    # https://developers.google.com/admin-sdk/directory/v1/reference/chromeosdevices/list
    def list(self, customer_id):
        """
        Obtain a list of Chrome OS devices associated with a customer.

        :param customer_id: An identifier for a customer.
        :return: An array of Chrome OS devices.
        """
        urlfetch.set_default_fetch_deadline(60)
        url = 'https://www.googleapis.com/admin/directory/v1/customer/{0}/devices/chromeos'.format(customer_id)
        headers = {
            'Content-type': 'application/json',
            'Accept': 'application/json'
        }

        response = urlfetch.fetch(url=url, method=urlfetch.GET, headers=headers)
        if response.status_code == 200:
            pass
        else:
            pass


    # https://developers.google.com/admin-sdk/directory/v1/reference/chromeosdevices/update
    def update(self, customer_id, device_id, annotated_user=None, annotated_location=None, notes=None):
        """
        Update a Chrome OS device with annotated user, location and notes information.

        :param customer_id:
        :param device_id:
        :param annotated_user:
        :param annotated_location:
        :param notes:
        :return:
        """
        pass
