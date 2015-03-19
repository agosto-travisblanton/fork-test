# coding=utf-8
import json
import os
import logging

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

ENGLISH_CODE = 'en'
GERMAN_CODE = 'de'

SUPPORTED_LANGUAGES = [ENGLISH_CODE, GERMAN_CODE]


def get_codec(language):
    try:
        return json.load(open("{}/i18n/{}/text.json".format(__location__, language)), encoding='utf-8')
    except IOError:
        raise ValueError("{} unsupported language".format(language))


def resolve_i18n_text(text_key, language, *replacement_args):
    """
    Note this will HTML escape keys and values as needed.
    :param text_key:
    :param language:
    :param replacement_args:
    :return: ascii string with correct i18n codepage values and substitutions, both of which may be html escaped.
    """
    codec = get_codec(language)
    text = codec.get(text_key)
    if None is text:
        logging.warn("¡¡ No value for i18n key !! '{}'".format(text_key))
        return text_key
    text = text.encode("utf8")
    if None is not replacement_args and 0 < len(replacement_args):
        new_arg_replace = []
        for arg in replacement_args:
            try:
                float(arg)
                new_arg_replace.append(str(arg))
            except:
                arg = arg.encode('utf8')
                new_arg_replace.append(arg)
        text = text.format(*new_arg_replace)
    return text
