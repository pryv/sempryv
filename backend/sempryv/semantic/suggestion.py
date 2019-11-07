# -*- coding: utf-8 -*-
"""Suggestion of semantic codes."""
import os
import json
import re

from sempryv.semantic.providers.bioportal import look
from semantic.stream_classifier import StreamsClassifier
from semantic.thryve_pulso_trainer import ThryvePulsoTrainer
from joblib import dump, load
from sklearn.feature_extraction.text import CountVectorizer
import pickle


# class SuggestionsProvider(object):
#     def __init__(self):

def suggest(kind, path):
    """Suggest semantic codes based on a kind and a path."""
    rules = _rules_suggestions(kind, path)
    ml = _ml_suggestions(kind, path)
    return rules + ml


def _rules_suggestions(kind, path):
    """Suggest semantic codes based on rules."""
    return _calculate_rule_suggestions(kind, path, RULES, CODES)


def _ml_suggestions(_kind, _path):
    """Suggest semantic codes based on ML."""
    # TODO: Placeholder for incorporating ML suggestions in the future
    model = load('model.joblib')
    new_stream = _kind + _path
    predictions = _predict_suggestions(model, [new_stream])
    results = []
    for pred in predictions:
        results.append(_parse_code(pred))

    return results


def _predict_suggestions(model, stream):
    # vectorizer = load('file_vect.joblib')
    file = open('file_vect.joblib', 'rb')
    vectorizer = pickle.load(file)
    file.close()
    # vector = CountVectorizer(vocabulary=vector.vocabulary)

    counts = vectorizer.transform(stream)
    predicted = model.predict(counts)
    print(predicted)
    predicted_codes = get_codes(predicted[0])
    return predicted_codes.split("_")[:-1]


def get_codes(predicted: int):
    f = open('code_labels.dict', 'rb')
    code_labels = pickle.load(f)
    print(code_labels)
    for codes, label in code_labels.items():
        if label == predicted:
            return codes


def _calculate_rule_suggestions(kind, path, rules, codes):
    """Find the codes from the rules that are matching path and kind."""
    matchings = []
    for rule in rules.values():
        if "pryv:pathExpression" in rule and re.fullmatch(
                rule["pryv:pathExpression"].lower(), path.lower()
        ):
            matchings += rule["pryv:mapping"]
    results = []
    for matching in matchings:
        rule = rules[matching]
        for notation in rule["skos:notation"]:
            if notation.lower() == kind.lower():
                for matchtype in ["skos:closeMatch", "skos:broadMatch"]:
                    if matchtype in rule and rule[matchtype] in codes:
                        results.append(codes[rule[matchtype]])
    return results


def sempryv_ml_train():
    users_data = [{'uname': 'orfi2019', 'token': 'cjxa7szlr00461id327owwz27'},
                  {'uname': 'orfeas', 'token': 'cjzy2ioal04xj0e40zdcy4sku'},
                  {'uname': 'orfeas-synthetics', 'token': 'ck2g12tot00191i40w1x1h7t4'}
                  ]
    sc = StreamsClassifier(users_data=users_data)
    model = sc.train()
    # counts = sc.count_vect.transform(['/Disorders'])
    # model.predict(counts)
    save_model_to_file(sc.count_vect, filename='file_vect.joblib')
    save_model_to_file(model, filename='model.joblib')


def save_model_to_file(model, filename):
    os.remove(filename)
    file = open(filename, 'wb')
    pickle.dump(model, file)
    # dump(model, filename)
    file.close()


def _load_rules():
    """Load the rules."""
    print('===================== LOAD RULES =====================\n')
    rules = {}
    codes = {}
    # Open the file
    with open("../rules.json", "r") as file_pointer:
        entries = json.load(file_pointer)["@graph"]
    # For each entry
    for entry in entries:
        # If it is a type entry, load its codes
        if "@type" in entry and entry["@type"] == "skos:Concept":
            rules[entry["@id"]] = entry
            for matchtype in ["skos:closeMatch", "skos:broadMatch"]:
                if matchtype not in entry:
                    continue
                code_str = entry[matchtype]
                code = _parse_code(code_str)
                if code:
                    codes[code_str] = code
        # If it is a path entry just copy it
        elif "pryv:mapping" in entry:
            rules[entry["@id"]] = entry
    return rules, codes


def _parse_code(code_str):
    """Return the code object of a given text code input."""
    ontology, code = code_str.split(":", maxsplit=1)
    ontology = {"snomed-ct": "SNOMEDCT", "loinc": "LOINC"}[ontology]
    return look(ontology, code)


RULES, CODES = _load_rules()
synthetics_trainer = ThryvePulsoTrainer()
synthetics_trainer.train_data()