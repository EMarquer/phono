#! /usr/bin/env python3
from collections import Counter
from typing import List, Optional

import pandas as pd
import pprint as pp

from dictionaries import phon_to_class
from transcribe import PHON_SEPARATOR, SYLLABLE_SEPARATOR


# Data that has been processed
DATA_FILE = "data/Output_File.txt"


def load_data(source_file: str = DATA_FILE) -> List[List[str]]:
    """Load data from CSV file

    :warning: phonetic fields, corresponding CV fields and syllabified fields may contain multiple values

    :param source_file: path to the file from which the data is loaded
    :return: a bi-dimensional list, with the first dimension being the lines, and the second being the words, where
    values in lines are ordered as follows:
    word, word_cv, phon, phon_cv, syll_phon, syll_cv
    """

    return pd.read_table(source_file, sep=' ', header=None).values.tolist()


def syllable_cv_list(data: List[List[str]]) -> List[str]:
    """Extract a list af all the syllables present in the data in form of their CV representation

    :param data: bi-dimensional list of data, where values in lines are ordered as follows:
    word, word_cv, phon, phon_cv, syll_phon, syll_cv
    :return: a list of all the syllables (duplicates are kept)
    """

    cv_list = []

    # CV syllables are in the last field
    for word, word_cv, phon, phon_cv, syll_phon, syll_cv in data:

        # separate the multiple phonetic representations
        for representation_CV in syll_cv.split(PHON_SEPARATOR):

            # add all the syllables in the representation in the list of syllables
            cv_list += representation_CV.split(SYLLABLE_SEPARATOR)

    return cv_list


def syllable_class_list(data: List[List[str]]) -> List[str]:
    """Extract a list af all the syllables present in the data in form of their phonetic class

    :param data: bi-dimensional list of data, where values in lines are ordered as follows:
    word, word_cv, phon, phon_cv, syll_phon, syll_cv
    :return: a list of all the syllables (duplicates are kept)
    """

    class_list = []

    # phonetic representation syllables are in the before-last field
    for word, word_cv, phon, phon_cv, syll_phon, syll_cv in data:

        # separate the multiple phonetic representations
        for representation_phon in syll_phon.split(PHON_SEPARATOR):

            # separate the syllables in the representation
            for syllable_phon in representation_phon.split(SYLLABLE_SEPARATOR):

                # transform the syllable in its class equivalent
                syllable_class = ''.join(phon_to_class(char) for char in syllable_phon)

                # add the transformed syllable to the list of syllables
                class_list.append(syllable_class)

    return class_list


def syllable_phon_list(data: List[List[str]]) -> List[str]:
    """Extract a list af all the syllables present in the data in form of their phonetic representation

    :param data: bi-dimensional list of data, where values in lines are ordered as follows:
    word, word_cv, phon, phon_cv, syll_phon, syll_cv
    :return: a list of all the syllables (duplicates are kept)
    """

    phon_list = []

    # phonetic representation syllables are in the before-last field
    for word, word_cv, phon, phon_cv, syll_phon, syll_cv in data:

        # separate the multiple phonetic representations
        for representation_CV in syll_phon.split(PHON_SEPARATOR):

            # add all the syllables in the representation in the list of syllables
            phon_list += representation_CV.split(SYLLABLE_SEPARATOR)

    return phon_list


def most_frequent(syllable_list: List[str], count: Optional[int] = 15):
    return Counter(syllable_list).most_common(count)


if __name__ == "__main__":

    # load processed data
    data = load_data()

    # question 1 - CV forms - 15 most frequent
    # extract list of syllables
    syllables_cv = syllable_cv_list(data)

    # compute the most common syllables
    syllables_cv_most_frequent = most_frequent(syllables_cv)

    # print the result
    print("Question 1")
    print("(total forms: {}, total different forms: {})".format(
        len(syllables_cv),
        len(Counter(syllables_cv).keys())
    ))
    pp.pprint(syllables_cv_most_frequent)

    # question 2 - phonetic classes
    # extract list of syllables
    syllables_class = syllable_class_list(data)

    # compute the most common syllables
    syllables_class_most_frequent = most_frequent(syllables_class)

    # print the result
    print("Question 2")
    print("(total forms: {}, total different forms: {})".format(
        len(syllables_class),
        len(Counter(syllables_class).keys())
    ))
    pp.pprint(syllables_class_most_frequent)

    # question 3 - phonetic constituents
    # extract list of syllables
    syllables_phon = syllable_phon_list(data)

    # compute the most common syllables
    syllables_phon_most_frequent = most_frequent(syllables_phon)

    # print the result
    print("Question 3")
    print("(total forms: {}, total different forms: {})".format(
        len(syllables_phon),
        len(Counter(syllables_phon).keys())
    ))
    pp.pprint(syllables_phon_most_frequent)
