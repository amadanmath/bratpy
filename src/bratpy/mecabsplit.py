import MeCab
from .standoffizer import Standoffizer
from .simplesplit import find_sentence_standoffs

wakati = MeCab.Tagger("-Owakati")

def find_token_standoffs(text):
    tokens = wakati.parse(text).split()
    return list(Standoffizer(text, tokens))
