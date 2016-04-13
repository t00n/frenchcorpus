import re
import json
from french_grammar import *

def is_permutation(l1, l2):
    res = True
    for elem in l1:
        if elem not in l2:
            res = False
    for elem in l2:
        if elem not in l1:
            res = False
    return res

lexical_categories = {
    LexicalCategories.ADJECTIVE: '.*adjecti.*',
    LexicalCategories.ADVERB: '.*adverb.*',
    LexicalCategories.DETERMINER: '.*article.*',
    LexicalCategories.COORD_CONJUNCTION: '.*conjoncti.*',
    LexicalCategories.INTERJECTION: '.*interjecti.*',
    LexicalCategories.NOUN: '[ ]?(nom|mon)[ ]?',
    LexicalCategories.PREPOSITION: '.*prépositi.*',
    LexicalCategories.PRONOUN: '[ ]?pronom[ ]?',
    LexicalCategories.VERB: '(.* |^)verb.*'
}

lexical_subcategories = {
    
}

def parse_categories(s):
    splitted = re.split('et|ou', s[:-1])
    items = []
    for x in splitted:
        for cat, regex in lexical_categories.items():
            match = re.match(regex, x)
            if match:
                items.append(cat)
    return items

grammatical_modes = [
    GrammaticalModes.INDICATIVE,
    GrammaticalModes.IMPERATIVE,
    GrammaticalModes.SUBJONCTIVE,
    GrammaticalModes.CONDITIONAL,
]

def parse_modes(s):
    return grammatical_modes[s-1]

grammatical_tenses = [
    GrammaticalTenses.PRESENT,
    GrammaticalTenses.IMPARFAIT,
    GrammaticalTenses.PASSE_SIMPLE,
    GrammaticalTenses.FUTUR,
    GrammaticalTenses.PASSE_COMPOSE,
    GrammaticalTenses.PLUSQUEPARFAIT,
    GrammaticalTenses.PASSE_ANTERIEUR,
    GrammaticalTenses.FUTUR_ANTERIEUR,
    GrammaticalTenses.PASSE
]
def parse_tenses(s):
    return grammatical_tenses[s-1]

if __name__ == '__main__':
    fixture = json.load(open('fixtures/categories.json'))

    with open('data/categories.txt') as f:
        for i, line in enumerate(f):
            splitted = re.split('et|ou', line[:-1])
            categories = parse_categories(splitted)
            try:
                assert is_permutation([category.value for category in categories], fixture[i])
            except AssertionError:
                print(i, line, categories, fixture[i])