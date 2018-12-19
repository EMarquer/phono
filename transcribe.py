#! /usr/bin/env python3
from typing import List, Optional, Tuple

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

# Keys for the syllabification algorithm
ONSET, NUCLEUS, CODA = "onset", "nucleus", "coda"

SYLLABLE_SEPARATOR = "-"
PHON_SEPARATOR = ";"  # TODO not mannaged yet

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
    """Produce the CV representation of a letter.
    If the character is unknown, returns the character itself and store it in a TEXT_UNK dictionnary to keep track of
    unrecognised letters.

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
    """Produce the CV representation of a phonetic character.
    If the character is unknown, returns the character itself and store it in a PHON_UNK dictionnary to keep track of
    unrecognised characters.

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


# Get the rank according to the sonority scale
def phon_to_rank(char: str) -> int:
    """Get the rank of a phonetic character according to the sonority scale.
    If the character is unknown, returns -1 and store it in a PHON_UNK dictionnary to keep track of
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


def is_onset_legal(chars: str) -> bool:
    #criteria: >= 2

    return all(abs(phon_to_rank(chars[i]) - phon_to_rank(chars[i + 1])) > 1
               for i in range(len(chars) - 1))


def determine_syllable_components(chars: str, cv_form: str) -> List[Tuple[str, str, str]]:
    # ---------------
    # Begin algorithm
    # ---------------

    # We store the sequence of onsets, nuclei and codas as a list of tuples with the type of element ("onset", "nucleus"
    # or "coda"), the corresponding characters
    # ex: [("onset", "p", "C"), ("coda", "o", "V")]
    components = []

    # Store position of current character and length of the word
    current_char = 0
    length = len(cv_form)

    # adding consonants to first onset until the first vowel is found
    onset, onset_cv = "", ""
    while cv_form[current_char] != "V" and current_char < length:
        onset += chars[current_char]
        onset_cv += cv_form[current_char]
        current_char += 1
    components.append((ONSET, onset, onset_cv))

    # processing the characters left until the end of the word
    while current_char < length:
        # the current character is a nucleus (it must be a vowel)
        nucleus = chars[current_char]
        nucleus_cv = cv_form[current_char]
        current_char += 1
        components.append((NUCLEUS, nucleus, nucleus_cv))

        # if there is no character left, end the processing
        if current_char >= length:
            break

        # if there is no more vowel in the word (end the processing)
        elif "V" not in cv_form[current_char:]:
            coda = chars[current_char:]
            coda_cv = cv_form[current_char:]
            components.append((CODA, coda, coda_cv))
            break

        # in any other case, we try to split the sequence of consonants before the next vowel in legal coda and onset
        else:
            # we get the whole sequence of consonants before the next vowel
            onset, onset_cv = "", ""
            coda, coda_cv = "", ""
            while cv_form[current_char] != "V" and current_char < length:  # the length check is unnecessary
                onset += chars[current_char]
                onset_cv += cv_form[current_char]
                current_char += 1

            # we transfer the first character of the onset to the coda until the onset is legal
            while not is_onset_legal(onset) and len(onset) > 0:
                # We add a character to the coda
                coda += onset[0]
                coda_cv += onset_cv[0]

                # We remove the first character of the onset
                onset = onset[1:]
                onset_cv = onset_cv[1:]

            components.append((CODA, coda, coda_cv))
            components.append((ONSET, onset, onset_cv))

    return components


def concat_syllable_components(components: List[Tuple[str, str, str]]) -> Tuple[str, str]:

    # we suppose that the componants follow the construction rules

    def syllables():
        """Generator of syllables over the components"""
        syllable_phon, syllable_cv = "", ""
        previous_component = None

        for component_type, component_phon, component_cv in components:
            # if we are not at the beginning of the word (previous_component = None) and we begin a new syllable, yield
            # the previous syllable and start a new one
            if component_type in {ONSET, NUCLEUS} and previous_component in {CODA, NUCLEUS}:
                # yield the previous syllable
                yield syllable_phon, syllable_cv
                syllable_phon, syllable_cv = "", ""

            # Add the syllable content to the syllables
            syllable_phon += component_phon
            syllable_cv += component_cv

            # Store component type for next component
            previous_component = component_type

        # yield the last syllable
        yield syllable_phon, syllable_cv

    # Concatenate the syllables
    syllables_phon, syllables_cv = [], []
    for syllable_phon, syllable_cv in syllables():
        syllables_phon.append(syllable_phon)
        syllables_cv.append(syllable_cv)

    # Concatenate the syllables into one string
    syllables_phon = SYLLABLE_SEPARATOR.join(syllables_phon)
    syllables_cv = SYLLABLE_SEPARATOR.join(syllables_cv)

    return syllables_phon, syllables_cv


# Syllabification
def syllabify(chars: str, cv_form: Optional[str] = "") -> Tuple[str, str]:
    """Find the correct syllabification for a word using the phonetic scale theory and the maximal onset principle.

    Using the algorythm for the article "On the Syllabification of Phonemes", by Susan Bartlett, Grzegorz Kondrak and
    Colin Cherry

    :not supported: multiple phonetic representations concatenated with a `;`

    :param chars: phonetic characters corresponding to the representation of the word
    :param cv_form: optional argument for the CV-form of the word, if not provided it will be computed from provided
    characters
    :return: the syllabified phonetic representation and the equivalent in CV; all the syllables are in a single string,
    linked by a dash ("-", ex: "pomiE" -> "po-mi-E", "CV-CV-V")
    """

    # manage multiple phonetic representations concatenated
    if PHON_SEPARATOR in chars:
        phon_syllables, cv_syllables = [], []

        # compute and store the syllabification for each sub representation
        for sub_representation in chars.split(PHON_SEPARATOR):
            phon_syllables_, cv_syllables_ = syllabify(sub_representation)
            phon_syllables.append(phon_syllables_)
            cv_syllables.append(cv_syllables_)

        # join and return the syllabification for each sub representation
        return PHON_SEPARATOR.join(phon_syllables), PHON_SEPARATOR.join(cv_syllables)

    # managing missing or wrong CV representation
    if not cv_form or len(cv_form) != len(chars):
        cv_form = "".join(phon_to_cv(char) for char in chars)

    # Apply syllabification algorithm
    components = determine_syllable_components(chars, cv_form)

    # assembling the syllabified string and the equivalent CV representation
    phon_syllables, cv_syllables = concat_syllable_components(components)

    return phon_syllables, cv_syllables


# Line by line processing
def process_line(line: List[str]) -> List[str]:
    """Produce the processed version of the line, \
    producing the CV transcription of the word and its phonetic representation

    :todo: add support for syllabification
    :todo: add support for multi-representations of words

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
        *syllabify(phone)  # Phonetic syllable and syllable in CV
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
        return "{0} -> {1}, {2} -> {3} ({4} -> {5})".format(*line)

    raise ValueError("Wrong line length")


if __name__=="__main__":
    data = load_data()

    data = [process_line(line) for line in load_data()]

    print(*(line_to_str(line) for line in data), sep="\n")

    PHON_UNK.discard(PHON_SEPARATOR)
    print("Unknown TEXT chars:", *TEXT_UNK)
    print("Unknown PHON chars:", *PHON_UNK)

    save_data(data)
