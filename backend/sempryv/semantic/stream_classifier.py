import pickle
from semantic.stream_parser import StreamParser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import json


class StreamsClassifier(object):
    def __init__(self, users_data=list):
        self.train_data = []
        self.train_data_synthetic = []
        self.target_data = []
        self.target_data_synthetic = []
        self.users_data = users_data
        self.code_labels = {}
        self.ontology_names = {"SNOMEDCT": "snomed-ct", "LOINC": "loinc", "LNC": "loinc"}
        self.count_vect = CountVectorizer()
        # self.synthetics = self.load_synthetic_data()
        # self.create_train_data_from_synthetics()

    def load_synthetic_data(self):
        f_thryve = open('synthetics/thryve-streams.json', 'r')
        f_thryve_annotations = open('synthetics/data_annotated-thryve-filtered.json', 'r')
        thryve_streams = json.load(f_thryve)
        d_stream_types = self.get_name_types(thryve_streams)
        thryve_annotated_data = json.load(f_thryve_annotations)
        for ann_dato in thryve_annotated_data:
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

        f_thryve.close()
        f_thryve_annotations.close()
        x = 1

    def get_name_types(self, streams: []) -> dict:
        dict_types = {}
        for stream in streams:
            client_data = stream['clientData']
            dict_types[stream['id']] = list(client_data['sempryv:codes'].keys())[0]
        return dict_types

    def create_train_data(self):
        for user in self.users_data:
            stream_parser = StreamParser(user=user['uname'], token=user['token'])
            streams = stream_parser.streams
            for stream in streams:
                stream_name = stream['name']
                if 'clientData' not in stream:
                    continue
                if 'sempryv:codes' not in stream['clientData']:
                    continue

                sempryv_annotations = stream['clientData']['sempryv:codes']
                for ann_type in sempryv_annotations:
                    self.train_data.append(stream_name + ' ' + ann_type)
                    codes = ''
                    for annotation in sempryv_annotations[ann_type]:
                        codes += self.ontology_names[annotation['system_name']] + ':' + annotation['code'] + '_'
                    label = self.assign_codes_label(codes)
                    self.target_data.append(label)
        self.save_dict_to_file(self.code_labels)

    def create_train_data_from_synthetics(self):

        streams = []
        for stream in streams:
            stream_name = stream['name']
            if 'clientData' not in stream:
                continue
            if 'sempryv:codes' not in stream['clientData']:
                continue

            sempryv_annotations = stream['clientData']['sempryv:codes']
            for ann_type in sempryv_annotations:
                self.train_data.append(stream_name + ' ' + ann_type)
                codes = ''
                for annotation in sempryv_annotations[ann_type]:
                    codes += self.ontology_names[annotation['system_name']] + ':' + annotation['code'] + '_'
                label = self.assign_codes_label(codes)
                self.target_data.append(label)
        self.save_dict_to_file(self.code_labels)

    def save_dict_to_file(self, dict: {}):
        f = open('code_labels.dict', 'wb')
        pickle.dump(dict, f)
        f.close()

    def assign_codes_label(self, codes):
        if codes in self.code_labels:
            return self.code_labels[codes]
        new_label = len(self.code_labels)
        self.code_labels[codes] = new_label
        return new_label

    def train(self):
        self.create_train_data()
        counts = self.count_vect.fit_transform(self.train_data)
        # self.classifier_model = MultinomialNB().fit(counts, self.target_data)
        classifier_model = MultinomialNB().fit(counts, self.target_data)
        return classifier_model

    def predict_annotations(self, model, stream):
        counts = self.count_vect.transform(stream)
        predicted = model.predict(counts)
        predicted_codes = self.get_codes(predicted[0])
        return predicted_codes.split("_")[:-1]

    def get_codes(self, predicted: int):
        for codes, label in self.code_labels.items():
            if label == predicted:
                return codes


users_data = [{'uname': 'orfi2019', 'token': 'cjxa7szlr00461id327owwz27'},
              {'uname': 'orfeas', 'token': 'cjzy2ioal04xj0e40zdcy4sku'}]
sc = StreamsClassifier(users_data=users_data)
sc.load_synthetic_data()

# # sc.create_train_data()
# sc.train()
# new_stream = ["ACtivity txt"]
#
# pred = sc.predict(new_stream)
# x = 1
