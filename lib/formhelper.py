# -*- coding: utf-8 -*-

from collections import OrderedDict
from markupsafe import Markup, escape


class Form(object):

    def __init__(self, params):
        self.params = params
        self.errors = OrderedDict()

    def validate(self):
        raise NotImplementedError("%s.validate(): not implemented yet." % self.__class__.__name__)


class FormHelper(object):

    _ERR_EXIST = Markup('class="err-exist"')

    def __init__(self, form):
        self._form = form
        self._param_stack = []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._param_stack.pop()

    def param(self, name):
        self._param_stack.append(name)
        return self

    def ec(self, name):
        """returns 'class="err-exist"' when form parameter has error."""
        return self._form.errors.get(name) and self._ERR_EXIST or ''

    def em(self, name, emclass='err-desc'):
        """returns '<em class="err-desc">MESSAGE</em>' when form parameter has error."""
        errmsg = self._form.errors.get(name)
        if errmsg:
            return Markup('<em class="%s">%s</em>' % (emclass, escape(errmsg),))
        return ''

    def nv(self, name):
        """returns ' name="..." value="..."'."""
        value = self._form.params.get(name, '')
        return Markup('name="%s" value="%s"' % (escape(name), escape(value)))

    def nvc(self, name, value):
        """returns 'name="..." value="..." checked="checked"'."""
        checked = self._form.params.get(name, '') == value
        s = checked and ' checked="checked"' or ''
        return Markup('name="%s" value="%s"%s' % (escape(name), escape(value), s))


def checked(boolean):
    """returns 'checked="checked"' if boolean is truthy value."""
    return boolean and _CHECKED or ''

def selected(boolean):
    """returns 'selected="selected"' if boolean is truthy value."""
    return boolean and _SELECTED or ''

def disabled(boolean):
    """returns 'disabled="disabled"' if boolean is truthy value."""
    return boolean and _DISABLED or ''


_CHECKED  = Markup('checked="checked"')
_SELECTED = Markup('selected="selected"')
_DISABLED = Markup('disabled="disabled"')
