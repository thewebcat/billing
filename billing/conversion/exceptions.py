class MissingRate(Exception):
    status_code = 400
    title = 'Bad Request'
    type = 'about:blank'

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['detail'] = self.message
        rv['status'] = self.status_code
        rv['title'] = self.title
        rv['type'] = self.type
        return rv


class ImproperlyConfigured(Exception): pass # NOQA
