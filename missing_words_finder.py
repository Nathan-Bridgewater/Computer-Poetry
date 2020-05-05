"""This module produces a .json file containing a dictionary of words. This
dictionary represents all the words from a text file which are not included in
the CMU pronunciation dictionary along with their syllable count. The output
from this program will aid in counting syllables for any word or phrase.

The CMU pronunciation dictionary contains data in the form:
{word : phonemes}
where phonemes are distinct units of sound - useful for counting syllables
for example {aged : ['EY1', 'JH', 'D']

For all the words not included in the CMU dictionary you can define their
syllable count manually.
"""

import sys
from string import punctuation
import pprint
import json
from nltk.corpus import cmudict

# Load the CMU pronunciation dictionary
cmudict = cmudict.dict()  # Carnegie Mellon University Pronouncing Dictionary


def main():
    haiku = load_haiku('train.txt')
    exceptions = cmudict_missing(haiku)
    build_dict = input("\nManually build an exceptions dictionary (y/n)? \n")
    if build_dict.lower() == 'n':
        sys.exit()
    else:
        missing_words_dict = make_exceptions_dict(exceptions)
        save_exceptions(missing_words_dict)


def load_haiku(filename):
    """Open and return training corpus of haiku as a set."""
    with open(filename) as in_file:
        haiku = set(in_file.read().replace('-', ' ').split())
        return haiku


def cmudict_missing(word_set):
    """Find and return words in word set mssing from cmudict."""
    # define a set to hold the unique words not included in cmudict
    exceptions = set()

    # loop through each word in text (in this case a haiku poem),
    # removing unnecessary parts like punctuation
    for word in word_set:
        word = word.lower().strip(punctuation)
        if word.endswith("'s") or word.endswith("’s"):
            word = word[:-2]

        # add word to exceptions if not in cmudict
        if word not in cmudict:
            exceptions.add(word)

    print("\nexceptions:")
    print(*exceptions, sep="\n")
    print(f"Number of unique words in haiku: {len(word_set)}")
    print(f"Number of words in corpus not in cmudict = {len(exceptions)}")
    membership = (1 - (len(exceptions) / len(word_set))) * 100
    print(f"cmudict membership = {membership:.1f}%")
    return exceptions


def make_exceptions_dict(exceptions_set):
    """Return dictionary of words & syllable counts from a set of words"""
    # define missing_words dict
    missing_words = {}
    print("Input # syllables in a word. Mistakes can be corrected at the end\n")

    # loop through set of missing words and allow input for number of syllables
    for word in exceptions_set:
        while True:
            num_sylls = input(f"Enter nymber syllables in {word}: ")
            if num_sylls.isdigit():
                break
            else:
                print("         Not a valid answer", file=sys.stderr)

        # print results and give next options
        missing_words[word] = int(num_sylls)
        print()
        pprint.pprint(missing_words, width=1)

        print("\nMake changes to dictionary before saving?")
        print("""
        0 - Exit and Save
        1 - Add a word or change syllable count
        2 - Remove a word
        """)

        # Allow user to add new words, change words or exit
        while True:
            choice = input("\nEnter Choice: ")
            if choice == '0':
                break
            elif choice == '1':
                word = input("Word to add or change: ")
                missing_words[word] = int(input(f"Enter number of syllables"))
            elif choice == '2':
                word = input("\nEnter word to delete: ")
                missing_words.pop(word, None)

            print("\nNew words or syllable changes:")
            pprint.pprint(missing_words, width=1)

        return missing_words


# Save results as .json file
def save_exceptions(missing_words):
    """sSave exceptions dictionary as json file"""
    json_string = json.dumps(missing_words)
    f = open('missing_words.json', 'w')
    f.write(json_string)
    f.close()
    print("\nFile saved as miss_words.json")


if __name__ == '__main__':
    main()
