#! /usr/bin/env python3
from typing import List

import pandas as pd

# File paths
SOURCE_FILE = "data/test.cv"
OUTPUT_FILE = "data/test_out.cv"

# Dictionaries (will be loaded and saved to file)
VOWEL_DICT = {letter for letter in 'aeiouy' + 'éèàù'}
CONSONANT_DICT = {letter for letter in 'bcdfghjklmnpqrstvwxz' + 'ç'}
NON_LETTER_DICT = {';'}


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


# Managing unknown characters
def categorise_new_char(char: str) -> None:
    """Prompt the user to categorise a character, then add the caracter to the corresponding category

    :param char: character to categorise
    """

    # Prompt for character category, until a valid category is given
    choice = None

    while not choice:
        try:
            # Ask for user input
            choice = input("The character '{}' is unknown. Is it a:"
                           "\n(C) Consonant\n(V) Vowel\n(N) Not a letter"
                           "\n(Please input the letter in parenthesis corresponding to the correct answer):\n".
                           format(char))

            choice = choice.strip().lower()

            # Check validity of the input
            if choice not in {'c', 'v', 'n'}:
                raise ValueError

        # Manage value errors
        except ValueError:
            print("Invalid input")
            choice = None

    # Add the letter to the dictionary corresponding to the selected category
    {'c': CONSONANT_DICT,
     'v': VOWEL_DICT,
     'n': NON_LETTER_DICT}[choice].add(char)


# Produce the CV representation of a character & prompt if character is unknown
def char_to_cv(char: str) -> str:
    """Produce the CV representation of a character and ask the user to categorise the character if it is unknown
    (using :code:`categorise_new_char()`)

    :param char: character to transform to CV representation
    :return: the CV representation of the character (either 'C', 'V' or the character itself if it is not a letter)
    """

    # We know the character and it is a vowel
    if char in VOWEL_DICT:
        return 'V'

    # We know the character and it is a consonant
    elif char in CONSONANT_DICT:
        return 'C'

    # We know the character and it is a non-letter character
    elif char in NON_LETTER_DICT:
        return char

    # We do not know the character
    else:

        # We categorise the letter
        categorise_new_char(char)

        # We get the correct value for the letter
        return char_to_cv(char)


# Producing the CV representation for a word
def word_to_cv(word: str) -> str:
    """Produce the CV representation of word

    :param word: a word (or a phonetic representation of a word)
    :return: a CV version of the word
    """
    return ''.join(char_to_cv(char) for char in word.lower())


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
        word_to_cv(word),  # Word in CV
        phone,  # Phonetic representation
        word_to_cv(phone),  # Phonetic representation in CV
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
    if length == 2:
        return "{0}, {1}".format(*line)

    elif length == 4:
        return "{0} -> {1}, {2} -> {3}".format(*line)

    raise ValueError("Wrong line length")


if __name__=="__main__":
    data = load_data()

    data = [process_line(line) for line in load_data()]

    print(*(line_to_str(line) for line in data), sep="\n")

    save_data(data)
