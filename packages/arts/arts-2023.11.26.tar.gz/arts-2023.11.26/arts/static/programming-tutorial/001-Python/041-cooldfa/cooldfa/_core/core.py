from json import loads
from pathlib import Path


# 内置敏感词
words_dir = Path(__file__).parent / 'words'

class PwType(type):
    def __getattr__(cls, name):
        words = loads((words_dir / f'{name}.json').read_text('utf8'))
        setattr(cls, name, words)
        return words

class preset_words(object, metaclass=PwType):
    politics: list
    sex: list
    violence: list
    url: list
    others: list