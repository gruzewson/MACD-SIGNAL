import pandas as pd

def get_data(name):
    df = pd.read_csv(name, sep=';')
    data = df.values.tolist()
    rows = len(data)
    return data, rows
