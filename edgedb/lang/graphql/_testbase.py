##
# Copyright (c) 2016 MagicStack Inc.
# All rights reserved.
#
# See LICENSE for details.
##


import os
import re

from edgedb.lang._testbase import BaseParserTest, must_fail
from edgedb.lang.common import markup
from edgedb.lang.graphql import codegen
from edgedb.lang.graphql.parser import parser


class ParserTest(BaseParserTest):
    re_filter = re.compile(rb'''(?x)
        [\s,]+ | (\#.*?\n) | (\xef\xbb\xbf) | (\xfe\xff) | (\xff\xfe)
    ''')
    parser_cls = parser.GraphQLParser

    def get_parser(self, *, spec):
        return self.__class__.parser_cls()

    def assert_equal(self, expected, result):
        expected_stripped = self.re_filter.sub(b'', expected).lower()
        result_stripped = self.re_filter.sub(b'', result).lower()

        assert expected_stripped == result_stripped, \
            '[test]expected: {}\n[test] != returned: {}'.format(
                expected, result)

    def run_test(self, *, source, spec):
        debug = bool(os.environ.get('DEBUG_GRAPHQL'))
        if type(source) is bytes:
            bsource = source
        else:
            bsource = source.encode()

        if debug:
            if type(source) is bytes:
                print(source)
            else:
                markup.dump_code(source, lexer='graphql')

        p = self.get_parser(spec=spec)

        esast = p.parse(bsource)

        if debug:
            markup.dump(esast)

        processed_src = codegen.GraphQLSourceGenerator.to_source(esast)

        if debug:
            markup.dump_code(processed_src, lexer='graphql')

        expected_src = bsource

        self.assert_equal(expected_src, processed_src.encode())