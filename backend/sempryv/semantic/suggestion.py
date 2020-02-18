# -*- coding: utf-8 -*-
"""Suggestion of semantic codes."""
import os
import json
import re

from sempryv.semantic.providers.bioportal import look
from sempryv.semantic.stream_classifier import StreamsClassifier
from sempryv.semantic.thryve_pulso_trainer import ThryvePulsoTrainer
from sempryv.semantic.domain_models.data_provider import SempryvDataProvider
from joblib import load
import pickle
import logging
logging.basicConfig(filename='example.log', level=logging.INFO)


# class SuggestionsProvider(object):
#     def __init__(self):

def suggest(kind, path):
    """Suggest semantic codes based on a kind and a path."""
    rules = _rules_suggestions(kind, path)
    ml_synthetic = _ml_synthetic_suggestions(kind, path)
    ml = _ml_suggestions(kind, path)
    # return rules + ml_synthetic
    return rules + ml_synthetic + ml


def _rules_suggestions(kind, path):
    """Suggest semantic codes based on rules."""
    return _calculate_rule_suggestions(kind, path, RULES, CODES)


def _ml_synthetic_suggestions(_kind, _path):
    """Suggest semantic codes based on ML."""
    # TODO: Placeholder for incorporating ML suggestions in the future
    print('Synthetics model predictions')
    model = load('sempryv/synthetics_model.joblib')
    file = open('sempryv/file_vect_synth.joblib', 'rb')
    vectorizer = pickle.load(file)
    file.close()
    new_stream = _kind + _path
    predictions = _predict_suggestions(model, vectorizer, [new_stream], model_type='synthetics')
    results = []
    for pred in predictions:
        print(pred)
        prediction_code = _parse_code(pred)
        if prediction_code is None:
            continue
        results.append(prediction_code)

    return results


def _ml_suggestions(_kind, _path):
    """Suggest semantic codes based on ML."""
    # TODO: Placeholder for incorporating ML suggestions in the future
    print('Users model predictions')
    model = load('model_users.joblib')
    file = open('file_vect_users.joblib', 'rb')
    vectorizer = pickle.load(file)
    file.close()
    new_stream = _kind + _path
    predictions = _predict_suggestions(model, vectorizer, [new_stream], model_type='users')
    results = []
    for pred in predictions:
        print(pred)
        prediction_code = _parse_code(pred)
        if prediction_code is None:
            continue
        results.append(prediction_code)

    return results


def _predict_suggestions(model, vectorizer, stream, model_type: str):
    counts = vectorizer.transform(stream)
    predicted = model.predict(counts)
    print(predicted)
    # predicted_codes = get_synthetic_codes(predicted[0])
    # predicted_codes = get_codes(predicted = predicted[0], model_type= model_type)
    code_labels = None
    if model_type == 'synthetics':
        f = open('sempryv/code_labels_synth.dict', 'rb')
        code_labels = pickle.load(f)
        f.close()
    elif model_type == 'users':
        f = open('code_labels_users.dict', 'rb')
        code_labels = pickle.load(f)
        f.close()
    print(code_labels)
    if code_labels is not None:
        for codes, label in code_labels.items():
            if label == predicted:
                return codes.split("_")[:-1]

    # return predicted_codes.split("_")[:-1]


def get_codes(predicted: int):
    f = open('sempryv/code_labels_synth.dict', 'rb')
    # f = open('code_labels_2.dict', 'rb')
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
    # users_data = [{'uname': 'orfi2019', 'token': 'cjxa7szlr00461id327owwz27'},
    #               {'uname': 'orfeas-client', 'token': 'ck1qo6fdk004j0g40juft91og'},
    #               {'uname': 'orfeas-synthetics', 'token': 'ck2g12tot00191i40w1x1h7t4'}
    #               ]
    logging.error('ml train')
    users_data = []
    data_provider = SempryvDataProvider()
    users = data_provider.get_all_users()
    for user in users:
        users_data.append({'uname': user[0], 'token': user[1]})
    sc = StreamsClassifier(users_data=users_data)
    model = sc.train()
    save_model_to_file(sc.count_vect, filename='file_vect_users.joblib')
    # db_file_vectorizer = convertToBinaryData(filename='file_vect_users.joblib') # TODO: persist in DB
    # data_provider.persist_models(file=db_file_vectorizer)
    save_model_to_file(model, filename='model_users.joblib')


def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def save_model_to_file(model, filename):
    if os.path.exists(path=filename):
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
    # with open("rules.json", "r") as file_pointer:
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
print('Train synthetic model...')
synthetics_trainer = ThryvePulsoTrainer()
synthetics_trainer.train_data()
print('Training finished.')
