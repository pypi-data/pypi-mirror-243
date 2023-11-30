import json
import pandas as pd

def preprocess_data(data):
    if isinstance(data, dict):
        for key, value in list(data.items()):
            new_key = key.replace('.', '_').replace('\"', '').replace('\'', '')
            if isinstance(value, str) and (value == '' or value == "None" or value == None or value == ' '):
                data[key] = None
            elif isinstance(value, (dict, list)):
                preprocess_data(value)
            if key != new_key:
                data[new_key]=data.pop(key)
    elif isinstance(data, list):
        for item in data:
            preprocess_data(item)
    return data

def cross_join(left, right):
    if not right:
        return left

    new_rows = []
    for left_row in left:
        for right_row in right:
            temp_row = left_row.copy()
            temp_row.update(right_row)
            new_rows.append(temp_row)

    return new_rows

def flatten_list(data):
    for elem in data:
        if isinstance(elem, list):
            yield from flatten_list(elem)
        else:
            yield elem

def flatten_json(data, prev_heading=''):
    if isinstance(data, dict):
        rows = [{}]
        for key, value in data.items():
            rows = cross_join(rows, flatten_json(value, prev_heading + '_' + key))
    elif isinstance(data, list):
        rows = []
        for item in data:
            rows.extend(flatten_list(flatten_json(item, prev_heading)))
    else:
        rows = [{prev_heading[1:]: data}]
    return rows

def flatten_complex_json(data_in):
    data_in = preprocess_data(data_in)
    rows = flatten_json(data_in)
    return pd.DataFrame(rows)