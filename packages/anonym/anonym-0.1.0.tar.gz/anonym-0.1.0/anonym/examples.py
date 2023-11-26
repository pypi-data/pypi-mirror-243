# %%
# import anonym
# print(dir(anonym))
# print(anonym.__version__)

# python -m spacy download en_core_web_sm

# %%
filepath=r'D:\DILab\PROJECTEN\INHUUR_DASHBOARD\Extern Personeel per afdeling.csv'
filepath_fake=r'D:\DILab\PROJECTEN\INHUUR_DASHBOARD\Extern Personeel per afdeling_fake.csv'
from anonym import anonym
# 'Budgethouder', 'Behoeftesteller', 'Project- afdeling', 'Type Inhuur',
#        'Financieringsbron', 'Inkoopdocument', 'Naam', 'Functie/Rol', 'uur',
#        'Team FOW', 'FOW Functie', 'FOW ID (functie)', 'Formatieplek',
#        'Startdatum', 'Einddatum', 'Mogelijke Einddatum', 'Contractduur J/M',
#        'Verlengen', 'Totaal verpl.', 'Kasrealisatie', 'Zachte kasrealisatie',
#        'Kaseffect', 'Kaseffecten\r\nVerplichtingen\r\n  T+1',

do_not_fake=['FOW Functie', 'FOW ID (functie)', 'Formatieplek', 'Contractduur J/M', 'Verlengen']
fakeit = {'Budgethouder':'PERSON',
          'Behoeftesteller': 'PERSON',
          'Project- afdeling': 'ORG',
          'Financieringsbron': 'EVENT',
          'Naam': 'PERSON',
          'Startdatum': 'DATE',
          'Einddatum': 'DATE',
          'Mogelijke Einddatum': 'DATE',
          'Mogelijke Einddatum': 'DATE',
          'Totaal verpl.': 'MONEY',
          'Kasrealisatie': 'MONEY',
          }

model = anonym(verbose='info')
df = model.import_data(filepath)
df_fake = model.anonymize(df, fakeit=fakeit, do_not_fake=do_not_fake)
model.to_csv(df_fake, filepath_fake)

# %%
filepath=r'D:\DILab\PROJECTEN\INHUUR_DASHBOARD\Extern Personeel per afdeling.csv'
filepath_fake=r'D:\DILab\PROJECTEN\INHUUR_DASHBOARD\Extern Personeel per afdeling_fake.csv'

from anonym import anonym
model = anonym(language='dutch', verbose='info')
df = model.import_data(filepath)
df_fake = model.anonymize(df)
model.to_csv(df_fake, filepath_fake)

# %%
from anonym import anonym
model = anonym()
df = model.import_example('titanic')
df_fake = model.anonymize(df)
