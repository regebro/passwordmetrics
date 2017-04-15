========
Usage
========

Basic usage
-----------

To use passwordmetrics you import it and run the configure method.

    >>> import passwordmetrics
    >>> passwordmetrics.configure()

You can then get metrics for passwords:

    >>> passwordmetrics.metrics('correcthorseb!wdbatterystaplerWd6t')
    {'unused_groups': {'whitespace', 'non-printable', 'other'},
     'word_entropy': 53.48690135737497,
     'entropy': 99.36902331911844,
     'words': {'battery', 'i', 'horse', 'stapler', 'correct'},
     'unknown_chars': set(),
     'used_groups': {'digits', 'uppercase', 'lowercase', 'punctuation'},
     'length': 34,
     'character_entropy': 45.882121961743465}


Advanced usage
--------------

The configure method makes it possibly to configure passwordmetrics for
your usecase. This is particularily useful if you want to have
language-specific wordlists or character groups:

    >>> import passwordmetrics
    >>> import string
    >>> from io import open

    >>> groups = {'lowercase': set(u'abcdefghijklmnopqrstuvxyz\xe5\xe4\xf6'),
    ...           'uppercase': set(u'ABCDEFGHIJKLMNOPQRSTUVXYZ\xc5\xd4\xd6'),
    ...           'digits': set(string.digits),
    ...           'punctuation': set(string.punctuation),
    ...           'whitespace': set(string.whitespace),
    ...           }

    >>> words = {}
    >>> with open('docs/ordlista_sv.txt', 'rt', encoding='latin-1') as wordlist:
    ...     for line in wordlist.readlines():
    ...         word, entropy = line.strip().split(' ')
    ...         words[word] = float(entropy)

    >>> substitutions = {'0': 'o', '1': 'i', '2': 'z', '3': 'e', '4': 'a',
    ...                  '5': 's', '6': 'b', '7': 't', '8': 'b', '9': 'g',
    ...                  '!': 'i', '#': 3, '$': 's', '&': 'g', '@': 'a',
    ...                  '[': 'c', '(': 'c', '+': 't', '{': '\xe4', '|': '\xf6',
    ...                  '}': '\xe5', '[': '\xd4', '\\': '\xd6', ']': '\xc5'}

    >>> passwordmetrics.configure(groups=groups, words=words, substitutions=substitutions)
    >>> passwordmetrics.metrics(u'korrekth\xe4stbatterih\xe4ftapparat')
    {'unused_groups': {'digits', 'uppercase', 'punctuation', 'whitespace'},
     'word_entropy': 29.3,
     'entropy': 29.3,
     'words': {u'batteri', u'korrekt', u'h\xe4ftapparat', u'h\xe4st'},
     'unknown_chars': set(),
     'used_groups': {'lowercase'},
     'length': 29,
     'character_entropy': 0}


``groups``
..........

``groups`` are character groups, such as digits, lowercase and uppercase. You
pass in sets of characters, and passwordmetrics will tell you which ones
were used. This is so that you, if desired, can disallow certain character
groups. You can also, of course, force certain character groups, but that is
a bad idea (more on that elsewhere).


``words``
.........

``words`` is a mapping of words to word frequency values. It is used to find
words in the password and base a calculation of the entropy based on that.
For example, a password containing common words should have a lower
entropy than a password containing uncommon words, as it is easier to guess.


``substitutions``
.................

``substitutions`` are character mappings for "leet" character substitutions.
For example, the words "alive" can be written "al1v3" in a way to make it
harder to guess. A mapping of substitutions is used to try and find words.
This is because a word with substitutions is easier to guess than a random
character string, although it is harder to guess than the same word without
substitutions.


The metrics
-----------

The returned metrics are:

    * entropy: A relative measure of how hard a password is to guess.

    * length: The total length of the password.

    * words: The words found in the password.

    * word_entropy: The entropy of the words.

    * character_entropy: The entropy of any characters not found in any words.

    * used_groups: The character groups used.

    * unused_groups: Any character groups that were not used.

    * unknown_chars: Characters in the password that were  not found in any groups.


Most of the metrics returned are returned only for completeness, not because
they are very useful.

``length`` is useful if you have a maximum password length your system can
handle and ``used_groups`` and ``unknown_chars`` is useful to make sure there
are no characters your system can't handle.

The most important metric is the "entropy". The higher the harder it is to
guess the passwords, and the harder it will be to forcibly crack the password.
Giving the user feedback on how safe/unsafe the password is based on this is
a good way to ensure that you have safe passwords.
