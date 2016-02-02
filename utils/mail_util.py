import logging

import requests

from app_config import config

__author__ = 'Bob MacNeal <bob.macneal@agosto.com>'


class MailUtil(object):
    ##############################################################################
    # Methods against the MailGun API:
    # https://documentation.mailgun.com/quickstart-sending.html#send-via-api
    ##############################################################################

    @staticmethod
    def send_message(recipients, subject, html=None, text=None, attachment=None):
        if config.EMAIL_SUPPORT:
            payload = {'from': config.MAIL_FROM,
                       'to': recipients,
                       'subject': subject
                       }
            if html:
                payload['html'] = html
            if text:
                payload['text'] = text
            attachments = [("attachment", attachment)] if attachment else None
            try:
                result = requests.post(
                    config.MAIL_MESSAGES_URL,
                    auth=("api", config.MAIL_API_KEY),
                    files=attachments,
                    data=payload)
                return_text = result.content
                if result.status_code != 200:
                    logging.error(return_text)
            except Exception, exp:
                logging.error("Error on URL Fetch. Message may not have been delivered! %s" % exp)
                return_text = "Error on URL Fetch. Message may not have been delivered! %s" % exp
        else:
            return_text = "Email support is set to False."
            logging.warning(return_text)
        return return_text

    @staticmethod
    def get_recipient_log_entries(recipient, begin_datetime=None, entry_limit=None):
        if begin_datetime is None:
            begin_datetime = "Mon, 1 Feb 2016 09:00:00 -0000"
        if entry_limit is None:
            entry_limit = 25
        return requests.get(
            config.MAIL_EVENTS_URL,
            auth=("api", config.MAIL_API_KEY),
            params={"begin": begin_datetime,
                    "ascending": "yes",
                    "limit": entry_limit,
                    "pretty": "yes",
                    "recipient": recipient})
