from peewee import *
import sqlite3
import os
from tqdm import tqdm
from sys import stderr

from parser import parse_categories, parse_modes, parse_tenses
from french_grammar import LexicalCategories, GrammaticalPersons, GrammaticalNumbers, GrammaticalGenders, GrammaticalModes, GrammaticalTenses, LemmaTypes

db = SqliteDatabase('data/corpus.db')

class LexicalCategory(Model):
    id_lexical_category = PrimaryKeyField()
    name = TextField(null=False, unique=True)

    class Meta:
        database = db

class Mode(Model):
    id_mode = PrimaryKeyField()
    name = CharField(50, null=False, unique=True)

    class Meta:
        database = db

class Tense(Model):
    id_tense = PrimaryKeyField()
    name = CharField(50, null=False, unique=True)

    class Meta:
        database = db

class Person(Model):
    id_person = PrimaryKeyField()
    name = CharField(50, null=False, unique=True)
    
    class Meta:
        database = db

class Gender(Model):
    id_gender = PrimaryKeyField()
    name = CharField(50, null=False, unique=True)
    
    class Meta:
        database = db

class Number(Model):
    id_number = PrimaryKeyField()
    name = CharField(50, null=False, unique=True)
    
    class Meta:
        database = db

class LemmaType(Model):
    id_type = PrimaryKeyField()
    name = CharField(50, null=False, unique=True)

    class Meta:
        database = db

class Lemma(Model):
    id_lemma = PrimaryKeyField()
    canonical_form = CharField(50, null=False, unique=True)
    lemma_type = ForeignKeyField(rel_model=LemmaType)

    class Meta:
        database = db

class LemmaCategories(Model):
    lexical_category = ForeignKeyField(rel_model=LexicalCategory)
    lemma = ForeignKeyField(rel_model=Lemma)

    class Meta:
        database = db
        primary_key = CompositeKey('lexical_category', 'lemma')

class Declension(Model):
    id_declension = PrimaryKeyField()
    lemma = ForeignKeyField(rel_model=Lemma)
    declined_form = CharField(50, null=False)

    class Meta:
        database = db
        indexes = (
            (('lemma', 'declined_form'), True),
        )

class Conjugation(Model):
    id_conjugation = PrimaryKeyField()
    lemma = ForeignKeyField(rel_model=Lemma)
    declined_form = CharField(50, null=False)
    mode = ForeignKeyField(rel_model=Mode)
    tense = ForeignKeyField(rel_model=Tense)
    person = ForeignKeyField(rel_model=Person, null=True)
    gender = ForeignKeyField(rel_model=Gender, null=True)
    number = ForeignKeyField(rel_model=Number, null=True)

    class Meta:
        database = db

db.connect()
db.create_tables([LexicalCategory, Person, Number, Gender, Mode, Tense, LemmaType, Lemma, Declension, Conjugation, LemmaCategories], True)

# lemma types
lexical_categories = {category: LexicalCategory.create(name=category.value) for category in LexicalCategories}
grammatical_persons = {person: Person.create(name=person.value) for person in GrammaticalPersons}
grammatical_numbers = {number: Number.create(name=number.value) for number in GrammaticalNumbers}
grammatical_genders = {gender: Gender.create(name=gender.value) for gender in GrammaticalGenders}
grammatical_modes = {mode: Mode.create(name=mode.value) for mode in GrammaticalModes}
grammatical_tenses = {tense: Tense.create(name=tense.value) for tense in GrammaticalTenses}
lemma_types = {lemma_type: LemmaType.create(name=lemma_type.value) for lemma_type in LemmaTypes}

def connect_db_files():
    for dbfile in os.listdir('data'):
        if dbfile.endswith('fr.db'):
            connection = sqlite3.connect('data/' + dbfile)
            yield connection
            connection.close()

