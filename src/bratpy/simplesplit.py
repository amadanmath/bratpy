import re
from brat.ssplit import regex_sentence_boundary_gen



def find_sentence_standoffs(text):
    return list(regex_sentence_boundary_gen(text))


NONSPACE_RE = re.compile(r'\S+')
def find_token_standoffs(text, pattern=NONSPACE_RE):
    # simple whitespace tokenizer is good enough as default
    return [
        (match.start(), match.end())
        for match in pattern.finditer(text)
    ]
