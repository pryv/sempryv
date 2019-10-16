import json, requests


class StreamParser(object):
    def __init__(self, user, token):
        # structure = json.load(file)
        structure = json.loads(
            requests.get(url="https://" + user + ".pryv.me/streams", params={"auth": token}).text)
        # self.streams = structure['streams']
        self.streams = []
        self.extract_streams(structure['streams'])
        self.annotations = {}
        # self.names = []
        # self.get_streams_names()

    def extract_streams(self, streams):
        for stream in streams:
            self.streams.append(stream)
            self.extract_children_streams(stream)

    def extract_children_streams(self, stream):
        if 'children' in stream:
            if len(stream['children']) == 0:
                return
            for children_stream in stream['children']:
                self.streams.append(children_stream)
                self.extract_children_streams(children_stream)

    def get_streams_names(self):
        for stream in self.streams:
            self.process_stream(stream)
        return self.names

    def process_stream(self, stream):
        self.names.append(stream['name'])
        if len(stream['children']) == 0:
            return True

        children_streams = stream['children']
        for stream in children_streams:
            self.process_stream(stream)
