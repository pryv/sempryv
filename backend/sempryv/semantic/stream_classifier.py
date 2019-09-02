from stream_parser import StreamParser
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


class StreamsClassifier(object):
    def __init__(self, users_data: dict):
        self.train_data = []
        self.target_data = []
        self.users_data = users_data
        self.code_labels = {}
        self.count_vect = CountVectorizer()
        self.ontolgy_names = {"SNOMEDCT": "snomed-ct", "LOINC": "loinc"}

    def create_train_data(self):
        for user in self.users_data:
            stream_parser = StreamParser(user=user['uname'], token=user['token'])
            streams = stream_parser.streams
            for stream in streams:
                stream_name = stream['name']
                sempryv_annotations = stream['clientData']['sempryv:codes']
                for ann_type in sempryv_annotations:
                    self.train_data.append(stream_name + ' ' + ann_type)
                    codes = ''
                    for annotation in sempryv_annotations[ann_type]:
                        codes += self.ontolgy_names[annotation['system_name']] + ':' + annotation['code'] + '_'
                    label = self.assign_codes_label(codes)
                    self.target_data.append(label)

    def assign_codes_label(self, codes):
        if codes in self.code_labels:
            return self.code_labels[codes]
        new_label = len(self.code_labels)
        self.code_labels[codes] = new_label
        return new_label

    def train(self):
        sc.create_train_data()
        counts = self.count_vect.fit_transform(self.train_data)
        self.classifier = MultinomialNB().fit(counts, self.target_data)

    def predict(self, stream):
        counts = self.count_vect.transform(stream)
        predicted = self.classifier.predict(counts)
        predicted_codes = self.get_codes(predicted[0])
        return predicted_codes.split("_")[:-1]

    def get_codes(self, predicted: int):
        for codes, label in self.code_labels.items():
            if label == predicted:
                return codes

users_data = [{'uname': 'orfi2019', 'token': 'cjxa7szlr00461id327owwz27'},
              {'uname': 'orfeas', 'token': 'cjzy2ioal04xj0e40zdcy4sku'}]
sc = StreamsClassifier(users_data=users_data)
# sc.create_train_data()
sc.train()
new_stream = ["ACtivity txt"]

pred = sc.predict(new_stream)
x = 1
