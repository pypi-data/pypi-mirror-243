# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta as rd
from .api import quantim

class bi_data(quantim):
    def __init__(self, username, password, secretpool, env="pdn", api_url=None):
        super().__init__(username, password, secretpool, env, api_url)

    def get_positions_afps_cl(self, ref_date=None, bucket="condor-sura"):
        '''
        Get Value at Risk results and suport information.
        '''
        ref_date = dt.datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0) - rd(days=1) if ref_date is None else dt.datetime.strptime(ref_date, '%Y-%m-%d') 
        key = f'{prefix}{ref_date.year}/{ref_date.strftime("%m")}/data.json'

        data = {'bucket':bucket, 'key':key}
        try:
            resp = self.api_call('retrieve_json_s3', method="post", data=data, verify=False)
            keys = list(resp.keys())
            resp_dfs = {k:pd.DataFrame(resp[k]) for k in keys}
        except:
            print(f"Data not available for {ref_date}. Try previous month!")
            keys, resp_dfs = None, None
        return keys, resp_dfs

