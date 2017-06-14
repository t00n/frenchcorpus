# frenchcorpus
French language corpus from Larousse dictionary

# Use
To use this project, you will have to buy https://play.google.com/store/apps/details?id=pack.LarDicoFR and extract all Larousse*_fr.db files in the `data` directory

Install the requirements from `requirements.txt`

Run `python3 corpus.py`

This will create a `corpus.db` sqlite3 file in the `data` directory with (almost) every lemma in the French language annotated with lemma categories, number, gender, mode, tense etc...

Look at the DB schema to use it ;)
