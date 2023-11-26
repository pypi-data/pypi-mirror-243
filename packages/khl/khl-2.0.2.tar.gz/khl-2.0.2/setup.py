# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['khl']

package_data = \
{'': ['*']}

install_requires = \
['natasha==1.4.0']

setup_kwargs = {
    'name': 'khl',
    'version': '2.0.2',
    'description': 'Preparing russian hockey news for machine learning',
    'long_description': '![Khl Logo](https://raw.githubusercontent.com/Rishat-F/khl/master/data/logo.png)\n\n<h1 align="center">No Water - Ice Only</h1>\n\nPreparing russian hockey news for machine learning.\n\n**Unify -> Simplify -> Preprocess** text and feed your neural model.\n\n## Installation\n\n*Khl* is available on PyPI:\n\n```console\n$ pip install khl\n```\nIt requires Python 3.8+ to run.\n\n## Usage\n\nTo get started right away with basic usage:\n\n```python\nfrom khl import text_to_codes\n\ncoder = {\n    \'\': 0,     # placeholder\n    \'???\': 1,  # unknown\n    \'.\': 2,\n    \'и\': 3,\n    \'в\': 4,\n    \'-\': 5,\n    \':\': 6,\n    \'матч\': 7,\n    \'за\': 8,\n    \'забить\': 9,\n    \'гол\': 10,\n    \'per\': 11,   # person entity\n    \'org\': 12,   # organization entity\n    \'loc\': 13,   # location entity\n    \'date\': 14,  # date entity\n    \'против\': 15,\n    \'год\': 16,\n    \'pers\': 17,  # few persons entity\n    \'orgs\': 18,  # few organizations entity\n    \'свой\': 19\n}\n\ntext = """\n    1 апреля 2023 года в Москве в матче ⅛ финала против „Спартака” Иван Иванов забил свой 100—й гол за карьеру.\n    «Динамо Мск» - «Спартак» 2:1 ОТ (1:0 0:1 0:0 1:0) Голы забили: Иванов, Петров и Сидоров.\n"""\n\ncodes = text_to_codes(\n    text=text,\n    coder=coder,\n    stop_words_=["за", "и", "свой"],  # stop words to drop\n    replace_ners_=True,               # replace named entities ("Иван Иванов" -> "per", "Спартак" -> "org", "Москва" -> "loc")\n    replace_dates_=True,              # replace dates ("1 апреля 2023 года" -> "date")\n    replace_penalties_=True,          # replace penalties ("5+20" -> "pen")\n    exclude_unknown=True,             # drop lemma that not presented in coder\n    max_len=20,                       # get sequence of codes of length 20\n)\n# codes = [0, 0, 0, 14, 4, 13, 4, 7, 15, 12, 11, 9, 10, 2, 18, 10, 9, 6, 17, 2]\n```\n\n```text_to_codes``` is a very high level function. What\'s happens under hood see in [Lower level usage](#lower-level-usage).\n\n## What is `coder`?\n`coder` is just a dictionary where each lemma is represented with unique integer code.\nNote that first two elements are reserved for *placeholder* and *unknown* elements.\n\nIt is possible to get `coder` from frequency dictionary file (see in [Get lemmas coder](#2-get-lemmas-coder)).\nFrequency dictionary file is a **json**-file with dictionary where key is lemma and value is how many times this lemma occurred in your whole dataset.\nPreferably it should be sorted in descending order of values.  \n`example_frequency_dictionary.json`:\n\n```json\n{\n  ".": 1000,\n  "и": 500,\n  "в": 400,\n  "-": 300,\n  ":": 300,\n  "матч": 290,\n  "за": 250,\n  "забить": 240,\n  "гол": 230,\n  "per": 200,\n  "org": 150,\n  "loc": 150,\n  "date": 100,\n  "против": 90,\n  "год": 70,\n  "pers": 40,\n  "orgs": 30,\n  "свой": 20\n}\n```\n\nYou could make and use your own frequency dictionary or download [this dictionary](https://github.com/Rishat-F/khl/blob/master/data/frequency_dictionary.json) created by myself.\n\n## Lower level usage<a id="lower-level-usage"></a>\n\n#### 1. Make imports\n```python\nfrom khl import stop_words\nfrom khl import utils\nfrom khl import preprocess\n```\n\n#### 2. Get lemmas coder<a id="2-get-lemmas-coder"></a>\n```python\ncoder = preprocess.get_coder("example_frequency_dictionary.json")\n```\n\n#### 3. Define text\n```python\ntext = """\n    1 апреля 2023 года в Москве в матче ⅛ финала против „Спартака” Иван Иванов забил свой 100—й гол за карьеру.\n    «Динамо Мск» - «Спартак» 2:1 ОТ (1:0 0:1 0:0 1:0) Голы забили: Иванов, Петров и Сидоров.\n"""\n```\n\n#### 4. Unify\n```python\nunified_text = utils.unify(text)\n# "1 апреля 2023 года в Москве в матче 1/8 финала против \'Спартака\' Иван Иванов забил свой 100-й гол за карьеру. \'Динамо Мск\' - \'Спартак\' 2:1 ОТ (1:0 0:1 0:0 1:0) Голы забили: Иванов, Петров и Сидоров."\n```\n\n#### 5. Simplify\n```python\nsimplified_text = utils.simplify(\n    text=unified_text,\n    replace_ners_=True,\n    replace_dates_=True,\n    replace_penalties_=True,\n)\n# \'date в loc в матче финала против org per забил свой гол за карьеру. org org Голы забили: per per per.\'\n```\n\n#### 6. Lemmatize\n```python\nlemmas = preprocess.lemmatize(text=simplified_text, stop_words_=stop_words)\n# [\'date\', \'в\', \'loc\', \'в\', \'матч\', \'финал\', \'против\', \'org\', \'per\', \'забить\', \'гол\', \'карьера\', \'.\', \'orgs\', \'гол\', \'забить\', \':\', \'pers\', \'.\']\n```\n\n#### 7. Transform to codes\n```python\ncodes = preprocess.lemmas_to_codes(\n    lemmas=lemmas,\n    coder=coder,\n    exclude_unknown=True,\n    max_len=20,\n)\n# [0, 0, 0, 14, 4, 13, 4, 7, 15, 12, 11, 9, 10, 2, 18, 10, 9, 6, 17, 2]\n```\n\n#### 8. Transform to lemmas back (just to look which lemmas are presented in codes sequence)\n```python\nprint(\n    preprocess.codes_to_lemmas(codes=codes, coder=coder)\n)\n# [\'\', \'\', \'\', \'date\', \'в\', \'loc\', \'в\', \'матч\', \'против\', \'org\', \'per\', \'забить\', \'гол\', \'.\', \'orgs\', \'гол\', \'забить\', \':\', \'pers\', \'.\']\n```\n',
    'author': 'Rishat Fayzullin',
    'author_email': 'nilluziaf@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Rishat-F/khl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
