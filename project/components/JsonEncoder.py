from json import JSONEncoder


class JsonEncoder(JSONEncoder):
    def default(self, data):
        return data.__dict__
