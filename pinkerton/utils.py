import regex as re
import pymorphy2
import unicodedata
import b_labs_models as models


morph = pymorphy2.MorphAnalyzer()
tokenizer = models.Tokenizer()


def remove_unnecessary_chars(string):
    '''
    Removes some characters, like accent diacritics
    '''
    source = unicodedata.normalize('NFD', string)
    result = ''.join(
        c for c in source if c not in {'´', '́'}
    )
    return unicodedata.normalize('NFC', result)


def normalize(tokens, analyzer=morph):
    '''
    Replaces tokens with its first normal form returned by pymorphy2
    '''

    def get_normal_form(token):
        forms = morph.parse(token)
        return forms[0].normal_form

    return (get_normal_form(t) for t in tokens)


def tokenize(text):
    tokens = tokenizer.tokenize(text)
    tokens = (token for token in tokens if len(token) >= 3)
    tokens = (
        remove_unnecessary_chars(token.lower()) for token in tokens
    )
    return list(
        normalize(tokens)
    )


def serialize_object(obj):
    obj['type'] = obj['type'].value
    return obj
