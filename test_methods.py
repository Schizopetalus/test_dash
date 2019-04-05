# -*- coding: utf-8 -*-


import unittest


import pandas as pd

def read_store(stored_data):
    """
    @ stored_data dict (dans l'appli obtenu à partir de json.to_dict)
    """
    data_as_df = pd.DataFrame.from_dict(stored_data)
    conv_dict = {'date': pd.to_datetime}
    for column in data_as_df.columns:
        data_as_df[column] = conv_dict.get(
            column,pd.to_numeric)(data_as_df[column])
    return data_as_df

