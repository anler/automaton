# -*- coding: utf-8 -*-
import parsley
import ometa

from .language import GRAMMAR
from .nodes import Constant, Concat, Choice, Repeat


parse = parsley.makeGrammar(GRAMMAR, {
    "Concat": Concat,
    "Choice": Choice,
    "Constant": Constant,
    "Repeat": Repeat
})


ParseError = ometa.runtime.ParseError
