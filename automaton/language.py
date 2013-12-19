# -*- coding: utf-8 -*-
import string

GRAMMAR = """
constant = anything:atom ?(atom in '{letters}{digits}') -> Constant(atom)
concat = concat:left constant:right -> Concat(left, right)
concat = concat:left choice:right -> Concat(left, right)
concat = constant:left constant:right -> Concat(left, right)
concat = constant:left choice:right -> Concat(left, right)

choice = concat:left '|' concat:right -> Choice(left, right)
choice = constant:left '|' concat:right -> Choice(left, right)
choice = choice:left constant:right -> Concat(left, right)
choice = '(' constant:left '|' constant:right ')' -> Choice(left, right)
choice = '(' concat:left '|' concat:right ')' -> Choice(left, right)
choice = concat:left '|' constant:right -> Choice(left, right)
choice = constant:left '|' constant:right -> Choice(left, right)

repetition = '*'

repeat = constant:value repetition -> Repeat(value)
repeat = choice:value repetition -> Repeat(value)
repeat = '(' concat:value ')' repetition -> Repeat(value)
repeat = '(' choice:value ')' repetition -> Repeat(value)

expr = (repeat | choice | concat | constant)
""".format(letters=string.letters, digits=string.digits)
