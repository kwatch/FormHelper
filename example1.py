# -*- coding: utf-8 -*-

from collections import OrderedDict

from formhelper import Form
import tenjin
from tenjin.helpers import *


class MemberForm(Form):

    MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec',)

    ROLES = OrderedDict([
            (2, 'Alien'),
            (5, 'Time Traveler'),
            (9, 'ESPer'),
            ])

    def validate(self):
        #
        k = 'name'
        v = self.params.get(k, '').strip()
        if not v:
            self.errors[k] = 'Required.'
        elif len(v) > 50:
            self.errors[k] = 'Too long (max 50 chars).'
        #
        k = 'age'
        v = self.params.get(k, '').strip()
        if not v:                      self.errors[k] = 'Required.'
        elif not v.isdigit():          self.errors[k] = 'Integer required.'
        #
        k = 'month'
        v = self.params.get(k, '').strip()
        if not v:                      self.errors[k] = 'Required.'
        elif not v.isdigit():          self.errors[k] = 'Integer required.'
        elif not (1 <= int(v) <= 12):  self.errors[k] = 'Unexpected value.'
        #
        k = 'gender'
        v = self.params.get(k, '').strip()
        if not v:                      self.errors[k] = 'Not selected.'
        elif not v in ('M', 'F'):      self.errors[k] = 'Unexpected value.'
        #
        k = 'role_flag'
        v = self.params.get(k, '').strip()
        if not v:                      self.errors[k] = 'Not selected.'
        elif not v in ('Y', 'N'):      self.errors[k] = 'Unexpected value.'
        #
        k = 'role_id'
        if self.params.get('role_flag') == 'Y':
            v = self.params.get(k, '').strip()
            if not v:                      self.errors[k] = 'Not selected.'
            elif not v.isdigit():          self.errors[k] = 'Integer required.'
            elif int(v) not in self.ROLES: self.errors[k] = 'Not found.'
        #
        k = 'role_name'
        if self.params.get('role_flag') == 'N':
            v = self.params.get(k, '').strip()
            if not v:                      self.errors[k] = 'Not entered.'
            elif len(v) > 100:             self.errors[k] = 'Too long (max 100 chars).'
        #
        k = 'confirmed'
        v = self.params.get(k, '').strip()
        if not v:                      self.errors[k] = 'Not confirmed.'
        elif v != 'Y':                 self.errors[k] = 'Unexpected value.'
        #
        return self.errors


def main():
    params = {
        #'name': 'Haruhi',
        'name': '',        # should not be empty
        'age':  'twenty',  # should be integer
        'month': '13',     # should be <= 12
        'role_flag': 'N',  # should be 'Y' or 'N'
        'role_id': '',
        'role_name': '',   # should not be empty when role_flag is 'N'
    }
    form = MemberForm(params)
    form.validate()

    engine = tenjin.Engine(postfix='.pyhtml')
    context = dict(form=form)
    html = engine.render(':example1', context)
    print(html.encode('utf-8'))


if __name__ == '__main__':
    main()
