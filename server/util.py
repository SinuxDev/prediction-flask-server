import json
import pickle
import numpy as np
import pandas as pd

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location, sqft, bhk, bath):
    # load_saved_artifacts()
    loc_index = None
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1
    x = np.zeros(len(__data_columns))
    print(x)
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    print("loc_index: ", loc_index)
    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0], 2)


def get_predicted_medicine_sale_qty(item_id, month, year, day):
    loc_index = -1
    try:
        loc_index = __data_columns.index(item_id.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = month
    x[1] = year
    x[2] = day

    if loc_index >= 0:
        x[loc_index] = 1

    x_df = pd.DataFrame([x], columns=__data_columns)
    return round(__model.predict(x_df)[0], 2)


def get_location_names():
    # load_saved_artifacts()
    return __locations

def load_saved_artifacts():
    print("Loading saved artifacts... start")
    global __data_columns
    global __locations

    with open('./artifacts/Cherry-K.medicine-prediction-model.json', 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]
    
    global __model
    with open("./artifacts/Cherry-K.medicine-prediction-model.pickle", 'rb') as f:
        __model = pickle.load(f)
    print("Loading saved artifacts... done")

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_location_names())
    # print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    # print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    # print(get_estimated_price('Kalhalli', 1000, 2, 2))
    # print(get_estimated_price('Fjipura', 1000, 2, 2))
    print(get_predicted_medicine_sale_qty("649fe69922c5eb76edec5280", "5", "2025","31"))
