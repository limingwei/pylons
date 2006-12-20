import os
from gettext import *
from pkg_resources import resource_exists, resource_stream
from paste.deploy.config import CONFIG
import pylons

class LanguageError(Exception):
    """Exception raised when a problem occurs with changing languages"""
    pass

def gettext(value):
    """Mark a string for translation. Returns the localized string of value.
    
    Mark a string to be localized as follows:
    
    .. code-block:: Python
    
        gettext('This should be in lots of languages')
    """
    return pylons.translator.gettext(value)

def ugettext(value):
    """Mark a string for translation. Returns the localized unicode string of
    value.
    
    Mark a string to be localized as follows:
    
    .. code-block:: Python
    
        _('This should be in lots of languages')
    """
    return pylons.translator.ugettext(value)
_ = ugettext

def ngettext(singular, plural, n):
    """Mark a string for translation. Returns the localized string of the
    pluralized value.

    This does a plural-forms lookup of a message id. ``singular`` is used as
    the message id for purposes of lookup in the catalog, while ``n`` is used
    to determine which plural form to use. The returned message is a string.
    
    Mark a string to be localized as follows:
    
    .. code-block:: Python
    
        ngettext('There is %(num)d file here', 'There are %(num)d files here',
                 n) % {'num': n}
    """
    return pylons.translator.ngettext(singular, plural, n)

def ungettext(singular, plural, n):
    """Mark a string for translation. Returns the localized unicode string of
    the pluralized value.

    This does a plural-forms lookup of a message id. ``singular`` is used as
    the message id for purposes of lookup in the catalog, while ``n`` is used
    to determine which plural form to use. The returned message is a Unicode
    string.
    
    Mark a string to be localized as follows:
    
    .. code-block:: Python
    
        ungettext('There is %(num)d file here', 'There are %(num)d files here',
                  n) % {'num': n}
    """
    return pylons.translator.ungettext(singular, plural, n)

def set_lang(lang):
    """Set the i18n language used"""
    registry = pylons.request.environ['paste.registry']
    if lang is None:
        registry.replace(pylons.translator, NullTranslations())
    else:
        project_name = CONFIG['app_conf']['package']
        catalog_path = os.path.join('i18n', lang, 'LC_MESSAGES')
        if not resource_exists(project_name, catalog_path):
            raise LanguageError('Language catalog %s not found' % \
                                os.path.join(project_name, catalog_path))
        translator = egg_translation(project_name, lang=catalog_path)
        translator.pylons_lang = lang
        registry.replace(pylons.translator, translator)

def get_lang():
    """Return the current i18n language used"""
    return getattr(pylons.translator, 'pylons_lang', None)

def egg_translation(domain, lang):
    """
    This method doesn't do all the checking etc of the gettext.translation method
    but it seems to work.
    
    We can't just use gettext.translation because the .mo files might be in eggs
    """
    class_ = GNUTranslations
    return class_(resource_stream(domain, os.path.join(lang, '%s.mo' % domain)))

__all__ = ['gettext', 'ugettext', '_', 'ngettext', 'ungettext', 'set_lang',
           'get_lang']
