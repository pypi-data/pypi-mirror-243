# anonym

[![Python](https://img.shields.io/pypi/pyversions/anonym)](https://img.shields.io/pypi/pyversions/anonym)
[![Pypi](https://img.shields.io/pypi/v/anonym)](https://pypi.org/project/anonym/)
[![Docs](https://img.shields.io/badge/Sphinx-Docs-Green)](https://gitlab.com/datainnovatielab/public/anonym)
[![LOC](https://sloc.xyz/datainnovatielab/public/anonym/?category=code)](https://gitlab.com/datainnovatielab/anonym/)
[![Downloads](https://static.pepy.tech/personalized-badge/anonym?period=month&units=international_system&left_color=grey&right_color=brightgreen&left_text=PyPI%20downloads/month)](https://pepy.tech/project/anonym)
[![Downloads](https://static.pepy.tech/personalized-badge/anonym?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/anonym)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://gitlab.com/datainnovatielab/anonym/blob/master/LICENSE)
[![Forks](https://img.shields.io/gitlab/forks/datainnovatielab/anonym.svg)](https://gitlab.com/datainnovatielab/anonym/network)
[![Issues](https://imSg.shields.io/gitlab/issues/datainnovatielab/anonym.svg)](https://gitlab.com/datainnovatielab/anonym/issues)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Colab](https://colab.research.google.com/assets/colab-badge.svg?logo=gitlab%20sponsors)](https://gitlab.com/datainnovatielab/public/anonympages/html/Documentation.html#colab-notebook)
![gitlab Repo stars](https://img.shields.io/gitlab/stars/datainnovatielab/anonym)
![gitlab repo size](https://img.shields.io/gitlab/repo-size/datainnovatielab/anonym)


* The ``anonym`` library is designed to anonymize sensitive data in Python, allowing users to work with, share, or publish their data without compromising privacy or violating data protection regulations. It uses Named Entity Recognition (NER) from ``spacy`` to identify sensitive information in the data. Once identified, the library leverages the ``faker`` library to generate fake but realistic replacements. Depending on the type of sensitive information (like names, addresses, dates), corresponding faker methods are used, ensuring the anonymized data maintains a similar structure and format to the original, making it suitable for further data analysis or testing.


# 
**Star this repo if you like it! ⭐️**
#


## Blog/Documentation

* [**anonym documentation pages (Sphinx)**](https://gitlab.com/datainnovatielab/public/anonym)


### Contents
- [Installation](#-installation)
- [Contribute](#-contribute)
- [Citation](#-citation)
- [Maintainers](#-maintainers)
- [License](#-copyright)

### Installation
* Install anonym from PyPI (recommended). anonym is compatible with Python 3.6+ and runs on Linux, MacOS X and Windows. 
* A new environment can be created as following:

```bash
conda create -n env_anonym python=3.10
conda activate env_anonym
```

```bash
pip install anonym            # normal install
pip install --upgrade anonym # or update if needed
```

* Alternatively, you can install from the GitHub source:
```bash
# Directly install from github source
pip install -e git://gitlab.com/datainnovatielab/public/anonym.git@0.1.0#egg=master
pip install git+https://gitlab.com/datainnovatielab/public/anonym#egg=master
pip install git+https://gitlab.com/datainnovatielab/public/anonym

# By cloning
git clone https://gitlab.com/datainnovatielab/public/anonym.git
cd anonym
pip install -U .
```  

#### Import anonym package
```python
import anonym as anonym
```

#### Example:
```python
  # Example 2
  # Load library
  from anonym import anonym
  # Initialize
  model = anonym(language='english', verbose='info')
  # Import example data set
  df = model.import_example('titanic')
  # Anonimyze the data set
  df_fake = model.anonymize(df)
```


#### References
* https://gitlab.com/datainnovatielab/public/anonym

#### Citation
Please cite in your publications if this is useful for your research (see citation).
   
### Contribute
* All kinds of contributions are welcome!

### Licence
See [LICENSE](LICENSE) for details.
