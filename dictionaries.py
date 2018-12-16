#! /usr/bin/env python3
from typing import Dict, Set

import pandas as pd


# File path
PHON_FILE="letters_phon.csv"
TEXT_FILE="letters_text.csv"


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


def load_phon(source_file: str = PHON_FILE) -> Dict[str, Dict[str, Set[str]]]:
    """Load the characters used in the phonetic representation of the words,
    their CV categories and their phonologic categories
    
    :return: a dictionary with CV categories as keys and another dictionary as values
    that second dictionary contains phonologic categories as keys and a set of the letters in those categories as values

    >>> {'CV category': 
            {'Phonologic category 1': {'char 1','char 2', ...},
             'Phonologic category 2': {'char 3','char 4', ...}}
        }
    """

    # Load the data
    phon_data = pd.read_table(source_file, sep=' ', header=None).values

    # Transform the data into a dictionary
    phon_dict = {}
    for cv_category, phon_category, letters in phon_data:

        # Make shure the dictionary contatins a value for the CV category
        if not cv_category in phon_dict.keys():
            phon_dict[cv_category] = dict()


        # Get the set of letters already in the phonologic category
        # and add the new letters to the category
        # If no letter was in the category, `get` will return an empty set
        # With sets, the `|` operator is the 'union' operator
        phon_dict[cv_category][phon_category] = phon_dict[cv_category].get(phon_category, set()) | set(letters)

    return phon_dict


if __name__=="__main__":
    import pprint as pp

    printer = pp.PrettyPrinter()

    printer.pprint(load_text())
    printer.pprint(load_phon())
