from flask import Flask, request, jsonify
import util

app = Flask(__name__)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])
    response = jsonify({
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

@app.route('/predict_medicine', methods=['GET', 'POST'])
def predict_price():
    if request.method == 'POST':
        item_id = request.form['item_id']
        month = int(request.form['month'])
        year = int(request.form['year'])
        day = int(request.form['day'])

        estimated_price = util.get_predicted_medicine_price(item_id, month, year, day)

        response = jsonify({
            'estimated_price': estimated_price
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    else:
        return jsonify({'message': 'Send a POST request with item_id, month, year, and day'})


if __name__ == "__main__":
    print("Starting Python Flask Server for Home Price Prediction")
    util.load_saved_artifacts()
    app.run()

