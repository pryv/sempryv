import json
import requests


class StreamParser(object):
    def __init__(self, user, token):
        structure = json.loads(
            requests.get(url="https://" + user + ".pryv.me/streams", params={"auth": token}).text)
        self.streams = []
        self.extract_streams(structure['streams'])
        self.annotations = {}

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
