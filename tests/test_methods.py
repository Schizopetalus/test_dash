# -*- coding: utf-8 -*-

# Oh que c'est laid!
import sys
sys.path.append('/home/hugo/test_dash')

import json
from test_data_table import read_store,dflb
with open('tests/client_side_data/data_cor.json','r') as f:
    stored_data = json.load(f)


df_stored = read_store(stored_data)
df_stored.htn = dflb.htnavg


print(df_stored.head())
print(dflb.head())
