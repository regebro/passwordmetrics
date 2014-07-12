from io import open
from math import log
from collections import defaultdict

lemmas = defaultdict(lambda: 0)
chr_entropy = log(26, 2)

with open('ANC-written-count.txt', 'rt', encoding='latin-1') as infile:
    for line in infile.readlines():
        try:
            word, lemma, pos, count = line.strip().split('\t')
        except ValueError:
            # End of file
            break
        lemmas[lemma] += int(count)
    
if 'troubador' not in lemmas:
    # XKCD hack:
    lemmas['troubador'] = 1
    
most_common = max(lemmas.values())

for lemma, frequency in sorted(lemmas.items(), key=lambda x: x[1], reverse=True):
    # Calculate the words häufigkeit and use that as entropy.
    haufigkeit = 0.5 - log(frequency/most_common, 2)
    # If the entropy is *higher* than what you get with just characters, then it's
    # not a real word, and we skip it. Examples of this are the 'words' "abcd" and "fgh",
    # both in this database.
    if haufigkeit > len(lemma) * chr_entropy:
        continue
    print('%s %s' % (lemma, haufigkeit))
    