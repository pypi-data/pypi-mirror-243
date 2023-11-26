# --------------------------------------------------
# Name        : anonym.py
# Author      : E.Taskesen
# Contact     : erdogan.taskesen@minienw.nl
# github      : https://gitlab.com/datainnovatielab/public/anonym
# Department  : Data and Innovatielab (IenW)
# Licence     : See licences
# --------------------------------------------------

import os
import re
import logging
import numpy as np
import pandas as pd
from tqdm import tqdm
import datazets as dz
from ismember import ismember
import spacy
from faker import Faker
from spacy.lang.nl.stop_words import STOP_WORDS
fake = Faker()


logger = logging.getLogger('')
[logger.removeHandler(handler) for handler in logger.handlers[:]]
console = logging.StreamHandler()
formatter = logging.Formatter('[anonym] >%(levelname)s> %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)
logger = logging.getLogger(__name__)


#%%
class anonym:
    """anonym class is used to anonymize data."""

    def __init__(self, language='dutch', verbose='info'):
        """Initialize anonym class with user-defined parameters.

        Parameters
        ----------
        language : str, optional
            'dutch': nl_core_news_sm
            'english': en_core_news_sm

        verbose : str, optional
            Level of verbosity, by default 'info'

        Examples
        --------
        >>> # Example 1
        >>> filepath=r'./names_per_department.csv'
        >>> filepath_fake=r'./names_per_department_fake.csv'
        >>> # Load library
        >>> from anonym import anonym
        >>> # Initialize
        >>> model = anonym(language='dutch', verbose='info')
        >>> # Import csv data from file
        >>> df = model.import_data(filepath, delim=';')
        >>> # Anonimyze the data set
        >>> df_fake = model.anonymize(df)
        >>> # Write to csv
        >>> model.to_csv(df_fake, filepath_fake)
        >>> #
        >>> #
        >>> # Example 2
        >>> # Load library
        >>> from anonym import anonym
        >>> # Initialize
        >>> model = anonym(language='english', verbose='info')
        >>> # Import example data set
        >>> df = model.import_example('titanic')
        >>> # Anonimyze the data set
        >>> df_fake = model.anonymize(df)

        """
        self.language = language
        # Set the logger
        set_logger(verbose=verbose)

    def import_data(self, filepath, delim=';'):
        """Reads the dataset from the given filepath.

        Parameters
        ----------
        filepath : str
            Path to the dataset file.
        delim : str, optional
            Delimiter used in the dataset file, by default ';'
        
        Examples
        --------
        >>> # Example 1
        >>> filepath=r'./names_per_department.csv'
        >>> filepath_fake=r'./names_per_department_fake.csv'
        >>> # Load library
        >>> from anonym import anonym
        >>> # Initialize
        >>> model = anonym()
        >>> # Import csv data from file
        >>> df = model.import_data(filepath, delim=';')
        >>> print(df)

        Returns
        -------
        pd.DataFrame
            Dataset read from the file.
        """
        return pd.read_csv(filepath, encoding='latin-1', delimiter=delim)

    def to_csv(self, df_fake, filepath, delim=';'):
        """Writes the DataFrame to a CSV file.

        Parameters
        ----------
        df_fake : pd.DataFrame
            DataFrame to be written to a file.
        filepath : str
            Path to the file where DataFrame will be written.
        delim : str, optional
            Delimiter to be used in the file, by default ';'
        """
        df_fake.to_csv(filepath, index=False, sep=delim)

    def anonymize(self, df, fakeit=None, do_not_fake=None, NER_blacklist = ['CARDINAL', 'GPE', 'PRODUCT', 'DATE']):
        """Anonymize the input dataframe.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame to be anonymized.
        fakeit : dict, optional
            Dictionary of column names and their fake replacements, by default None
        do_not_fake : list, optional
            List of column names that should not be faked, by default None
        NER_blacklist : list, optional
            List of named entity recognition labels to be ignored, by default ['CARDINAL', 'GPE', 'PRODUCT', 'DATE']

        Examples
        --------
        >>> # Example 1
        >>> filepath=r'./names_per_department.csv'
        >>> filepath_fake=r'./names_per_department_fake.csv'
        >>> # Load library
        >>> from anonym import anonym
        >>> # Initialize
        >>> model = anonym(language='dutch', verbose='info')
        >>> # Import csv data from file
        >>> df = model.import_data(filepath, delim=';')
        >>> # Anonimyze the data set
        >>> df_fake = model.anonymize(df)
        >>> # Write to csv
        >>> model.to_csv(df_fake, filepath_fake)

        Examples
        --------
        >>> # Example 2
        >>> # Load library
        >>> from anonym import anonym
        >>> # Initialize
        >>> model = anonym(language='english', verbose='info')
        >>> # Import example data set
        >>> df = model.import_example('titanic')
        >>> # Anonimyze the data set
        >>> df_fake = model.anonymize(df)

        Returns
        -------
        pd.DataFrame
            Anonymized DataFrame.
        """
        # Preprocessing
        # df = preprocessing(df)
        # For each column, extract all entities
        NER = extract_entities(df, fakeit=fakeit, do_not_fake=do_not_fake, NER_blacklist=NER_blacklist, language=self.language)
        # Create Fake names
        NER = generate_fake_labels(NER)
        # Replace entities with fake data
        df = replace_label_with_fake(df, NER)
        # Return
        return df

    def import_example(self, data='titanic', url=None, sep=','):
        """Import example dataset from github source.

        Import one of the few datasets from github source or specify your own download url link.

        Parameters
        ----------
        data : str
            Name of datasets: 'sprinkler', 'titanic', 'student', 'fifa', 'cancer', 'waterpump', 'retail'
        url : str
            url link to to dataset.

        Returns
        -------
        pd.DataFrame()
            Dataset containing mixed features.

        References
        ----------
            * https://github.com/erdogant/datazets

        """
        return dz.get(data=data, url=url, sep=sep)

def clean_text(text):
    """Cleans the text by removing commas, dots, special characters, and extra spaces.

    Parameters
    ----------
    text : str
        Text to be cleaned.

    Returns
    -------
    str
        Cleaned text.
    """
    # Define regex pattern to remove commas, dots, special characters, and extra spaces
    # pattern = r'[,\.\W_]+'
    pattern = r'[^\w\s]'
    # Substitute the pattern with an empty string to remove these characters
    cleaned_text = re.sub(pattern, ' ', text)
    return cleaned_text.strip()  # Strip any leading/trailing spaces

def preprocessing(df):
    """Preprocesses the DataFrame by cleaning all its columns.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to be preprocessed.

    Returns
    -------
    pd.DataFrame
        Preprocessed DataFrame.
    """
    for col in df.columns:
        # Preprocessing
        df[col] = df[col].astype(str).apply(clean_text)
    return df

def filter_for_values(df, rem_values=['nan', 'ja', 'nee', 'Ja', 'Nee', 'nvt', 'n v t', 'niet', 'Niet']):
    """Filters the DataFrame for given values.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to be filtered.
    rem_values : list, optional
        List of values to be removed from the DataFrame, by default ['nan', 'ja', 'nee', 'Ja', 'Nee', 'nvt', 'n v t', 'niet', 'Niet']

    Returns
    -------
    list
        List of filtered values.
    """
    string = ', '.join(df.astype(str))
    data_list = string.split(', ')
    filtered_values = [value for value in data_list if value not in rem_values]
    filtered_values = list(set(filtered_values))
    return filtered_values

def extract_entities(df, fakeit=None, do_not_fake=None, NER_blacklist=['CARDINAL', 'GPE', 'DATE', 'PRODUCT'], language='dutch'):
    """Extracts entities from the DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame from which entities will be extracted.
    fakeit : dict, optional
        Dictionary of column names and their fake replacements, by default None
    do_not_fake : list, optional
        List of column names that should not be faked, by default None
    NER_blacklist : list, optional
        List of named entity recognition labels to be ignored, by default ['CARDINAL', 'GPE', 'DATE', 'PRODUCT']

    Returns
    -------
    list
        List of extracted entities.
    """
    # Call the function to check and install the model if needed
    nlp = check_spacy_model(language=language)
    NER = []
    for col in df.columns:
        # Filter for values
        labels = filter_for_values(df[col])
        # Continu if text is present
        if labels is not None and len(labels)>0:
            if (fakeit is not None) and fakeit.get(col, None) is not None:
                logger.info('[%s]> Faked as [%s]' %(col, fakeit.get(col)))
                ENT = [(label, fakeit.get(col)) for label in labels]
            elif np.any(np.isin(col, do_not_fake)):
                logger.info('[%s]> Remains untouched.' %(col))
                ENT = []
            else:
                # Automatically extract 
                logger.info('[%s]> Named Entity Recognition per row.' %(col))
                ENT = extract_entities_for_string(nlp, labels, NER_blacklist)
            # Append
            if len(ENT)>0:
                NER = NER + ENT
    return NER


def extract_entities_for_string(nlp, text, NER_blacklist=None):
    """Extracts entities from the given text.

    Parameters
    ----------
    text : str
        Text from which entities will be extracted.
    NER_blacklist : list, optional
        List of named entity recognition labels to be ignored, by default None

    Returns
    -------
    list
        List of extracted entities.
    """
    if NER_blacklist is None: NER_blacklist=[]
    # Remove stop words
    text = [token for token in text if token not in STOP_WORDS]

    word = ', '.join(text)
    doc = nlp(word)
    # Extract entities from the text
    entities = list(set([(ent.text, ent.label_) for ent in doc.ents if ent.label_ not in NER_blacklist]))

    # # Extract entities per word
    # entities=[]
    # for word in text:
    #     # Lowercase the word (this will destroy the detction of some entities)
    #     # word = word.lower()
    #     # Process the word
    #     # doc = nlp(word)
    #     # Lemmatize the word
    #     # lemmatized_word = ' '.join([token.lemma_ for token in doc])
    #     # Process the lemmatized word
    #     # doc = nlp(lemmatized_word)
    #     # Process the word
    #     doc = nlp(word)
    #     # Extract entities from the text
    #     entity = list(set([(ent.text, ent.label_) for ent in doc.ents if ent.label_ not in NER_blacklist]))
    #     entities = entities + entity

    # Return
    return entities


def generate_fake_labels(NER):
    """Generates fake labels for the given entities.

    Parameters
    ----------
    NER : list
        List of entities for which fake labels will be generated.

    Returns
    -------
    pd.DataFrame
        DataFrame containing original labels and their fake replacements.
    """
    # Get the unique entities
    entities = list(set([entity[1] for entity in NER]))
    # Create Dataframe for NER
    NER = pd.DataFrame(NER, columns=['LABEL','ENTITY'])
    NER['FAKE'] = ''

    # Create fake labels
    for entity in entities:
        logger.info('[%s] is Faked' %(entity))
        store = True

        # Get all entities
        Iloc = NER.iloc[:, 1]==entity
        ui_label = NER['LABEL'].loc[Iloc].unique()

        # Determine replacement based on the entity label
        if entity == 'PERSON':
            _func = fake.name
        elif entity == 'ORG':
            _func = fake.company
        elif entity == 'DATE':
            _func = fake.date
        elif entity == 'LOC':
            _func = fake.city
        elif entity == 'MONEY':
            _func = fake.pricetag
        elif entity == 'NORP':
            _func = fake.word
        elif entity == 'ADDRESS':
            _func = fake.address
        elif entity == 'GPE':
            _func = fake.country
        elif entity == 'EVENT':
            _func = fake.catch_phrase
        elif entity == 'WORK_OF_ART':
            _func = fake.sentence
        elif entity == 'LAW':
            _func = fake.paragraph
        else:
            store = False
            logger.warning('[%s] is not Faked' %(entity))

        if store:
            fake_labels = np.array([_func() for _ in range(len(ui_label))])
            IA, idx = ismember(NER['LABEL'].values, ui_label)
            NER['FAKE'].loc[IA] = fake_labels[idx]

    # Return
    return NER


def replace_label_with_fake(df, NER):
    """Replaces original labels in the DataFrame with their fake replacements.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame in which labels will be replaced.
    NER : pd.DataFrame
        DataFrame containing original labels and their fake replacements.

    Returns
    -------
    pd.DataFrame
        DataFrame with replaced labels.
    """
    replacement_dict = dict(zip(NER['LABEL'], NER['FAKE']))
    # Replace values in input dataframe
    for col in df.columns:
        df[col] = df[col].replace(replacement_dict)
    return df

# %%
def get_logger():
    """Gets the current logger.

    Returns
    -------
    logging.Logger
        Current logger.
    """
    return logger.getEffectiveLevel()


# %%
def set_logger(verbose: [str, int] = 'info'):
    """Sets the logger for verbosity messages.

    Parameters
    ----------
    verbose : [str, int], default is 'info' or 20
        Sets the verbose messages using string or integer values.
        * [0, 60, None, 'silent', 'off', 'no']: No message.
        * [10, 'debug']: Messages from debug level and higher.
        * [20, 'info']: Messages from info level and higher.
        * [30, 'warning']: Messages from warning level and higher.
        * [50, 'critical']: Messages from critical level and higher.

    Returns
    -------
    None.

    Examples
    --------
    >>> # Set the logger to warning
    >>> set_logger(verbose='warning')
    >>> # Test with different messages
    >>> logger.debug("Hello debug")
    >>> logger.info("Hello info")
    >>> logger.warning("Hello warning")
    >>> logger.critical("Hello critical")

    """
    # Set 0 and None as no messages.
    if (verbose==0) or (verbose is None):
        verbose=60
    # Convert str to levels
    if isinstance(verbose, str):
        levels = {'silent': 60,
                  'off': 60,
                  'no': 60,
                  'debug': 10,
                  'info': 20,
                  'warning': 30,
                  'error': 50,
                  'critical': 50}
        verbose = levels[verbose]

    # Show examples
    logger.setLevel(verbose)


# %%
def disable_tqdm():
    """Disables tqdm if the logger level is higher than or equal to 30.

    Returns
    -------
    bool
        True if the logger level is higher than or equal to 30, False otherwise.
    """
    return (True if (logger.getEffectiveLevel()>=30) else False)


# %%
def check_spacy_model(language='dutch'):
    import spacy
    if language=='dutch':
        data_model = "nl_core_news_sm"
    else:
        data_model = "en_core_web_sm"

    try:
        logger.info("NLP model [%s] is loaded" %(data_model))
        # Attempt to load the 'en_core_web_sm' model
        nlp = spacy.load(data_model)
    except OSError:
        from spacy.cli import download
        # If the model is not found, download it
        logger.info("NLP model [%s] is not installed. Downloading..." %(data_model))
        download(data_model)
        logger.info("NLP model 'en_core_web_sm' has been installed.")
        # Attempt to load the 'en_core_web_sm' model
        nlp = spacy.load(data_model)
    return nlp


# %% Main
if __name__ == "__main__":
    import anonym as anonym
    df = anonym.import_example()
    out = anonym.fit(df)
    fig,ax = anonym.plot(out)
