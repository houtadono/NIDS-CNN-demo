import numpy as np
import pandas as pd

import pickle
from io import StringIO
from tensorflow import keras
from sklearn.preprocessing import OneHotEncoder

def normalize_with_log(df, cols):
    result = df.copy() # do not touch the original df
    for col in cols:
        result[col] = np.log1p(result[col])
    return result
def normalize_cus(df, columns_normalize_cus):
    result = df.copy() # do not touch the original df
    for col in columns_normalize_cus.keys():
        result[col] = result[col]/columns_normalize_cus[col]
    return result

columns_normalize_cus = {
    'duration': 57715,
    'src_bytes': 1379963888,
    'dst_bytes': 309937401,
    'wrong_fragment': 3,
    'count': 511,
    'srv_count': 511,
    'dst_host_count': 255,
    'dst_host_srv_count': 255
}
columns_with_values_other_than_zero_or_one = ['duration', 'src_bytes', 'dst_bytes', 'wrong_fragment', 'urgent',
       'count', 'srv_count', 'serror_rate', 'srv_serror_rate', 'rerror_rate',
       'srv_rerror_rate', 'same_srv_rate', 'diff_srv_rate',
       'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
       'dst_host_same_srv_rate', 'dst_host_diff_srv_rate',
       'dst_host_same_src_port_rate', 'dst_host_srv_diff_host_rate',
       'dst_host_serror_rate', 'dst_host_srv_serror_rate',
       'dst_host_rerror_rate', 'dst_host_srv_rerror_rate']

with open("onehot_encoder_X.pkl", "rb") as f:
    one_hot = pickle.load(f)


model = keras.models.load_model("model_cnn_nids_real.h5")
print(model)

# data = '''0,tcp,private,OTH,66,0,0,0,0,0,0,0.00,0.00,0.00,0.00,0.00,0.00,0.00,19,12,0.63,0.37,0.92,0.00,0.00,0.00,0.00,0.00,163.70.158.14,443,192.168.1.10,56478,2024-03-18T19:30:24'''
# csv_data = StringIO(data)

df = pd.read_csv("new.csv", header=None)
df = df.iloc[: , :28]
df.columns = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes',
       'dst_bytes', 'land', 'wrong_fragment', 'urgent', 'count', 'srv_count',
       'serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
       'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate',
       'dst_host_count', 'dst_host_srv_count', 'dst_host_same_srv_rate',
       'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
       'dst_host_srv_diff_host_rate', 'dst_host_serror_rate',
       'dst_host_srv_serror_rate', 'dst_host_rerror_rate',
       'dst_host_srv_rerror_rate']

print(df, df.shape)
columns_object_X = ['protocol_type', 'service', 'flag']
df_oh = one_hot.transform(df[columns_object_X])
df.drop(columns_object_X, axis=1, inplace=True)
df = pd.concat([df, df_oh], axis=1)


df = normalize_cus(df, columns_normalize_cus)

pred = model.predict(df)
print(pred)
pred = np.argmax(pred,axis=1)
class_name = ['DoS', 'Probe', 'R2L', 'U2R', 'normal']

print([class_name[i] for i in pred])