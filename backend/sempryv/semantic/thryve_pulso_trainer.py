import json
import os
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


# from semantic.domain_models import sempryv_models as database


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
        # self.db = database

    @staticmethod
    def load_synthetic_data():
        # TODO: load data from DB
        f_thryve = open('semantic/synthetics/thryve-streams.json', 'r')
        f_thryve_annotations = open('semantic/synthetics/data_annotated-thryve-filtered.json', 'r')
        f_pulso = open('semantic/synthetics/pulso-streams.json', 'r')
        f_pulso_annotations = open('semantic/synthetics/data_annotated-pulso-filtered.json', 'r')
        thryve_streams = json.load(f_thryve)
        thryve_annotated_data = json.load(f_thryve_annotations)
        pulso_streams = json.load(f_pulso)
        pulso_annotated_data = json.load(f_pulso_annotations)
        f_thryve.close()
        f_thryve_annotations.close()
        return thryve_streams, thryve_annotated_data, pulso_streams, pulso_annotated_data

    def create_train_target_data(self):
        # thryve
        d_stream_types = self.get_name_types(self.thryve_streams)
        for ann_dato in self.thryve_annotated_data:
            type = d_stream_types[ann_dato['id']]
            name = ann_dato['name']
            id = ann_dato['id']
            annotations = ann_dato['codes']
            codes = ''
            for code in annotations:
                alter_name = code['prefLabel']
                name += ' ' + alter_name
                annotation = code['id'].split('/')[-1]
                ontology_name = self.ontology_names[code['id'].split('/')[-2]]
                if ontology_name == 'loinc':
                    continue
                codes += ontology_name + ':' + annotation + '_'
            if codes == '':
                continue
            label = self.assign_codes_label(codes)
            self.train_data_synthetic.append(id + ' ' + name + ' ' + type)
            self.target_data_synthetic.append(label)

        # pulso
        d_stream_types = self.get_name_types(self.pulso_streams)
        for ann_dato in self.pulso_annotated_data:
            type = d_stream_types[ann_dato['id']]
            name = ann_dato['name']
            id = ann_dato['id']
            annotations = ann_dato['codes']
            codes = ''
            for code in annotations:
                alter_name = code['prefLabel']
                name += ' ' + alter_name
                annotation = code['id'].split('/')[-1]
                ontology_name = self.ontology_names[code['id'].split('/')[-2]]
                if ontology_name == 'loinc':
                    continue
                codes += ontology_name + ':' + annotation + '_'
            if codes == '':
                continue
            label = self.assign_codes_label(codes)
            # self.train_data_synthetic.append(name + ' ' + type)
            self.train_data_synthetic.append(id + ' ' + name + ' ' + type)
            self.target_data_synthetic.append(label)

        self.save_dict_to_file(self.code_labels, 'code_labels_synth.dict')  # TODO: persist in db

    @staticmethod
    def save_dict_to_file(dict: {}, filename: str):
        f = open(filename, 'wb')
        pickle.dump(dict, f)
        f.close()

    @staticmethod
    def get_name_types(streams: []) -> dict:
        dict_types = {}
        for stream in streams:
            if stream is None:
                continue
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
        self.save_model_to_file(self.count_vect, filename='file_vect_synth.joblib')
        classifier_model = MultinomialNB().fit(counts, self.target_data_synthetic)
        self.save_model_to_file(classifier_model, filename='synthetics_model.joblib')

    def persist_model(self, model):
        filename = 'semantic/synthetics/synthetics_model.pk'
        # os.remove(filename)
        file = open(filename, 'wb')
        pickle.dump(model, file)
        # dump(model, filename)
        file.close()
        # persist in DB:
        table = self.db.ModelsTable
        conn = self.db.engine.connect()
        conn.execute('insert into ' + table.__tablename__ + '')

        rows = self.db.session.query(table.url_id, model.price_with_vat, sibyl_database.DaredevilShopPage.shop_id,
                                     model.last_spider_counter, model.category) \
            .filter(model.url_id.in_([u['url_id'] for u in url_ids])) \
            .filter(sibyl_database.DaredevilShopPage.id == model.url_id) \
            .all()
        self.db.session.remove()

    @staticmethod
    def save_model_to_file(model, filename):
        if os.path.exists(path=filename):
            os.remove(filename)
        file = open(filename, 'wb')
        pickle.dump(model, file)
        # dump(model, filename)
        file.close()
