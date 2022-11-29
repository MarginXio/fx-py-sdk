import ujson as json


class FxdexRequestException(Exception):
    pass


class FxdexRPCException(Exception):
    def __init__(self, response):
        self.code = 0
        try:
            json_res = json.loads(response.content)
        except ValueError:
            self.message = 'Invalid JSON error message from Chain: {}'.format(
                response.text)
        else:
            self.code = json_res['error']['code']
            self.message = json_res['error']['message']
        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return f'RPCError(code={self.code}): {self.message}'
