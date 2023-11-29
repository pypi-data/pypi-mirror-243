import requests
import itertools
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode

class metrics:
    def __init__(self, api_key):
        self.base_url = 'https://data.quantsigns.com/'
        self.headers = {'x-api-key': api_key}

    def make_api_call(self, params):
        try:
            if 'size' in params:
                base_url=self.base_url+'indicators/'
            else:
                base_url=self.base_url+'dates/' if 'symb' in params else self.base_url+'symbols/'
            return requests.get(f'{base_url}?{urlencode(params)}', headers=self.headers).json()
        except requests.RequestException as e:
            return {'error': str(e)}

    def extract(self, param_options):
        param_options['mkt']=[param_options['mkt']]
        combinations = list(itertools.product(*param_options.values()))
        params_list = [{k: v for k, v in zip(param_options.keys(), combo)} for combo in combinations]
        with ThreadPoolExecutor(max_workers=10) as executor:
            results = executor.map(self.make_api_call, params_list)
        return {k: v for d in list(results) for k, v in d.items()}


