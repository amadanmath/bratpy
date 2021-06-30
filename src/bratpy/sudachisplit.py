from sudachipy import dictionary, tokenizer
from .standoffizer import Standoffizer
from .simplesplit import find_sentence_standoffs

sudachi_tokenizer = dictionary.Dictionary().create()

def find_token_standoffs(text, mode=tokenizer.Tokenizer.SplitMode.A, whitespace=False):
    tokens = [m.surface() for m in sudachi_tokenizer.tokenize(text, mode)]
    if not whitespace:
        tokens = [t for t in tokens if not t.isspace()]
    return list(Standoffizer(text, tokens))
