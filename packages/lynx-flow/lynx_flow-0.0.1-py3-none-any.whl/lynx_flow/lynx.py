import requests
from logstyle.base import CustomLog

log = CustomLog("Lynx Flow")


class _BaseMethod:
    def __init__(self):
        self.method = None

    def post(self):
        self.method = 'POST'
        log.title_log("HTTP Method definition", f"{self.method} has been used", log.COLOR_BLUE)
        return self

    def get(self):
        self.method = 'GET'
        log.title_log("HTTP Method definition", f"{self.method} has been used", log.COLOR_BLUE)
        return self

    def put(self):
        log.title_log("HTTP Method definition", f"{self.method} has been used", log.COLOR_BLUE)
        self.method = 'PUT'

    def patch(self):
        log.title_log("HTTP Method definition", f"{self.method} has been used", log.COLOR_BLUE)
        self.method = 'PATCH'

    def delete(self):
        log.title_log("HTTP Method definition", f"{self.method} has been used", log.COLOR_BLUE)
        self.method = 'DELETE'


class _With(_BaseMethod):
    def __init__(self):
        super(_With, self).__init__()
        self.url = None
        self.body = None
        self.headers = None

    def with_url(self, url):
        self.url = url
        return self

    def with_headers(self, headers):
        self.headers = headers
        return self

    def with_body(self, body):
        self.body = body
        return self


class _ToBe(_With):
    def __init__(self):
        super(_ToBe, self).__init__()
        self.response = None

    def where(self):
        self.response = requests.request(self.method, self.url, headers=self.headers, json=self.body)
        return self

    def json(self):
        return self

    def tobe(self):
        return self

    def equal(self, expected):
        expected_value = expected
        actual_value = self.response.json()
        assert actual_value == expected_value, f"Expected: {expected_value}, but actual value is: {actual_value}"

    def not_equal(self, expected):
        expected_value = expected
        actual_value = self.response.json()
        assert actual_value != expected_value, f"Expected not equal to: {expected_value}, but actual value is: " \
                                               f"{actual_value}"

    def contains(self, target_value):
        main_value = self.response.json()
        assert target_value in main_value, f"Expected {target_value} to be in {main_value}"


class Lynx(_ToBe):
    def __init__(self):
        super(Lynx, self).__init__()
