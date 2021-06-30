from .simplesplit import find_sentence_standoffs, find_token_standoffs



def get_doc_json(doc, sentence_standoffs=None, token_standoffs=None, norm_urls=None):
    text = doc.get_document_text()

    if sentence_standoffs is None:
        sentence_standoffs = find_sentence_standoffs(text)
    if token_standoffs is None:
        token_standoffs = find_token_standoffs(text)

    entity_doc_data = [
        [ann.id, ann.type, ann.spans]
        for ann in doc.get_entities()
    ]
    normalization_doc_data = [
        [ann.id, ann.type, ann.target, ann.refdb, ann.refid, ann.tail]
        for ann in doc.get_normalizations()
    ]
    event_doc_data = [
        [ann.id, ann.trigger, ann.args]
        for ann in doc.get_events()
    ]
    trigger_doc_data = [
        [ann.id, ann.type, ann.spans]
        for ann in doc.get_triggers()
    ]
    relation_doc_data = [
        [ann.id, ann.type,
            [(ann.arg1l, ann.arg1),
            (ann.arg2l, ann.arg2)]]
        for ann in doc.get_relations()
    ]
    attribute_doc_data = [
        [ann.id, ann.type, ann.target, ann.value]
        for ann in doc.get_attributes()
    ]
    comment_doc_data = [
        [ann.target, ann.type, ann.tail]
        for ann in doc.get_oneline_comments()
    ]
    doc_data = {
        "entities": entity_doc_data,
        "events": event_doc_data,
        "relations": relation_doc_data,
        "triggers": trigger_doc_data,
        "modifications": [],
        "attributes": attribute_doc_data,
        "equivs": [],
        "normalizations": normalization_doc_data,
        "comments": comment_doc_data,
        "norm_urls": norm_urls or {},
        "text": text,
        "annfile": str(doc),
        "token_offsets": token_standoffs,
        "sentence_offsets": sentence_standoffs,
        # "mtime": 1533538148.3611436,
        # "ctime": 1585644597.360524,
        # "source_files": [
        #     "ann",
        #     "txt"
        # ],
        # "action": "getDocument",
        # "protocol": 1,
        # "messages": []
    }

    return doc_data


