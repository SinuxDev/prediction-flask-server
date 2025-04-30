from flask import Flask, request, jsonify
from flask_cors import CORS
import util

app = Flask(__name__)
CORS(app)  # Enables CORS for all routes

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    return jsonify({
        'locations': util.get_location_names()
    })

@app.route('/predict_home_price', methods=['GET', 'POST'])
def predict_home_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])

    return jsonify({
        'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
    })

@app.route('/predict_medicine', methods=['GET', 'POST'])
def predict_price():
    if request.method == 'POST':
        try:
            data = request.get_json()
            # related_branch = request.args.get('branch_id')

            print("Data:", data)
            # print("Related Branch:", related_branch)

            item_id = data['item_id']
            month = int(data['month'])
            year = int(data['year'])
            day = int(data['day'])
            related_branch = data['branch_id']


            # Now pass related_branch to the function
            estimated_price = util.get_predicted_medicine_sale_qty(item_id, month, year, day, related_branch)

            return jsonify({
                'success': True,
                'message': 'Prediction successful.',
                'estimated_sale_qty': estimated_price,
                'related_branch': related_branch
            }), 200

        except KeyError as e:
            return jsonify({
                'success': False,
                'message': f'Missing field: {str(e)}'
            }), 400

        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Internal server error: {str(e)}'
            }), 500

    else:
        return jsonify({
            'success': False,
            'message': 'Method not allowed. Please use POST.'
        }), 405



if __name__ == "__main__":
    print("Starting Python Flask Server for Home Price Prediction")
    util.load_saved_artifacts()
    app.run(host="0.0.0.0", debug=False, port=5000)

