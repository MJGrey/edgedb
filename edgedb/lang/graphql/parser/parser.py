##
# Copyright (c) 2016 MagicStack Inc.
# All rights reserved.
#
# See LICENSE for details.
##


from edgedb.lang.common import parsing
from .grammar import lexer


class GraphQLParser(parsing.Parser):
    def get_parser_spec_module(self):
        from .grammar import document
        return document

    def get_lexer(self):
        return lexer.GraphQLLexer()

    def process_lex_token(self, mod, tok):
        if tok.attrs['type'] in {'NL', 'WS', 'COMMENT', 'COMMA'}:
            return None
        else:
            return super().process_lex_token(mod, tok)