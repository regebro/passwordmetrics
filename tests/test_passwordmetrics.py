#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_passwordmetrics
----------------------------------

Tests for `passwordmetrics` module.
"""
from __future__ import unicode_literals
import unittest
import passwordmetrics
import string


class TestPasswordMetrics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        passwordmetrics.configure()
        cls.words = {'correct': 1, 'horse': 2, 'battery': 3, 'staple': 4, 'a': 1, 'incorrect': 1, 'bat': 1}

    def test_wordcount(self):
        words, rest = passwordmetrics._find_words('correcthorseb!wdbatterystaplerWd3t', self.words)
        self.assertEqual(words, set(['battery', 'horse', 'correct', 'staple']))
        self.assertEqual(rest, 'b!wdrWd3t')

        words, rest = passwordmetrics._find_words('abcdefgh', self.words)
        self.assertEqual(words, {'a'})
        self.assertEqual(rest, 'bcdefgh')

        # Duplicate words count only as one word:
        words, rest = passwordmetrics._find_words('batterybattery', self.words)
        self.assertEqual(words, {'battery'})


    def test_groups(self):
        groups = passwordmetrics._find_groups('abcdefgh')
        self.assertEqual(groups[0], {'lowercase'})

        groups = passwordmetrics._find_groups('12345678')
        self.assertEqual(groups[0], {'digits'})

        groups = passwordmetrics._find_groups('aAaAaAaA')
        self.assertEqual(groups[0], {'lowercase', 'uppercase'})

        groups = passwordmetrics._find_groups('xyFg98%!')
        self.assertEqual(groups[0], {'lowercase', 'uppercase', 'digits', 'punctuation'})

    def test_character_entropy(self):
        entropy, unkown = passwordmetrics._character_entropy('abcdefgh')
        self.assertAlmostEqual(entropy, 37.6035177451287)

        entropy, unkown = passwordmetrics._character_entropy('12345678')
        self.assertAlmostEqual(entropy, 26.5754247590989)

        # Repeated characters count as one:
        entropy, unkown = passwordmetrics._character_entropy('aAaAaAaA')
        self.assertAlmostEqual(entropy, 11.4008794362821)

        # As good as it gets for an 8 char password
        entropy, unkown = passwordmetrics._character_entropy('xyFg98%!')
        self.assertAlmostEqual(entropy, 52.4367108134211)

    def test_substitutions(self):
        # This long password gets a reasonable score on characters alone
        self.assertAlmostEqual(passwordmetrics._character_entropy('Tr0ub4dor&3')[0], 65.54588851677637)
        # But much worse when considering it uses a word, even though it's misspelled and only
        # appears once in the whole corpus (because I put it there).
        self.assertAlmostEqual(passwordmetrics.metrics('Tr0ub4dor&3')['entropy'], 42.11714046349914)
        # Although still better than if there was no substitutions in the word
        self.assertAlmostEqual(passwordmetrics.metrics('Troubador&3')['entropy'], 31.332505617941614)

        words, rest = passwordmetrics._find_words('batterybattery', self.words)
        self.assertEquals(rest, '')

        words, rest = passwordmetrics._find_words('b4tteryb4ttery', self.words)
        self.assertEquals(rest, '4')

        words, rest = passwordmetrics._find_words('b4ttery8attery', self.words)
        self.assertEquals(rest, '48')

    def test_password_entropy(self):
        self.assertAlmostEqual(passwordmetrics.metrics('abcdefgh')['entropy'], 36.7646671442273)
        self.assertAlmostEqual(passwordmetrics.metrics('xyFg98%!')['entropy'], 55.49709479680921)
        self.assertAlmostEqual(passwordmetrics.metrics('correcthorsebatterystaple')['entropy'], 45.58216824444706)

    def test_password_metrics(self):
        metrics = passwordmetrics.metrics('correcthorseb!wdbatterystaplerWd3t')
        self.assertEqual(metrics['words'], {'et', 'stapler', 'i', 'correct', 'battery', 'horse'})
        self.assertEqual(metrics['used_groups'], {'uppercase', 'lowercase', 'punctuation', 'digits'})
        self.assertEqual(metrics['unused_groups'], {'non-printable', 'whitespace', 'other'})
        self.assertEqual(metrics['length'], 34)
        self.assertAlmostEqual(metrics['entropy'], 101.57032841892621)
        self.assertAlmostEqual(metrics['word_entropy'], 62.24279530886037)
        self.assertAlmostEqual(metrics['character_entropy'], 39.32753311006583)

        metrics = passwordmetrics.metrics('b4naNAf!ddler')
        self.assertEqual(metrics['words'], {'banana', 'fiddler'})
        self.assertEqual(metrics['used_groups'], {'uppercase', 'lowercase', 'punctuation', 'digits'})
        self.assertEqual(metrics['unused_groups'], {'non-printable', 'whitespace', 'other'})
        self.assertEqual(metrics['length'], 13)
        self.assertAlmostEqual(metrics['entropy'], 40.37060138599877)
        self.assertAlmostEqual(metrics['word_entropy'], 29.585966540441248)
        self.assertAlmostEqual(metrics['character_entropy'], 10.784634845557521)

        # Repeated words do not increase entropy
        # (Although they probably should add 1)
        self.assertEqual(passwordmetrics.metrics('battery')['entropy'],
                         passwordmetrics.metrics('batterybattery')['entropy'])

        # Repeated substitutions do not increase entropy:
        self.assertEqual(passwordmetrics.metrics('b4tterybattery')['entropy'],
                         passwordmetrics.metrics('b4tteryb4ttery')['entropy'])

        # Differenty substitutions *do' not increase entropy:
        self.assertNotEqual(passwordmetrics.metrics('b4tteryb4ttery')['entropy'],
                            passwordmetrics.metrics('b4ttery84ttery')['entropy'])


class TestCustomConfig(unittest.TestCase):

    def test_nonascii_chars(self):
        passwordmetrics.configure()
        # In 8-bit strings, ö is a part of Latin-1
        entropy, unkown = passwordmetrics._character_entropy(b'abcdefgh\xf6')
        self.assertEqual(unkown, set())

        # But this is not!
        entropy, unkown = passwordmetrics._character_entropy('abcdefgh\N{LATIN CAPITAL LETTER H WITH STROKE}')
        self.assertEqual(unkown, set('\N{LATIN CAPITAL LETTER H WITH STROKE}'))

        # If you want these to work, you have to make a custom configuration.
        # I'll make one that uses all unicode characters even under Python 2.
        # This also get's rid of the warning.
        if 'unicode' not in locals():
            unicode = str
        groups = {'lowercase': set(unicode(string.ascii_lowercase)),
                  'uppercase': set(unicode(string.ascii_uppercase)),
                  'digits': set(unicode(string.digits)),
                  'punctuation': set(unicode(string.punctuation)),
                  'whitespace': set(unicode(string.whitespace)),
                  'non-printable': set(unicode((i)) for i in range(128) if chr(i) not in string.printable), # non-printable
                  'extras': set('åäöö\N{LATIN CAPITAL LETTER H WITH STROKE}'),
                  }

        passwordmetrics.configure(groups=groups)
        # This will still raise an error,
        entropy, unkown = passwordmetrics._character_entropy('abcdefghö\N{LATIN CAPITAL LETTER H WITH STROKE}')
        self.assertEqual(unkown, set())
        # return to default config, just to be safe
        passwordmetrics.configure()

    def test_verifygroups(self):
        passwordmetrics.configure()
        groups = passwordmetrics.config['groups']
        for name, g in groups.items():
            for c in g:
                for n, x in groups.items():
                    if n == name:
                        continue
                    if c in x:
                        print("Group %s and group %s both have character %s" % (name, n, c))

if __name__ == '__main__':
    unittest.main()