# -*- coding: utf-8 -*-


kookbook.default = 'test'


class test(Category):

    @recipe
    def default(c):
        system(c%"baka.py -ss test")
