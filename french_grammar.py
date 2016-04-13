from enum import Enum

class LexicalCategories(Enum):
    ADJECTIVE='A'
    PREPOSITION='P'
    ADVERB='ADV'
    COORD_CONJUNCTION='C'
    DETERMINER='D'
    INTERJECTION='I'
    NOUN='N'
    PRONOUN='PR'
    SUBORD_CONJUNCTION='SUB'
    VERB='V'

class GrammaticalPersons(Enum):
    FIRST='1'
    SECOND='2'
    THIRD='3'

class GrammaticalNumbers(Enum):
    SINGULAR='SG'
    PLURAL='PL'

class GrammaticalGenders(Enum):
    FEMININE='F'
    MASCULINE='M'

class GrammaticalModes(Enum):
    INFINITIVE='I'
    PARTICIPE='P'
    GERONDIVE='G'
    INDICATIVE='IN'
    IMPERATIVE='IM'
    SUBJONCTIVE='S'
    CONDITIONAL='C'

class GrammaticalTenses(Enum):
    PRESENT='PR'
    IMPARFAIT='I'
    PASSE_SIMPLE='PS'
    FUTUR='F'
    PASSE_COMPOSE='PC'
    PLUSQUEPARFAIT='PQP'
    PASSE_ANTERIEUR='PA'
    FUTUR_ANTERIEUR='FA'
    PASSE='P'

class LemmaTypes(Enum):
    SIMPLE='S'
    COMPOSED='C'
    COMPLEX='X'