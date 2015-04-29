# -*- coding: utf-8 -*-
import math
import string
import collections
from io import open

__version__ = '1.0b1'

config = {}

def configure(groups=None, words=None, substitutions=None):
    global config

    # Define up the d   ifferent character groups.
    if groups is None:
        # The default splits Latin-1 into seven different groups. The three last should be avoided, really.
        groups = {'lowercase': set(string.ascii_lowercase),
                  'uppercase': set(string.ascii_uppercase),
                  'digits': set(string.digits),
                  'punctuation': set(string.punctuation),
                  'whitespace': set(string.whitespace),
                  'non-printable': set(chr(i) for i in range(128) if chr(i) not in string.printable), # non-printable
                  'other': set(chr(i) for i in range(128, 256)), # latin-1
                  }
    config['groups'] = groups

    # Configure the word list
    if words is None:
        # XXX Open as resource instead
        words = {}
        with open('passwordmetrics/wordlist_en.txt', 'rt', encoding='latin-1') as wordlist:
            for line in wordlist.readlines():
                word, entropy = line.strip().split(' ')
                words[word] = float(entropy)
    config['words'] = words

    # Set up common substitutions:
    if substitutions is None:
        substitutions = {'0': 'o', '1': 'i', '2': 'z', '3': 'e', '4': 'a',
                         '5': 's', '6': 'b', '7': 't', '8': 'b', '9': 'g',
                         '!': 'i', '#': '3', '$': 's', '&': 'g', '@': 'a',
                         '[': 'c', '(': 'c', '+': 't'}
    config['substitutions'] = substitutions


def _find_groups(pw):
    groups = config['groups']
    unused_groups = set(groups.keys())
    used_groups = set()

    for c in pw:
        for group in unused_groups:
            if c in groups[group]:
                used_groups.add(group)
                unused_groups.remove(group)
                break

    return used_groups, unused_groups


def _find_words(pw, words):
    """Returns the found words and the non-word characters"""
    max_len = max(map(len, words)) #longest word in the set of words
    max_chunks = max_len - 1
    words_found = set()
    chunks = []

    # Replace leet spellings
    substituted = ''.join([config['substitutions'].get(c, c).lower() for c in pw])

    # Find all possible words in the password
    for c in substituted:
        chunks = [chunk + c for chunk in chunks]
        chunks.insert(0, c)
        if len(chunks) > max_len:
            chunks.pop()
        for chunk in chunks:
            if chunk in words:
                words_found.add(chunk) #add to set of words

    # In "canotier" the above will find 'canotier', 'can', 'not', 'tier',
    # 'an', 'no' and 'a'. But only 'canotier' should count.
    rest = pw
    found = set()
    # We sort the words on length, and then alphabetically for consistency.
    # What order words are handled in can make a difference on entropy.
    # Should you for example have "2can0the" as a password it contains "can",
    # "not" and "the". If it picks "not" as the first word, this is the only
    # one that is found, but otherwise it will find "can" and "not". Possibly
    # this algorithm could be changed to try to find the most non-overlapping
    # words (and hence the lowest entropy) but this is good enough I think.
    remaining = substituted
    for word in sorted(words_found, key=lambda x: (len(x), x), reverse=True):
        word_length = len(word)
        while True:
            pos = remaining.find(word)
            if pos == -1:
                break
            rest = rest[:pos] + rest[pos+word_length:]
            remaining = remaining[:pos] + remaining[pos+word_length:]
            found.add(word)

    # Now check if any of these found words used character replacements.
    # In that case add those replacements to the "rest" to increase entropy.
    for word in found:
        start = 0
        while True:
            pos = substituted.find(word, start)
            if pos == -1:
                break
            original = pw[pos:pos+len(word)]
            for c in original:
                if c in config['substitutions']:
                    if c not in rest:
                        rest += c
            # Find all copies of the word
            start = pos + 1

    return found, rest


def _character_entropy(pw):
    if not pw:
        return 0, set()

    chars = set()
    unknown = set()
    for char in pw:
        if isinstance(char, int):
            char = chr(char)
        for name, group in config['groups'].items():
            if char in group:
                chars.update(group)
                break
        else:
            # The character is in none of the groups
            unknown.add(char)

    bit_per_word = math.log(len(chars), 2) # ie 128 characters would make 7 bits
    return len(set(pw)) * bit_per_word, unknown


def metrics(pw):
    all_words = config['words']
    used_groups, unused_groups = _find_groups(pw)
    found_words, rest = _find_words(pw, all_words)
    w = sum(all_words[word] for word in found_words)
    c, unknown = _character_entropy(rest)
    return {'entropy': w + c,
            'word_entropy': w,
            'character_entropy': c,
            'words': found_words,
            'used_groups': used_groups,
            'unused_groups': unused_groups,
            'length': len(pw),
            'unknown_chars': unknown,
            }
