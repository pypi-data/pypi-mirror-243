import requests as rq

from diabolocom_api_client import resources
from diabolocom_api_client.utils import urljoin


class Client:
    BASE_URL = "https://public-{}.engage.diabolocom.com"

    def __init__(self, zone, token):
        
        self._session = rq.Session()
        self._session.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Private-Token': token
        }

        self._base_endpoint = urljoin(self.BASE_URL.format(zone), 'api')
        self._resources = {
            'v1': resources.V1Pool(
                urljoin(self._base_endpoint, 'v1'), self._session
            ),
            'v2': resources.V2Pool(
                urljoin(self._base_endpoint, 'v2'), self._session
            )
        }

    @property
    def resources(self):
        return self._resources
    
    @property
    def v1(self):
        return self._resources['v1']
    
    @property
    def v2(self):
        return self._resources['v2']    
