import numpy as np
import pandas as pd
import pickle
from io import StringIO
from tensorflow import keras
from sklearn.preprocessing import OneHotEncoder
import matplotlib.pyplot as plt
class NIDSClassifier:
    def __init__(self, model_file, class_name, onehotX_file, columns_onehot, columns_normalize):
        with open(onehotX_file, "rb") as f:
            self.one_hot = pickle.load(f)
        self.model = keras.models.load_model(model_file)
        self.columns_onehot = columns_onehot
        self.columns_normalize = columns_normalize

    def normalize_cus(self, df, columns_normalize_cus):
        result = df.copy() # do not touch the original df
        for col in columns_normalize_cus.keys():
            result[col] = result[col]/columns_normalize_cus[col]
        return result

    def classify(self, file_name, columns, numcols=None):
        df = pd.read_csv(file_name, header=None)
        if numcols:
            df = df.iloc[: , :numcols]
        df.columns = columns
        # onehot
        df_oh = self.one_hot.transform(df[self.columns_onehot])
        df.drop(self.columns_onehot, axis=1, inplace=True)
        df = pd.concat([df, df_oh], axis=1)
        # normalize
        df = self.normalize_cus(df, self.columns_normalize)
        # predict
        pred = self.model.predict(df)
        print(pred)
        pred = np.argmax(pred,axis=1)

        return [class_name[i] for i in pred]


class_name = ['DoS', 'Probe', 'R2L', 'U2R', 'normal']

columns_normalize = {
    'duration': 57715,
    'src_bytes': 1379963888,
    'dst_bytes': 309937401,
    'wrong_fragment': 3,
    'count': 511,
    'srv_count': 511,
    'dst_host_count': 255,
    'dst_host_srv_count': 255
}
columns_data = ['duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes', 'land', 'wrong_fragment',
    'urgent', 'count', 'srv_count','serror_rate', 'srv_serror_rate', 'rerror_rate', 'srv_rerror_rate',
    'same_srv_rate', 'diff_srv_rate', 'srv_diff_host_rate','dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate','dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate','dst_host_srv_serror_rate', 'dst_host_rerror_rate',
    'dst_host_srv_rerror_rate'
]

model = NIDSClassifier(
    model_file="model_cnn_nids_real.h5",
    class_name=class_name,
    onehotX_file="onehot_encoder_X.pkl",
    columns_onehot=['protocol_type', 'service', 'flag'],
    columns_normalize=columns_normalize,
)

file_data = "new.csv"
pred_classes = model.classify(file_name=file_data, columns=columns_data, numcols=len(columns_data))
print(pred_classes)

# Tạo một dictionary để đếm số lần xuất hiện của mỗi nhãn
predicted_labels = pred_classes
label_counts = {label: 0 for label in class_name}
for label in predicted_labels:
    label_counts[label] += 1

# Biểu đồ thanh
plt.figure(figsize=(8, 6))
plt.bar(label_counts.keys(), label_counts.values(), color='skyblue')
plt.xlabel('Labels')
plt.ylabel('Counts')
plt.title('Distribution of Predicted Labels')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Biểu đồ tròn
plt.figure(figsize=(8, 8))
plt.pie(label_counts.values(), labels=label_counts.keys(), autopct='%1.1f%%', colors=['lightcoral', 'lightgreen', 'lightskyblue', 'lightyellow', 'lightpink'])
plt.title('Distribution of Predicted Labels')
plt.axis('equal')  # Đảm bảo hình tròn
plt.tight_layout()
plt.show()
