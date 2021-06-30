import re
from collections import defaultdict
from .annotation import IdedAnnotation


def _parse_drawing(maybe_attribute_text):
    if maybe_attribute_text:
        attributes = dict(item.strip().split(':') for item in maybe_attribute_text[0].split(','))
    else:
        attributes = {}
    return attributes


def parse_visual_conf_file(filename):
    """
    Reads simple brat visual configuration files.
    Just simple ones. No macros, defaults...
    """

    with open(filename, "rt") as r:
        text = r.read()
    return parse_visual_conf(text)


_SECTION_RE = re.compile(r'^\s*\[(.*?)\]', flags=re.MULTILINE)
def parse_visual_conf(text):
    """
    Reads simple brat visual configuration files.
    Just simple ones. No macros, defaults...
    """

    it = iter(_SECTION_RE.split(text))
    next(it)

    sections = dict((key, [
            line for line in
                (line.strip() for line in text.strip().split("\n"))
            if line and not line.startswith('#')
        ]) for key, text in zip(it, it))
    labels = {
        name.strip(): [label.strip() for label in labels]
        for name, *labels
        in (line.split('|') for line in sections.get('labels', []))
    }
    drawing = {
        name: _parse_drawing(maybe_drawing)
        for name, *maybe_drawing
        in (line.split('\t', 2) for line in sections.get('drawing', []))
    }
    entries = {
        type: {
            "labels": labels.get(type, []),
            **(drawing.get(type, {})),
        }
        for type in set(labels) | set(drawing)
    }
    return entries


_NUMBERLESS_RE = re.compile(r'(.*?)\d*$')
def _numberless(type):
    match = _NUMBERLESS_RE.match(type)
    return match.group(1)


def _add_default_class(visual_conf, types, defaults):
    return {
        type: {
            **defaults,
            **visual_conf.get(type, {})
        } for type in types
    }


def add_defaults(raw_visual_conf, doc):
    event_arc_types = defaultdict(set)
    event_types = set()
    event_ids = set()
    for ann in doc.get_events():
        event_types.add(ann.type)
        event_ids.add(ann.id)
        event_arc_types[ann.type] |= {
            _numberless(type) for type, id in ann.args
        }
    entity_types = set()
    entity_ids = set()
    for ann in doc.get_entities():
        entity_types.add(ann.type)
        entity_ids.add(ann.id)
    arc_types = {
        arc
        for event_arcs in event_arc_types.values()
        for arc in event_arcs
    }
    span_types = event_types | entity_types
    relation_types = set()
    relation_ids = set()
    for ann in (*doc.get_equivs(), *doc.get_relations()):
        relation_types.add(ann.type)
        if isinstance(ann, IdedAnnotation):
            relation_ids.add(ann.id)

    event_attribute_types = set()
    entity_attribute_types = set()
    relation_attribute_types = set()
    attribute_types = set()
    for ann in doc.get_attributes():
        attribute_types.add(ann.type)
        if ann.target in event_ids:
            event_attribute_types.add(ann.type)
        if ann.target in entity_ids:
            entity_attribute_types.add(ann.type)
        if ann.target in relation_ids:
            relation_attribute_types.add(ann.type)

    span_default = raw_visual_conf.get("SPAN_DEFAULT", {})
    arc_default = raw_visual_conf.get("ARC_DEFAULT", {})
    attribute_default = raw_visual_conf.get("ATTRIBUTE_DEFAULT", {})

    spans = _add_default_class(raw_visual_conf, span_types, span_default)
    arcs = _add_default_class(raw_visual_conf, arc_types | relation_types, arc_default)
    attributes = _add_default_class(raw_visual_conf, attribute_types, attribute_default)

    for attr_type, attr in attributes.items():
        attr["type"] = attr_type
        attr["name"] = attr["labels"][0] if attr.get("labels", False) else attr_type
    for arc_type, arc in arcs.items():
        arc["type"] = arc_type
        arc["name"] = arc["labels"][0] if arc.get("labels", False) else arc_type
    for span_type, span in spans.items():
        span["type"] = span_type
        span["name"] = span["labels"][0] if span.get("labels", False) else span_type
        span["arcs"] = [
            arcs[arc]
            for arc in event_arc_types[span_type]
            if arc in arcs
        ]


    entity_types = [spans[entity] for entity in entity_types]
    event_types = [spans[event] for event in event_types]
    relation_types = [arcs[rel] for rel in relation_types]
    event_attribute_types = [attributes[attr] for attr in event_attribute_types]
    entity_attribute_types = [attributes[attr] for attr in entity_attribute_types]
    relation_attribute_types = [attributes[attr] for attr in relation_attribute_types]

    return {
        "entity_types": entity_types,
        "event_types": event_types,
        "relation_types": relation_types,
        "event_attribute_types": event_attribute_types,
        "entity_attribute_types": entity_attribute_types,
        "relation_attribute_types": relation_attribute_types,
    }


if __name__ == "__main__":
    import sys
    raw_visual_conf = parse_visual_conf_file(sys.argv[1])
    if len(sys.argv) > 2:
        from .annotation import TextAnnotations
        doc = TextAnnotations(sys.argv[2], read_only=True)
        visual_conf = add_defaults(raw_visual_conf, doc)
        print(visual_conf)
    else:
        print(raw_visual_conf)
