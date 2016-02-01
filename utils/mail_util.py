__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'
import logging

import requests

from app_config import config


class MailHelper(object):
    """
    This class is responsible for providing methods on the MailGun API service

    Using the urlfetch interface provided by GAE, we can send HTTP requests to the API
    along with a payload... and utilize many of the powerful features describe in further
    detail here: http://documentation.mailgun.com/api_reference.html
    """
A    def post_message(recipients, subject, html=None, text=None, attachment=None):
        payload = {}
        payload['from'] = "Skykit Provisionning <noreply-provisioning@skykit.com>"
        payload['to'] = recipients
        payload['subject'] = subject
        if html:
            payload['html'] = html
        if text:
            payload['text'] = text
        attachments = [("attachment", attachment)] if attachment else None
        if config.EMAIL_SUPPORT:
            try:
                result = requests.post(
                    config.MAILGUN_MESSAGES_URL,
                    auth=("api", config.MAILGUN_APIKEY),
                    files=attachments,
                    data=payload)
                return_text = result.content
                if result.status_code != 200:
                    logging.error(return_text)
            except Exception, exp:
                logging.error("Error on URL Fetch.  Message may not have been delivered! %s" % exp)
                return_text = "Error on URL Fetch.  Message may not have been delivered! %s" % exp
        else:
            logging.warn("Message not sent.")
            return_text = "No message sent."
        return return_text
