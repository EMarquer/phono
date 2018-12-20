#! /usr/bin/env python3
from typing import Dict, Set, Tuple

import pandas as pd


# File path
PHON_FILE = "letters_phon.csv"
TEXT_FILE = "letters_text.csv"


def load_text(source_file: str = TEXT_FILE) -> Dict[str, Set[str]]:
    """Load the characters used in the text representation of the words
    and their CV categories
    
    :return: a dictionary with CV categories as keys and a set of the letters in those categories as values

    >>> {'CV category': {'char 1','char 2', ...}}
    """

    # Load the data
    text_data = pd.read_table(source_file, sep=' ', header=None).values

    # Transform the data into a dictionary
    text_dict = {}
    for cv_category, letters in text_data:

        # Get the set of letters already in the category
        # and add the new letters to the category
        # If no letter was in the category, `get` will return an empty set
        # With sets, the `|` operator is the 'union' operator
        text_dict[cv_category] = text_dict.get(cv_category, set()) | set(letters)

    return text_dict


def load_phon(source_file: str = PHON_FILE) -> Dict[str, Dict[Tuple[int, str], Set[str]]]:
    """Load the characters used in the phonetic representation of the words,
    their CV categories and their phonological categories
    
    :return: a dictionary with CV categories as keys and another dictionary as values
    that second dictionary contains phonological categories as keys and a set of the letters in those categories as
    values

    >>> {'CV category': 
            {('Rank 1', 'Phonologic category 1'): {'char 1','char 2', ...},
             'Rank 2', 'Phonologic category 2'): {'char 3','char 4', ...}}
        }
    """

    # Load the data
    phon_data = pd.read_table(source_file, sep=' ', header=None).values

    # Transform the data into a dictionary
    phon_dict = {}
    for cv_category, phon_rank, phon_category, letters in phon_data:

        # Create a single key for phonetic classification
        phon_key = (int(phon_rank), phon_category)

        # Make sure the dictionary contatins a value for the CV category
        if not cv_category in phon_dict.keys():
            phon_dict[cv_category] = dict()

        # Get the set of letters already in the phonologic category
        # and add the new letters to the category
        # If no letter was in the category, `get` will return an empty set
        # With sets, the `|` operator is the 'union' operator
        phon_dict[cv_category][phon_key] = phon_dict[cv_category].get(phon_key, set()) | set(letters)

    return phon_dict


# Produce the CV representation of a text character
def text_to_cv(char: str) -> str:
    """Produce the CV representation of a letter.
    If the character is unknown, returns the character itself and store it in a TEXT_UNK dictionary to keep track of
    unrecognised letters.

    :param char: character to transform to CV representation
    :return: the CV representation of the character (either 'C', 'V' or the character itself if it is not a known
    character)
    """

    for cv_category, letters in TEXT_DICT.items():
        if char in letters:
            return cv_category

    # If the character is not found, return it and save it as unknown
    TEXT_UNK.add(char)
    return char


# Produce the CV representation of a text character
def phon_to_cv(char: str) -> str:
    """Produce the CV representation of a phonetic character.
    If the character is unknown, returns the character itself and store it in a PHON_UNK dictionary to keep track of
    unrecognised characters.

    :param char: character to transform to CV representation
    :return: the CV representation of the character (either 'C', 'V' or the character itself if it is not a known
    character)
    """

    for cv_category, phon_category_dict in PHON_DICT.items():
        for phon_category, letters in phon_category_dict.items():
            if char in letters:
                return cv_category

    # If the character is not found, return it and save it as unknown
    PHON_UNK.add(char)
    return char


# Get the rank according to the sonority scale
def phon_to_rank(char: str) -> int:
    """Get the rank of a phonetic character according to the sonority scale.
    If the character is unknown, returns -1 and store it in a PHON_UNK dictionary to keep track of
    unrecognised characters.

    :param char: character to transform to CV representation
    :return: the rank of the character according to the scale (or -1 if it is not a known character)
    """

    for cv_category, phon_category_dict in PHON_DICT.items():
        for phon_category, letters in phon_category_dict.items():
            if char in letters:
                return phon_category[0]

    # If the character is not found, return it and save it as unknown
    PHON_UNK.add(char)
    return -1


# Get the phonetic class according to the sonority scale
def phon_to_class(char: str) -> str:
    """Get the phonetic class of a phonetic character according to the sonority scale.
    If the character is unknown, returns "" and store it in a PHON_UNK dictionary to keep track of
    unrecognised characters.

    :param char: character to transform to CV representation
    :return: the phonetic class of the character according to the scale (or "" if it is not a known character)
    """

    for cv_category, phon_category_dict in PHON_DICT.items():
        for phon_category, letters in phon_category_dict.items():
            if char in letters:
                return phon_category[1]

    # If the character is not found, return it and save it as unknown
    PHON_UNK.add(char)
    return ""


if __name__ == "__main__":
    import pprint as pp

    printer = pp.PrettyPrinter()

    printer.pprint(load_text())
    printer.pprint(load_phon())

# If imported
else:
    # Dictionaries (loaded from specific file)
    TEXT_DICT = load_text()
    PHON_DICT = load_phon()
    TEXT_UNK = set()
    PHON_UNK = set()