with db.atomic():
    for connection in tqdm(connect_db_files(), "SQL files"):
        cursor = connection.cursor()
        lemmas = cursor.execute('SELECT index_nom_adresse, catgram, flexion, active_passive, inf_passe, part_present, part_pas_masc_sing, part_pas_masc_plur, part_pas_f_sing, part_pas_f_plur, part_pas_compose, id_detail_verbe FROM adresse LEFT JOIN flexions ON index_nom_adresse = flexion OR index_nom_adresse = canonique  LEFT JOIN detail_verbe ON inf_present = index_nom_adresse WHERE canonique IS NULL OR index_nom_adresse = canonique ORDER BY index_nom_adresse').fetchall()
        prev_word = ''
        new_lemma = None
        for lemma in tqdm(lemmas, "Lemmas"):
            # print(lemma)
            word, category, flexion, active_passive, inf_passe, part_present, part_pas_masc_sing, part_pas_masc_plur, part_pas_f_sing, part_pas_f_plur, part_pas_compose, id_detail_verbe = lemma
            if word != prev_word and word != '':
                prev_word = word
                try:
                    new_lemma = Lemma.create(canonical_form=word, lemma_type=lemma_types[LemmaTypes.SIMPLE])
                except IntegrityError as e:
                    print(e)
                cats = parse_categories(category)
                for cat in cats:
                    try:
                        LemmaCategories.create(lemma=new_lemma, lexical_category=lexical_categories[cat])
                    except IntegrityError as e:
                        print(new_lemma.canonical_form, lexical_categories[cat])
                        print(e)
                if active_passive != None:
                    Conjugation.create(lemma=new_lemma, declined_form=word, mode=grammatical_modes[GrammaticalModes.INFINITIVE], tense=grammatical_tenses[GrammaticalTenses.PRESENT])
                    if inf_passe:
                        Conjugation.create(lemma=new_lemma, declined_form=inf_passe, mode=grammatical_modes[GrammaticalModes.INFINITIVE], tense=grammatical_tenses[GrammaticalTenses.PASSE])
                    if part_present:
                        Conjugation.create(lemma=new_lemma, declined_form=part_present, mode=grammatical_modes[GrammaticalModes.PARTICIPE], tense=grammatical_tenses[GrammaticalTenses.PRESENT])
                    if part_pas_masc_sing:
                        Conjugation.create(lemma=new_lemma, declined_form=part_pas_masc_sing, mode=grammatical_modes[GrammaticalModes.PARTICIPE], tense=grammatical_tenses[GrammaticalTenses.PASSE], gender=grammatical_genders[GrammaticalGenders.MASCULINE], number=grammatical_numbers[GrammaticalNumbers.SINGULAR])
                    if part_pas_masc_plur:
                        Conjugation.create(lemma=new_lemma, declined_form=part_pas_masc_plur, mode=grammatical_modes[GrammaticalModes.PARTICIPE], tense=grammatical_tenses[GrammaticalTenses.PASSE], gender=grammatical_genders[GrammaticalGenders.MASCULINE], number=grammatical_numbers[GrammaticalNumbers.PLURAL])
                    if part_pas_f_sing:
                        Conjugation.create(lemma=new_lemma, declined_form=part_pas_f_sing, mode=grammatical_modes[GrammaticalModes.PARTICIPE], tense=grammatical_tenses[GrammaticalTenses.PASSE], gender=grammatical_genders[GrammaticalGenders.FEMININE], number=grammatical_numbers[GrammaticalNumbers.SINGULAR])
                    if part_pas_f_plur:
                        Conjugation.create(lemma=new_lemma, declined_form=part_pas_f_plur, mode=grammatical_modes[GrammaticalModes.PARTICIPE], tense=grammatical_tenses[GrammaticalTenses.PASSE], gender=grammatical_genders[GrammaticalGenders.FEMININE], number=grammatical_numbers[GrammaticalNumbers.PLURAL])
                    if part_pas_compose:
                        Conjugation.create(lemma=new_lemma, declined_form=part_pas_compose, mode=grammatical_modes[GrammaticalModes.PARTICIPE], tense=grammatical_tenses[GrammaticalTenses.PASSE_COMPOSE])
                    conjugations = cursor.execute('SELECT ps1, ps2, ps3, pp1, pp2, pp3, mode, temps FROM detail_conj WHERE det_verbe=%i' % id_detail_verbe).fetchall()
                    for conjugation in conjugations:
                        ps1, ps2, ps3, pp1, pp2, pp3, mode, tense = conjugation
                        mode = parse_modes(mode)
                        tense = parse_tenses(tense)
                        if ps1:
                            Conjugation.create(lemma=new_lemma, declined_form=ps1, mode=grammatical_modes[mode], tense=grammatical_tenses[tense], person=grammatical_persons[GrammaticalPersons.FIRST], number=grammatical_numbers[GrammaticalNumbers.SINGULAR])
                        if ps2:
                            Conjugation.create(lemma=new_lemma, declined_form=ps2, mode=grammatical_modes[mode], tense=grammatical_tenses[tense], person=grammatical_persons[GrammaticalPersons.SECOND], number=grammatical_numbers[GrammaticalNumbers.SINGULAR])
                        if ps3:
                            Conjugation.create(lemma=new_lemma, declined_form=ps3, mode=grammatical_modes[mode], tense=grammatical_tenses[tense], person=grammatical_persons[GrammaticalPersons.THIRD], number=grammatical_numbers[GrammaticalNumbers.SINGULAR])
                        if pp1:
                            Conjugation.create(lemma=new_lemma, declined_form=pp1, mode=grammatical_modes[mode], tense=grammatical_tenses[tense], person=grammatical_persons[GrammaticalPersons.FIRST], number=grammatical_numbers[GrammaticalNumbers.PLURAL])
                        if pp2:
                            Conjugation.create(lemma=new_lemma, declined_form=pp2, mode=grammatical_modes[mode], tense=grammatical_tenses[tense], person=grammatical_persons[GrammaticalPersons.SECOND], number=grammatical_numbers[GrammaticalNumbers.PLURAL])
                        if pp3:
                            Conjugation.create(lemma=new_lemma, declined_form=pp3, mode=grammatical_modes[mode], tense=grammatical_tenses[tense], person=grammatical_persons[GrammaticalPersons.THIRD], number=grammatical_numbers[GrammaticalNumbers.PLURAL])

            if flexion != None:
                try:
                    Declension.create(lemma=new_lemma, declined_form=flexion)
                except IntegrityError as e:
                    print(new_lemma.canonical_form, flexion)
                    print(e)