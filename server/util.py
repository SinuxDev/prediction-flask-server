import json
import pickle
import numpy as np
import pandas as pd

__locations = None
__data_columns = None
__model = None

branchMapper = {
	"6474394fdab649311f9fcc32":{
		"modelFileName": "./artifacts/Cherry-K.SouthOakkalapa.medicine-prediction-model.pickle",
		"columnFileName": "./artifacts/Cherry-K.SouthOakkalapa-medicine-prediction-model.json",
	},
	"649559535fc22f0e7f0884fe":{
		"modelFileName": "./artifacts/Cherry-K.TachiLeik.medicine-prediction-model.pickle",
		"columnFileName": "./artifacts/Cherry-K.TachiLeik-medicine-prediction-model.json",
	},
	"647439aadab649311f9fcc36":{
		"modelFileName": "./artifacts/Cherry-K.Mandalay.medicine-prediction-model.pickle",
		"columnFileName": "./artifacts/Cherry-K.Mandalay-medicine-prediction-model.json",
	},
	"64743985dab649311f9fcc33":{
		"modelFileName": "./artifacts/Cherry-K.8mile.medicine-prediction-model.pickle",
		"columnFileName": "./artifacts/Cherry-K.8mile-medicine-prediction-model.json",
	},
	"64743991dab649311f9fcc34":{
		"modelFileName": "./artifacts/Cherry-K.NayPyiTaw.medicine-prediction-model.pickle",
		"columnFileName": "./artifacts/Cherry-K.NayPyiTaw-medicine-prediction-model.json",
	},
	"6535f7fef68b0525e0eaf151":{
		"modelFileName": "./artifacts/Cherry-K.SanChaung.medicine-prediction-model.pickle",
		"columnFileName": "./artifacts/Cherry-K.SanChaung-medicine-prediction-model.json",
	},
	"6535f811f68b0525e0eaf152":{
		"modelFileName": "./artifacts/Cherry-K.ThinGanGyun.medicine-prediction-model.pickle",
		"columnFileName": "./artifacts/Cherry-K.ThinGanGyun-medicine-prediction-model.json",
	},
	"651647a617c8dbb264085bcf":{
		"modelFileName": "./artifacts/Cherry-K.TaungGyi.medicine-prediction-model.pickle",
		"columnFileName": "./artifacts/Cherry-K.TaungGyi-medicine-prediction-model.json",
	},
	"66023ad88bb368fe815343da":{
		"modelFileName": "./artifacts/Cherry-K.HlaingTharYar.medicine-prediction-model.pickle",
		"columnFileName": "./artifacts/Cherry-K.HlaingTharYar-medicine-prediction-model.json",
	},
	"66ed176674f503bf95858cf8":{
		"modelFileName": "./artifacts/Cherry-K.Tamwe.medicine-prediction-model.pickle",
		"columnFileName": "./artifacts/Cherry-K.Tamwe-medicine-prediction-model.json",
	},
	"675a5d8fb2a9c1d91266a144":{
		"modelFileName": "./artifacts/Cherry-K.LanMaDaw.medicine-prediction-model.pickle",
		"columnFileName": "./artifacts/Cherry-K.LanMaDaw-medicine-prediction-model.json",
	},
}


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


def get_predicted_medicine_sale_qty(item_id, month, year, day, branchID):
    loc_index = -1
    load_branch_artifacts(branchID)
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

def load_branch_artifacts(branch):
    print("Loading saved artifacts... start")

    global __data_columns
    global __locations
    global __model

    # Validate branch
    if branch not in branchMapper:
        raise ValueError(f"Branch ID '{branch}' is not supported.")

    with open(branchMapper[branch]['columnFileName'], 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # assuming locations start from index 3

    with open(branchMapper[branch]['modelFileName'], 'rb') as f:
        __model = pickle.load(f)

    print("Loading", branch, "artifacts... done")


def get_location_names():
    # load_saved_artifacts()
    return __locations

def load_saved_artifacts():
    print("Loading saved artifacts... start")
    global __data_columns
    global __locations

    with open('./artifacts/Cherry-K.HlaingTharYar-medicine-prediction-model.json', 'r') as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]
    
    global __model
    with open("./artifacts/Cherry-K.HlaingTharYar.medicine-prediction-model.pickle", 'rb') as f:
        __model = pickle.load(f)
    print("Loading saved artifacts... done")



if __name__ == '__main__':
    # load_saved_artifacts()
    print(get_location_names())
    # print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    # print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    # print(get_estimated_price('Kalhalli', 1000, 2, 2))
    # print(get_estimated_price('Fjipura', 1000, 2, 2))
    print(get_predicted_medicine_sale_qty("649fe69922c5eb76edec5280", "5", "2025","31"))
