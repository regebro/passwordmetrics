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
                
    def test_character_entropy(self):
        entropy, groups, unkown = passwordmetrics._character_entropy('abcdefgh')
        self.assertAlmostEqual(entropy, 37.6035177451287)
        self.assertEqual(groups, {'lowercase'})

        entropy, groups, unkown = passwordmetrics._character_entropy('12345678')
        self.assertAlmostEqual(entropy, 26.5754247590989)
        self.assertEqual(groups, {'digits'})

        # Repeated characters count as one:
        entropy, groups, unkown = passwordmetrics._character_entropy('aAaAaAaA')
        self.assertAlmostEqual(entropy, 11.4008794362821)
        self.assertEqual(groups, {'lowercase', 'uppercase'})

        # As good as it gets for an 8 char password
        entropy, groups, unkown = passwordmetrics._character_entropy('xyFg98%!')
        self.assertAlmostEqual(entropy, 52.4367108134211)
        self.assertEqual(groups, {'lowercase', 'uppercase', 'digits', 'punctuation'})
        
    def test_substitutions(self):
        # This long password gets a reasonable score on characters alone
        self.assertAlmostEqual(passwordmetrics._character_entropy('Tr0ub4dor&3')[0], 65.54588851677637)
        # But much worse when considering it uses a word, even though it's misspelled and only 
        # appears once in the whole corpus (because I put it there).
        self.assertAlmostEqual(passwordmetrics.metrics('Tr0ub4dor&3')['entropy'], 31.332505617941614)
                
    def test_password_entropy(self):
        self.assertAlmostEqual(passwordmetrics.metrics('abcdefgh')['entropy'], 36.7646671442273)
        self.assertAlmostEqual(passwordmetrics.metrics('xyFg98%!')['entropy'], 48.9425059451315)
        self.assertAlmostEqual(passwordmetrics.metrics('correcthorsebatterystaple')['entropy'], 45.58216824444706)
        
    def test_password_metrics(self):
        metrics = passwordmetrics.metrics('correcthorseb!wdbatterystaplerWd3t')
        self.assertEqual(metrics['words'], {'et', 'stapler', 'i', 'correct', 'battery', 'horse'})
        self.assertEqual(metrics['used_groups'], {'uppercase', 'lowercase'})
        self.assertEqual(metrics['unused_groups'], {'punctuation', 'non-printable', 'whitespace', 'digits', 'other'})
        self.assertEqual(metrics['length'], 34)
        self.assertAlmostEqual(metrics['entropy'], 85.04455418142474)
        self.assertAlmostEqual(metrics['word_entropy'], 62.24279530886037)
        self.assertAlmostEqual(metrics['character_entropy'], 22.80175887256437)
        

class TestCustomConfig(unittest.TestCase):
        
    def test_nonascii_chars(self):
        passwordmetrics.configure()
        # In 8-bit strings, ö is a part of Latin-1
        entropy, groups, unkown = passwordmetrics._character_entropy(b'abcdefgh\xf6')
        self.assertEqual(unkown, set())
           
        # But this is not!
        entropy, groups, unkown = passwordmetrics._character_entropy('abcdefgh\N{LATIN CAPITAL LETTER H WITH STROKE}')
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
        entropy, groups, unkown = passwordmetrics._character_entropy('abcdefghö\N{LATIN CAPITAL LETTER H WITH STROKE}')
        self.assertEqual(unkown, set())
        # return to default config, just to be safe
        passwordmetrics.configure()        

    def test_verifyg(self):
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