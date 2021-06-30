def _translate(offset, text, modifier):
    orig_frag = text[:offset]
    mod_frag = modifier(orig_frag)
    return len(mod_frag)


def modify_annotations(doc, modifier):
    text = doc._document_text
    for ann in doc.get_textbounds():
        new_spans = []
        for start, end in ann.spans:
            start = _translate(start, text, modifier)
            end = _translate(end, text, modifier)
            new_spans.append((start, end))
        ann.spans = new_spans
    doc._document_text = modifier(text)
