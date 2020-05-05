import sys
from string import punctuation
import json
from nltk.corpus import cmudict


# Load dictionary of words in haiku corpus but not in cmu dict
with open('missing_words.json') as f:
    missing_words = json.load(f)

cmudict = cmudict.dict()


def count_syllables(words):
    """Use corpora to count syllables in English word or phrase."""
    # prep words for cmudict corpus
    words = words.replace('-', ' ')
    words = words.lower().split()

    # initialise number of syllables in phrase or word
    num_sylls = 0

    # loop through each word in phrase and remove unnecessary parts
    for word in words:
        word = word.strip(punctuation)
        if word.endswith("'s") or word.endswith("’s"):
            word = word[:-2]

        if word in missing_words:
            # Part of the missing words dictionary
            num_sylls += missing_words[word]

        else:
            # Use the CMU dict and its phonemes
            for phonemes in cmudict[word][0]:
                for phoneme in phonemes:
                    if phoneme[-1].isdigit():
                        num_sylls += 1

    return num_sylls


def main():
    """Determine the number of syllables in a word or phrase"""
    while True:
        print("Syllable Counter")

        # get input for phrase
        word = input("Enter a word or phrase; else press enter to exit: ")
        if word == '':
            sys.exit()

        try:
            # count the syllables
            num_syllables = count_syllables(word)
            print(f"The number of syllables in {word} is {num_syllables}")
            print()

        except KeyError:
            # word not in CMU dict or missing words
            print("Word not found. Try again.\n", file=sys.stderr)


if __name__ == '__main__':
    main()
