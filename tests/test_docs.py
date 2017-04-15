import sys
import re
import doctest
import manuel.doctest
import manuel.codeblock
import manuel.testing
import unittest


if sys.version_info[0] < 3:
    # Just don't do them under Python 3.
    # Sigh.

    class CustomChecker(doctest.OutputChecker):

        def check_output(self, want, got, optionflags):
            got = re.sub("set\(\[([^\]]+?)\]\)", "{\\1}", got)
            got = re.sub("set\(\[]\)", "set()", got)
            return doctest.OutputChecker.check_output(self, want, got, optionflags)

        def additional_tests():
            m = manuel.doctest.Manuel(optionflags=doctest.NORMALIZE_WHITESPACE,
                                      checker=CustomChecker())
            m += manuel.codeblock.Manuel()
            return manuel.testing.TestSuite(m, r'../docs/usage.rst')

if __name__ == '__main__':
    unittest.TextTestRunner().run(additional_tests())
