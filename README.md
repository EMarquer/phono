## Repository
### Files
*Nothing here yet*

### TODO
* [ ] find articles about *"syllabification theory based on the degree of sonority"*
* [ ] create script for `VC transcription`
* [ ] implement syllabification
* [ ] analyse the data and answer the question
* [ ] write report

### Last updates
*Nothing here yet*

------
# Automatic syllabification of French words
## Steps
1. Learn about "syllabification theory based on the degree of sonority"
2. Prepare a script that does the correspondance `word` -> `VC transcription` (see the definition bellow)
3. Adapt the `VC transcription` script to support `transcriptions` (implement/find a phonetic alphabet correspondance to `VC transcription`)
4. Implement a syllabification algorythm
5. Adapt the `VC transcription` script to support syllabified
6. Analyse the data to answer the questions:\
   > Calculate the 15 most frequent syllabic forms in French represented as:
   > 1. ‘C’ and ‘V’ forms
   > 2. macro‐class forms (see the definition bellow)
   > 3. by the consonant(s) and vowel syllabic constituents
   
   In wich we consider 3 kind of syllabic forms (we must find the 15 most frequent for each of them):
    1. `CV`-based
    2. `macro-class`-based
    3. syllabic constituant-based (phonetic transcription format ?)
7. Write the report (see the dedicated section)

### Planning / Length estimation
1. **?** 4~12 man.hour
2. 2~3 man.hour
3. 2~5 man.hour
4. **? (depends on 1.)** 10~15 man.hour probably
5. 1 man.hour
6. 3~6 man.hour
7. 8~20 man.hour

## Definitions
### VC transcription
* `V` represents a vowel 
* `C` represents a consonant

#### Examples
* Classical text:
    * `abaisses` -> `VCVVCCVC`
* Phonetic transcription
    * `abEs` -> `VCVC`

### Macro‐class
* fricativeV
* fricativeU
* stopV
* stopU
* nasal
* liquid
* Semi‐Vow
* vowel

Where `V` is voiced and `U` is unvoiced

we can use shorter labels

## File format
### Input
#### General format
```text
word_1_letters word_1_phonetic
word_2_letters word_2_phonetic
```

Each line correspond to a word and contains:
* `word_n_letters`: the word in letters
* `word_n_phonetic`: the word phonetic transcription in phonetic symbols

#### Example
```text
abaisses abEs
```

### Output
```text
word_1_letters word_1_letters_VC word_1_phonetic word_1_phonetic_VC word_1_phonetic_syllable word_1_phonetic_syllable_VC
word_2_letters word_2_letters_VC word_1_phonetic word_1_phonetic_VC word_1_phonetic_syllable word_1_phonetic_syllable_VC
```

Each line correspond to a word and contains:
* `word_n_letters`: the word in letters
* `word_n_letters_VC`: the `VC transcription` of the letters
* `word_n_phonetic`: the word phonetic transcription in phonetic symbols
* `word_n_phonetic_VC`: the `VC transcription` of the phonetic symbols
* `word_n_phonetic_syllable`: the word phonetic transcription in phonetic symbols, split in syllables
* `word_n_phonetic_syllable_VC`: the `VC transcription` of the phonetic symbols, split in syllables

#### Example
```text
abaisses VCVVCCVC abEs VCVC a-bEs V-CVC
```

## Report / deliverables content
> Describe the methodology used and the results obtained in a short text document (3 to 4 pages).\
> Cite in the introduction 1 or 2 (or more) studies useful for your subject.\
> You must also provide the associated data (speech recorded, annotations, ...) and the scripts you have developed. 
