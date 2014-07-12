#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_passwordmetrics
----------------------------------

Tests for `passwordmetrics` module.
"""

import unittest

import passwordmetrics


class TestPasswordMetrics(unittest.TestCase):

    def setUp(self):
        passwordmetrics.configure()
        self.words = {'correct': 1, 'horse': 2, 'battery': 3, 'staple': 4, 'a': 1, 'incorrect': 1, 'bat': 1}
        
    def test_wordcount(self):
        words, rest = passwordmetrics._find_words('correcthorseb!wdbatterystaplerWd3t', self.words)
        self.assertEqual(words, set(['battery', 'horse', 'correct', 'staple']))
        self.assertEqual(rest, 'b!wdrWd3t')

        words, rest = passwordmetrics._find_words('abcdefgh', self.words)
        self.assertEqual(words, {'a'})
        self.assertEqual(rest, 'bcdefgh')        
                
    def test_character_entropy(self):
        entropy, groups = passwordmetrics._character_entropy('abcdefgh')
        self.assertAlmostEqual(entropy, 37.6035177451287)
        self.assertEqual(groups, {'lowercase'})

        entropy, groups = passwordmetrics._character_entropy('12345678')
        self.assertAlmostEqual(entropy, 26.5754247590989)
        self.assertEqual(groups, {'digits'})

        # Repeated characters count as one:
        entropy, groups = passwordmetrics._character_entropy('aAaAaAaA')
        self.assertAlmostEqual(entropy, 11.4008794362821)
        self.assertEqual(groups, {'lowercase', 'uppercase'})

        # As good as it gets for an 8 char password
        entropy, groups = passwordmetrics._character_entropy('xyFg98%!')
        self.assertAlmostEqual(entropy, 52.4367108134211)
        self.assertEqual(groups, {'lowercase', 'uppercase', 'digits', 'punctuation'})
        
    def test_substitutions(self):
        # This long password gets a reasonable score on characters alone
        self.assertAlmostEqual(passwordmetrics._character_entropy('Tr0ub4dor&3')[0], 65.54588851677637)
        # But much worse when considering it uses a word, even though it's misspelled and only 
        # appears once in the whole corpus (because I put it there).
        self.assertAlmostEqual(passwordmetrics.metrics('Tr0ub4dor&3')['entropy'], 31.332505617941614)
                
    def test_passwordmetrics(self):
        self.assertAlmostEqual(passwordmetrics.metrics('abcdefgh')['entropy'], 36.7646671442273)
        self.assertAlmostEqual(passwordmetrics.metrics('xyFg98%!')['entropy'], 48.9425059451315)
        self.assertAlmostEqual(passwordmetrics.metrics('correcthorsebatterystaple')['entropy'], 45.58216824444706)
        self.assertAlmostEqual(passwordmetrics.metrics('correcthorseb!wdbatterystaplerWd3t')['entropy'], 85.04455418142474)
        

if __name__ == '__main__':
    unittest.main()