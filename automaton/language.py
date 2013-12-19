# -*- coding: utf-8 -*-
import string

GRAMMAR = """
repetition = '*'

constant = constant:value repetition -> Repeat(Constant(value))
constant = anything:atom ?(atom in '{letters}{digits}!_,;') -> Constant(atom)

expr = expr:left expr:right -> Concat(left, right)
expr = expr:value repetition -> Repeat(value)
expr = '(' expr:left ('|' expr:right ')' -> Choice(left, right)
                      | ')' -> left)
expr = constant

regex = (expr)
""".format(letters=string.letters, digits=string.digits)
