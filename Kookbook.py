# -*- coding: utf-8 -*-


kookbook.default = 'test'


class test(Category):

    @recipe
    def default(c):
        """do test"""
        system(c%"baka.py -ss test")


@recipe('*.html')
@ingreds('$(1).py', '$(1).pyhtml')
def task_html(c):
    """generates *.html from *.py and *.pyhtml"""
    system(c%"python $(ingred) > $(product)")


@recipe
@ingreds('example1.html')
def task_html(c):
    """generates example1.html"""
    pass
