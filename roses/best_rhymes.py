from typing import Dict, List, Tuple
import string
import nltk 
import os
import sys

nltk.download('cmudict')

WORDS = ['crisscross', 'dos', 'chess', 'completed', 'depleted', 'hugged']

# this is a placeholder because I dont know to get it from generate_rhyming_words(emotion: str, word_pairs: List[Dict[str, Tuple[str, str]]]) 
LASTWORDLINE2 = "help"  

def rhyme(inp, level):
    entries = nltk.corpus.cmudict.entries()
    syllables = [(word, syl) for word, syl in entries if word == inp]
    rhymes = []
    for (word, syllable) in syllables:
        rhyming_words = [word for word, pron in entries if pron[-level:] == syllable[-level:]]
        rhyming_words = evaluate_rhymes(word, rhyming_words)
        rhymes += rhyming_words
        
    return rhymes

def evaluate_rhymes(word: str, rhymes: List[str]) -> List[str]:
    """remove the rhymes that are subwords of the word (ie. remove 'self-help' if the word is 'help')."""

    # TODO this doesn't work as wanted
    for rhyme in rhymes:
        if word.find(rhyme) == len(word) - len(rhyme):
            rhymes.remove(rhyme)
        elif rhyme.find(word) == len(rhyme) - len(word): 
            rhymes.remove(rhyme)

    return rhymes

# setting how strict the rhyme has to be, can be changed
def define_strictness_of_rhyme(wordToRhyme):
    strictness = 3
    if len(LASTWORDLINE2) < 4:
            strictness = 2
    return strictness

def generate_rhyming_words(emotion: str, word_pairs: List[Dict[str, Tuple[str, str]]]):
    """
    Finds possible rhyming words for the ending of line 2
    """

    partials_and_rhymes = []
    for row in word_pairs:
        last_word_line2 = row['word_pair'][1] # see an example input in the end of this file
        strictness = define_strictness_of_rhyme(last_word_line2)
        row['rhymes'] = [rhyme(last_word_line2, strictness)]
        partials_and_rhymes.append(row)

    return partials_and_rhymes

# For testing
if __name__ == '__main__':
    example_emotion = 'sad'
    example_word_pairs = [{'word_pair': ("human", "boss"), 'verb': 'was'}, 
                            {'word_pair': ('animal', 'legged'), 'verb': 'is'}]
    output = generate_rhyming_words(example_emotion, example_word_pairs)
    print(output)
    