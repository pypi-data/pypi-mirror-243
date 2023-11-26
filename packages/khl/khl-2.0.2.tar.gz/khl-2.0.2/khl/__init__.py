"""Подготовка русскоязычных текстов хоккейных новостей для обучения нейронных сетей."""

__version__ = "2.0.2"

from typing import Dict, List, Optional

from khl import preprocess, utils
from khl.stop_words import stop_words


def text_to_codes(
    text: str,
    coder: Dict[preprocess.Lemma, preprocess.Code],
    stop_words_: Optional[List[preprocess.Lemma]] = stop_words,
    replace_ners_: bool = True,
    replace_dates_: bool = True,
    replace_penalties_: bool = True,
    exclude_unknown: bool = True,
    max_len: Optional[int] = None,
) -> List[preprocess.Code]:
    """
    Преобразует текст в последовательность кодов.

    args:
      text: текст новости
      coder: словарь, в котором каждая лемма однозначно
        идентифицируется со своим целочисленным кодом
      stop_words_: стоп-слова для исключения
      replace_ners_: если True, то в тексте имена людей заменяются на
        слово 'per', названия команд заменяются на слово 'org',
        названия городов заменяются на слово 'loc'
      replace_dates_: если True, то в тексте даты заменяются на слово 'date'
      replace_penalties_: если True, то в тексте удаления вида '2+10'
        заменяются на слово 'pen'
      exclude_unknown: если True, то слова, которых нет в частотном словаре,
        отбрасываются; если False, то слова, которых нет в частотном словаре,
        заменяются на код неизвестного слова
      max_len: длина последовательности на выходе
    """
    text = utils.unify(text)
    text = utils.simplify(text, replace_ners_, replace_dates_, replace_penalties_)
    lemmas = preprocess.lemmatize(text, stop_words_)
    codes = preprocess.lemmas_to_codes(lemmas, coder, exclude_unknown, max_len)
    return codes
