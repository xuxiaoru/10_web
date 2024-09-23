import os

import numpy as np
import pandas as pd

# for key, value in os.environ.items():
#     print(key, value)

print(os.getenv('PWD'))

# pad_id = os.environ['PAD_ID']
# token = os.environ['TOKEN']
# print(pad_id, token)

pwd = os.environ['PWD']
id = os.environ['ID']
print(pwd, id)