# -*- coding: utf-8 -*-

from collections import OrderedDict
from markupsafe import Markup, escape

#|
#|UNDEFINED = object()
#|

class Form(object):

    def __init__(self, params):
        self.params = params
        self.errors = OrderedDict()

    def validate(self):
        raise NotImplementedError("%s.validate(): not implemented yet." % self.__class__.__name__)

    def item(self, name):
        """returns FormItem object."""
        value = self.params.get(name, '')
        error = self.errors.get(name, '')
        return FormItem(name, value, error)

    def to_hidden_parameters(self):
        buf = []; add = buf.append
        params = self.params
        for k in params:
            if not k.startswith('_'):
                v = params.get(k, '')
                add('<input type="hidden" name="%s" value="%s" />' % \
                                           (escape(k), escape(v)))
        return '\n'.join(buf)


class FormItem(object):

    _ERR_EXIST = Markup('class="err-exist"')
    _EMPTY     = Markup('')

    def __init__(self, name, value, error):
        self.name  = name
        self.value = value
        self.error = error

    @property
    def ec(self):
        """returns 'class="err-exist"' when form parameter has error."""
        return self.error and self._ERR_EXIST or self._EMPTY

    @property
    def em(self):
        """returns '<em class="err-desc">MESSAGE</em>' when form parameter has error."""
        return self.error and Markup('<em class="err-desc">%s</em>' % escape(self.error)) or self._EMPTY

    @property
    def nv(self):
        """returns 'name="..." value="..."'."""
        return Markup('name="%s" value="%s"' % (escape(self.name), escape(self.value)))

    def nvc(self, value):
        """returns 'name="..." value="..." checked="checked"'."""
        checked = self.value == value and ' checked="checked"' or ''
        return Markup('name="%s" value="%s"%s' % (escape(self.name), escape(value), checked))

    def vs(self, value):
        """returns 'value="..." selected="selected"'."""
        selected = self.value == str(value) and ' selected="selected"' or ''
        return Markup('value="%s"%s' % (escape(value), selected))


#|class FormHelper(object):
#|
#|    _ERR_EXIST = Markup('class="err-exist"')
#|
#|    def __init__(self, form):
#|        self._form = form
#|        self._param_stack = []
#|
#|    def __enter__(self):
#|        return self
#|
#|    def __exit__(self, *args):
#|        self._param_stack.pop()
#|
#|    def param(self, name):
#|        self._param_stack.append(name)
#|        return self
#|
#|    @property
#|    def last_param(self):
#|        return self._param_stack[-1]
#|
#|    def ec(self, name=None):
#|        """returns 'class="err-exist"' when form parameter has error."""
#|        if name is None: name = self.last_param
#|        return self._form.errors.get(name) and self._ERR_EXIST or ''
#|
#|    def em(self, name=None, emclass='err-desc'):
#|        """returns '<em class="err-desc">MESSAGE</em>' when form parameter has error."""
#|        if name is None: name = self.last_param
#|        errmsg = self._form.errors.get(name)
#|        if errmsg:
#|            return Markup('<em class="%s">%s</em>' % (emclass, escape(errmsg),))
#|        return ''
#|
#|    def nv(self, name=None):
#|        """returns ' name="..." value="..."'."""
#|        if name is None: name = self.last_param
#|        value = self._form.params.get(name, '')
#|        return Markup('name="%s" value="%s"' % (escape(name), escape(value)))
#|
#|    def nvc(self, name, value=UNDEFINED):
#|        """returns 'name="..." value="..." checked="checked"'."""
#|        if value is UNDEFINED:
#|            value = name
#|            name  = self.last_param
#|        checked = self._form.params.get(name, '') == value
#|        s = checked and ' checked="checked"' or ''
#|        return Markup('name="%s" value="%s"%s' % (escape(name), escape(value), s))
#|
#|
#|def checked(boolean):
#|    """returns 'checked="checked"' if boolean is truthy value."""
#|    return boolean and _CHECKED or ''
#|
#|def selected(boolean):
#|    """returns 'selected="selected"' if boolean is truthy value."""
#|    return boolean and _SELECTED or ''
#|
#|def disabled(boolean):
#|    """returns 'disabled="disabled"' if boolean is truthy value."""
#|    return boolean and _DISABLED or ''
#|
#|
#|_CHECKED  = Markup('checked="checked"')
#|_SELECTED = Markup('selected="selected"')
#|_DISABLED = Markup('disabled="disabled"')