def get_coll_json(visual_conf):
    norm_coll_data = [
        # [
        #     "UMLS",
        #     "https://www.nlm.nih.gov/research/umls/",
        #     "https://uts.nlm.nih.gov//metathesaurus.html?cui=%s",
        #     None,
        #     True
        # ]
    ]
    # event_coll_data = [
    #     # {
    #     #     "name": "Catalysis",
    #     #     "type": "Catalysis",
    #     #     "unused": False,
    #     #     "labels": [
    #     #         "Catalysis",
    #     #     ],
    #     #     "attributes": [
    #     #     ],
    #     #     "normalizations": [],
    #     #     "fgColor": "black",
    #     #     "bgColor": "#e0ff00",
    #     #     "borderColor": "darken",
    #     #     # "hotkey": "C",
    #     #     "arcs": [
    #     #         {
    #     #             "type": "Theme",
    #     #             "labels": [
    #     #                 "Theme",
    #     #                 "Th"
    #     #             ],
    #     #             "hotkey": "T",
    #     #             "color": "black",
    #     #             "arrowHead": "triangle,5",
    #     #             "targets": [
    #     #                 "Catalysis",
    #     #                 "DNA_methylation",
    #     #                 "DNA_demethylation",
    #     #                 "Acetylation",
    #     #                 "Methylation",
    #     #                 "Glycosylation",
    #     #                 "Hydroxylation",
    #     #                 "Phosphorylation",
    #     #                 "Ubiquitination",
    #     #                 "Deacetylation",
    #     #                 "Demethylation",
    #     #                 "Deglycosylation",
    #     #                 "Dehydroxylation",
    #     #                 "Dephosphorylation",
    #     #                 "Deubiquitination"
    #     #             ]
    #     #         },
    #     #         {
    #     #             "type": "Cause",
    #     #             "labels": [
    #     #                 "Cause",
    #     #                 "Ca"
    #     #             ],
    #     #             "color": "#007700",
    #     #             "arrowHead": "triangle,5",
    #     #             "targets": [
    #     #                 "Protein"
    #     #             ]
    #     #         }
    #     #     ],
    #     #     "children": []
    #     # }
    # ]
    # entity_coll_data = [
    #     {
    #         "name": tag,
    #         "type": tag,
    #         "unused": False,
    #         "labels": description.get("labels", [tag]),
    #         "attributes": [],
    #         "normalizations": [],
    #         "fgColor": description.get("fgColor", "black"),
    #         "bgColor": description.get("bgColor", "white"),
    #         "borderColor": description.get("borderColor", "darken"),
    #         # "hotkey": "A-C-S-T",
    #         "arcs": [
    #             {
    #                 "type": "Equiv",
    #                 "labels": [
    #                     "Equiv",
    #                     "Eq"
    #                 ],
    #                 "color": "black",
    #                 "dashArray": "3,3",
    #                 "arrowHead": "none",
    #                 "targets": [
    #                     "Protein"
    #                 ]
    #             }
    #             for arc in description["arcs"]
    #         ],
    #         "children": []
    #     }
    #     for tag, description in visual_conf.items()
    # ]
    # rel_coll_data = [
    #     # {
    #     #     "name": "Equiv",
    #     #     "type": "Equiv",
    #     #     "unused": False,
    #     #     "labels": [
    #     #         "Equiv",
    #     #         "Eq"
    #     #     ],
    #     #     "attributes": [],
    #     #     "properties": {
    #     #         "symmetric": True,
    #     #         "transitive": True
    #     #     },
    #     #     "color": "black",
    #     #     "dashArray": "3,3",
    #     #     "arrowHead": "none",
    #     #     "args": [
    #     #         {
    #     #             "role": "Arg1",
    #     #             "targets": [
    #     #                 "Protein"
    #     #             ]
    #     #         },
    #     #         {
    #     #             "role": "Arg2",
    #     #             "targets": [
    #     #                 "Protein"
    #     #             ]
    #     #         }
    #     #     ],
    #     #     "children": []
    #     # },
    #     # {
    #     #     "name": "Equiv",
    #     #     "type": "Equiv",
    #     #     "unused": False,
    #     #     "labels": [
    #     #         "Equiv",
    #     #         "Eq"
    #     #     ],
    #     #     "attributes": [],
    #     #     "properties": {
    #     #         "symmetric": True,
    #     #         "transitive": True
    #     #     },
    #     #     "color": "black",
    #     #     "dashArray": "3,3",
    #     #     "arrowHead": "none",
    #     #     "args": [
    #     #         {
    #     #             "role": "Arg1",
    #     #             "targets": [
    #     #                 "Entity"
    #     #             ]
    #     #         },
    #     #         {
    #     #             "role": "Arg2",
    #     #             "targets": [
    #     #                 "Entity"
    #     #             ]
    #     #         }
    #     #     ],
    #     #     "children": []
    #     # }
    # ]
    # event_attr_coll_data = [
    #     # {
    #     #     "name": "Negation",
    #     #     "type": "Negation",
    #     #     "unused": False,
    #     #     "labels": None,
    #     #     "values": [
    #     #         {
    #     #             "name": "Negation",
    #     #             "box": "crossed"
    #     #         }
    #     #     ]
    #     # },
    #     # {
    #     #     "name": "Speculation",
    #     #     "type": "Speculation",
    #     #     "unused": False,
    #     #     "labels": None,
    #     #     "values": [
    #     #         {
    #     #             "name": "Speculation",
    #     #             "dashArray": "3,3"
    #     #         }
    #     #     ]
    #     # }
    # ]
    unconf_coll_data = [
        # {
        #     "name": "Person",
        #     "type": "Person",
        #     "unused": True,
        #     "labels": [
        #         "Person"
        #     ],
        #     "fgColor": "black",
        #     "bgColor": "#ffccaa",
        #     "borderColor": "darken",
        #     "color": "black",
        #     "arrowHead": "triangle,5"
        # }
    ]
    coll_data = {
        # "items": [],
        # "header": [],
        # "parent": "T_2011",
        # "messages": [],
        # "description": "",
        # "search_config": [],
        # "disambiguator_config": [],
        # "normalization_config": norm_coll_data,
        # "annotation_logging": False,
        # "ner_taggers": [],

        # "event_types": event_coll_data,
        # "entity_types": entity_coll_data,
        # "relation_types": rel_coll_data,
        # "event_attribute_types": event_attr_coll_data,
        # "relation_attribute_types": [],
        # "entity_attribute_types": [],
        # "unconfigured_types": unconf_coll_data,

        "ui_names": {
            "entities": "entities",
            "relations": "relations",
            "events": "events",
            "attributes": "attributes"
        },
        "visual_options": {
            "arc_bundle": "all",
            "text_direction": "ltr"
        },
        # "action": "getCollectionInformation",
        # "protocol": 1

        **visual_conf,
    }

    return coll_data
