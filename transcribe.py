#! /usr/bin/env python3
from typing import List

import pandas as pd

from dictionaries import *


# File paths
SOURCE_FILE = "data/test.csv"
OUTPUT_FILE = "data/test_out.csv"
SOURCE_FILE = "data/Input_File.txt"
OUTPUT_FILE = "data/Output_File.txt"

# Dictionaries (loaded from specific file)
TEXT_DICT = load_text()
PHON_DICT = load_phon()
TEXT_UNK = set()
PHON_UNK = set()


# Reading data
def load_data(source_file: str = SOURCE_FILE) -> List[List[str]]:
    """Load data from CSV file

    :warning: phonetic fields may contain multiple values

    :param source_file: path to the file from which the data is loaded
    :return: a bi-dimensional list, with the first dimension being the lines, and the second being the words

    from file containing:

    >>> abaisses abEs
    >>> hérétique eʁetik
    >>> poêle pwal;pwɛl

    the result is:

    >>> [['abaisses', 'abEs'],
    >>>  ['hérétique', 'eʁetik'],
    >>>  ['poêle', 'pwal;pwɛl']]
    """

    return pd.read_table(source_file, sep=' ', header=None).values.tolist()


# Writing data
def save_data(data: List[List[str]], output_file: str = OUTPUT_FILE) -> None:
    """Save data in CSV file

    :warning: phonetic fields may contain multiple values

    :param data: a bi-dimensional list, with the first dimension being the lines, and the second being the words

    from the list:

    >>> [['abaisses', 'abEs'],
    >>>  ['hérétique', 'eʁetik'],
    >>>  ['poêle', 'pwal;pwɛl']]

    the file will contain:

    >>> abaisses abEs
    >>> hérétique eʁetik
    >>> poêle pwal;pwɛl

    :param output_file: path to the file from which the data is loaded
    """

    pd.DataFrame(data).to_csv(output_file, sep=' ', header=None, index=False)


# Produce the CV representation of a text character
def text_to_cv(char: str) -> str:
    """Produce the CV representation of a character and ask the user to categorise the character if it is unknown
    (using :code:`categorise_new_char()`)

    :param char: character to transform to CV representation
    :return: the CV representation of the character (either 'C', 'V' or the character itself if it is not a known character)
    """

    for cv_category, letters in TEXT_DICT.items():
        if char in letters:
            return cv_category

    # If the character is not found, return it and save it as unknown
    TEXT_UNK.add(char)
    return char

# Produce the CV representation of a text character
def phon_to_cv(char: str) -> str:
    """Produce the CV representation of a character and ask the user to categorise the character if it is unknown
    (using :code:`categorise_new_char()`)

    :param char: character to transform to CV representation
    :return: the CV representation of the character (either 'C', 'V' or the character itself if it is not a known character)
    """

    for cv_category, phon_category_dict in PHON_DICT.items():
        for phon_category, letters in phon_category_dict.items():
            if char in letters:
                return cv_category

    # If the character is not found, return it and save it as unknown
    PHON_UNK.add(char)
    return char


# Line by line processing
def process_line(line: List[str]) -> List[str]:
    """Produce the processed version of the line, \
    producing the CV transcription of the word and its phonetic representation

    :todo: add support for syllabification

    :param line: List of string:

    >>>['word', 'phonetic representation']

    :return: processed version of the word:

    >>>['word', 'word in CV', 'phonetic representation', 'phonetic in CV']
    """
    word, phone = line

    return [
        word,  # Word
        ''.join(text_to_cv(char) for char in word),  # Word in CV
        phone,  # Phonetic representation
        ''.join(phon_to_cv(char) for char in phone),  # Phonetic representation in CV
        # Phonetic syllable
        # Phonetic syllable in CV
    ]


# Line by line printing
def line_to_str(line: List[str]) -> str:
    """Represent a line as a string (only 2 elements and 4 elements lines are supported)

    :todo: adapt for syllabification

    :param line: line to representing as a string
    :return: string representing the line
    :raise ValueError: if the line does not contain 2 or 4 elements
    """
    # store length because it wil e used multiple times
    length = len(line)

    # print diferent things depending on the values
    # untreated data
    if length == 2:
        return "{0}, {1}".format(*line)

    # data without sylabification
    elif length == 4:
        return "{0} -> {1}, {2} -> {3}".format(*line)

    # data with sylabification
    elif length == 6:
        return "{0} -> {1} ({4}), {2} -> {3} ({5})".format(*line)

    raise ValueError("Wrong line length")


if __name__=="__main__":
    data = load_data()

    data = [process_line(line) for line in load_data()]

    print(*(line_to_str(line) for line in data), sep="\n")

    print("Unknown TEXT chars:", *TEXT_UNK)
    print("Unknown PHON chars:", *PHON_UNK)

    save_data(data)
