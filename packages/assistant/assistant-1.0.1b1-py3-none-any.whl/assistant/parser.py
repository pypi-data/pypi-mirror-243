# -*- coding: utf-8 -*-
"""Implements the xonsh parser."""
from xonsh.lazyasd import lazyobject
from xonsh.platform import PYTHON_VERSION_INFO
from xonsh.lexer import Lexer, LexToken
#from xonsh.parsers.base import BaseParser
from typing import List
import attr
# from pygments.token import Token
# from pygments.lexers import BashLexer
import pygments

@lazyobject
def Parser():
    if PYTHON_VERSION_INFO > (3, 8):
        from xonsh.parsers.v38 import Parser as p
    else:
        from xonsh.parsers.v36 import Parser as p
    return p


class AssistantParser():
    # def __init__(self):
    #     self.lexer = Lexer()

    def parse(self, s):
        #lexed = list(pygments.lex(s, self.lexer))
        words: List[str] = []
        error = False
        # known_tokens = (Token.Text, Token.Literal.Number, Token.Name.Builtin,
        #                 Token.Punctuation, Token.Keyword, Token.Literal.String.Double,
        #                 Token.Literal.String.Single)
        for value in s.split():
            stripped = value.strip()
            if len(stripped) > 0:
                words.append(value)
        # If the user starts the query with a question mark it forces running through model
        has_force_modeling_escape = False
        model_input_str = s
        if words[0].startswith("?"):
            words[0] = words[0][1:]
            has_force_modeling_escape = True
            model_input_str = model_input_str[1:]
        elif words[0] == "?":
            words = words[1:]
            has_force_modeling_escape = True
            model_input_str = model_input_str[1:]
        return ParseResult(was_error=error, words=words, model_input_str = model_input_str,
                           has_force_modeling_escape=has_force_modeling_escape)

@attr.s(frozen = True)
class ParseResult():
    words = attr.ib(converter=tuple)
    model_input_str = attr.ib()
    was_error = attr.ib(default=False)
    has_force_modeling_escape = attr.ib(default=False)
    def get_first_word(self):
        return self.words[0]
