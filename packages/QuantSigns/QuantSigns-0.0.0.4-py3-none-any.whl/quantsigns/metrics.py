import requests
import itertools
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlencode

class metrics:
    def __init__(self, api_key):
        self.base_url = 'https://data.quantsigns.com/'
        self.headers = {'x-api-key': api_key}

    def extract(self, param_options):
        param_options['mkt']=[param_options['mkt']]
        combinations = list(itertools.product(*param_options.values()))
        print(len(combinations))
        params_list = [{k: v for k, v in zip(param_options.keys(), combo)} for combo in combinations]
        with ThreadPoolExecutor() as executor:
            results = executor.map(self._make_api_call, params_list)
        if 'size' in params_list:
            return {k:self._ret_df(k,v) for d in list(results) for k, v in d.items()}
        else:
            return {k:v for d in list(results) for k, v in d.items()}

    def _make_api_call(self, params):
        try:
            if 'size' in params:
                base_url=self.base_url+'indicators/'
            else:
                base_url=self.base_url+'dates/' if 'symb' in params else self.base_url+'symbols/'
            return requests.get(f'{base_url}?{urlencode(params)}', headers=self.headers).json()
        except requests.RequestException as e:
            return {'error': str(e)}


    def _ret_df(self,k,data):
        l1=list(data.keys())[0]
        l2=list(data[l1].keys())
        with ThreadPoolExecutor() as executor:
            df_data = executor.map(self._extract_data, [k]*len(data.items()), data.items())
        return pd.DataFrame(list(df_data), columns=['Data','Time']+[i+'_'+str(j+1) if type(data[l1][i]).__name__=='list' else i for i in l2 for j in range(len(data[l1][i]) if type(data[l1][i]).__name__=='list' else 1)])

    def _extract_data(self, k,i):
        return list(itertools.chain(*[[k, i[0]]] + [i[1][j] if type(i[1][j]).__name__==list else [i[1][j]] for j in i[1]]))
