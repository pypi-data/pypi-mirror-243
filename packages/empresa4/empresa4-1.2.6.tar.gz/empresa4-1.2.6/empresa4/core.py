from math import radians, cos, sin, asin, sqrt
from typing import List
import pandas as pd
from .datasets import get_dataset


def calculate_error(predicted: List, real_values: List):
    """
    Calculate the error between the predicted values and the real values
    :param predicted: list of predicted values
    :param real_values: list of real values
    :return: error
    """
    error = 0
    real_sum = sum(real_values)
    for i in range(len(predicted)):
        error += abs(predicted[i] - real_values[i])
    return error / real_sum


def calculate_error_2(df: pd.DataFrame, periodo: int):
    if "product_id" not  in df.columns or "prediction" not in df.columns:
        raise ValueError("df must have 'product_id' and 'prediction' columns")
    
    if len(df["product_id"].unique().tolist()) != len(df["product_id"].tolist()):
        raise ValueError("df must have unique product_id values")   

    orig = get_dataset("02_productos_todos")
    data_to_compare = orig[(orig["periodo"] == periodo) & (orig["product_id"].isin(df["product_id"].unique()))]
    # merge "tn" column of data_to_compare with df by product_id
    merged = pd.merge(df, data_to_compare[["product_id", "tn"]], on="product_id", how="inner", validate="one_to_one")
    return calculate_error(merged["prediction"].to_list(), merged["tn"].to_list())


def get_clientes_importantes():
    return [
        10001,
        10002,
        10003,
        10004,
        10005,
        10006,
        10007,
        10008,
        10009,
        10011,
        10012,
        10013,
    ]


def get_productos_importantes():
    return [20001, 20002, 20003, 20004, 20005, 20006, 20007, 20009, 20011, 20032]


def filter_productos_importantes(df):
    return df[df["product_id"].isin(get_productos_importantes())]

def filter_clientes_importantes(df):
    return df[df["customer_id"].isin(get_clientes_importantes())]