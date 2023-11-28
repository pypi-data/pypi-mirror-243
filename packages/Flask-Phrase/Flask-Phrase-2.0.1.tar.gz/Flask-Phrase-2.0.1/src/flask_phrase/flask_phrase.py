from flask_babel import gettext as gettext_original, ngettext as ngettext_original, lazy_gettext as lazy_gettext_original
from flask import current_app

class Phrase(object):

    def __init__(self, app=None):
        self.app = app
        app.jinja_env.install_gettext_callables(
            gettext,
            ngettext,
            newstyle=True
        )

def phrase_enabled():
    return current_app.config['PHRASEAPP_ENABLED']

def phrase_key(msgid):
    return current_app.config['PHRASEAPP_PREFIX'] + 'phrase_' + msgid + current_app.config['PHRASEAPP_SUFFIX']

def gettext(msgid, *args, **kwargs):
    if phrase_enabled():
        return phrase_key(msgid)
    else:
        return gettext_original(msgid, *args, **kwargs)

def lazy_gettext(msgid, *args, **kwargs):
    if phrase_enabled():
        return phrase_key(msgid)
    else:
        return lazy_gettext_original(msgid, *args, **kwargs)

def ngettext(msgid, *args, **kwargs):
    if phrase_enabled():
        return phrase_key(msgid)
    else:
        return ngettext_original(msgid, *args, **kwargs)
