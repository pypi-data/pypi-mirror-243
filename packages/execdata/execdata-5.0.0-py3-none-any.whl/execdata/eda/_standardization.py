'''
Date         : 2022-10-25 17:21:52
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2023-11-13 11:13:38
LastEditors  : BDFD
Description  : 
FilePath     : \execdata\eda\_standardization.py
Copyright (c) 2022 by BDFD, All Rights Reserved. 
'''


import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedShuffleSplit


def fit_label_encode(df, categorical_features):
    label_encoders = []
    for feature in categorical_features:
        Le = LabelEncoder()
        Le.fit(df[feature])
        # print(type(Le))
        label_encoders.append(Le)
        # print('The Feature', feature, ',with value', Le.classes_)
    return label_encoders


def transform_label_encode(df, categorical_features, label_encoders):
    # Transform the new data using the fitted LabelEncoders
    transformed_new_data = []
    for i in range(len(categorical_features)):
        le = label_encoders[i]
        feature = categorical_features[i]
        # print(i, feature)
        # print(i, label_encoders[i].classes_)
        # print(i, categorical_features[i])
        transformed_col = le.transform(df[categorical_features[i]])
        df[feature] = transformed_col
        # print(transformed_col)
        transformed_new_data.append(transformed_col)
    df_transformed = pd.DataFrame(transformed_new_data).transpose()
    df_transformed.columns = categorical_features
    return df_transformed


def inverse_label_encode(df, categorical_features, label_encoders):
    # Convert the transformed data back to the original form
    inverse_transformed_data = []
    for i in range(len(categorical_features)):
        le = label_encoders[i]
        # print(label_encoders[i].classes_)
        # print(feature)
        inverse_transformed_col = le.inverse_transform(
            df[categorical_features[i]])
        inverse_transformed_data.append(inverse_transformed_col)
    # Display the inverse transformed data
    df_inverse_transformed = pd.DataFrame(inverse_transformed_data).transpose()
    df_inverse_transformed.columns = categorical_features
    return df_inverse_transformed
