import json
import os
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


class ThryvePulsoTrainer(object):
    def __init__(self):
        self.train_data_synthetic = []
        self.target_data_synthetic = []
        self.ontology_names = {"SNOMEDCT": "snomed-ct", "LOINC": "loinc", "LNC": "loinc"}
        self.thryve_streams, self.thryve_annotated_data, self.pulso_streams, self.pulso_annotated_data = \
            self.load_synthetic_data()
        self.code_labels = {}
        self.create_train_target_data()
        self.count_vect = CountVectorizer()

    @staticmethod
    def load_synthetic_data():
        #TODO: load data from DB
        f_thryve = open('synthetics/thryve-streams.json', 'r')
        f_thryve_annotations = open('synthetics/data_annotated-thryve-filtered.json', 'r')
        f_pulso = open('synthetics/pulso-streams.json', 'r')
        f_pulso_annotations = open('synthetics/data_annotated-pulso-filtered.json', 'r')
        thryve_streams = json.load(f_thryve)
        thryve_annotated_data = json.load(f_thryve_annotations)
        pulso_streams = json.load(f_pulso)
        pulso_annotated_data = json.load(f_pulso_annotations)
        f_thryve.close()
        f_thryve_annotations.close()
        return thryve_streams, thryve_annotated_data, pulso_streams, pulso_annotated_data

    def create_train_target_data(self):
        d_stream_types = self.get_name_types(self.thryve_streams)
        for ann_dato in self.thryve_annotated_data:
            type = d_stream_types[ann_dato['id']]
            name = ann_dato['name']
            annotations = ann_dato['codes']
            self.train_data_synthetic.append(name + ' ' + type)
            codes = ''
            for code in annotations:
                annotation = code['id'].split('/')[-1]
                ontology_name = self.ontology_names[code['id'].split('/')[-2]]
                codes += ontology_name + ':' + annotation + '_'
            label = self.assign_codes_label(codes)
            self.target_data_synthetic.append(label)

    @staticmethod
    def get_name_types(streams: []) -> dict:
        dict_types = {}
        for stream in streams:
            client_data = stream['clientData']
            dict_types[stream['id']] = list(client_data['sempryv:codes'].keys())[0]
        return dict_types

    def assign_codes_label(self, codes):
        if codes in self.code_labels:
            return self.code_labels[codes]
        new_label = len(self.code_labels)
        self.code_labels[codes] = new_label
        return new_label

    def train_data(self):
        counts = self.count_vect.fit_transform(self.train_data_synthetic)
        classifier_model = MultinomialNB().fit(counts, self.target_data_synthetic)
        self.persist_model(classifier_model)

    @staticmethod
    def persist_model(model):
        filename = 'synthetics_model'
        os.remove(filename)
        file = open(filename, 'wb')
        pickle.dump(model, file)
        # dump(model, filename)
        file.close()
