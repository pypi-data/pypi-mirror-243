import urllib3
from urllib3.exceptions import HTTPError


class HttpUtility:
    def __init__(self):
        pass

    @staticmethod
    def http_get(url):
        http = urllib3.PoolManager()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:105.0) Gecko/20100101 Firefox/105.0'
        }

        try:
            response = http.request('GET', url, headers=headers)
            if response.status in [200, 302, 304]:
                return response.data.decode('utf-8')
            else:
                raise Exception(
                    'Received non-acceptable status code: ' + str(response.status))
        except HTTPError as e:
            raise Exception('HTTP error occurred: ' + str(e))
