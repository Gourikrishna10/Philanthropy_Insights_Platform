from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = "D://vscodefol//Philanthropy_Insights//Philanthropy_Insights_Platform//dataset"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

df = None  # Global DataFrame

# Function to load dataset
def load_dataset(file_path):
    global df
    try:
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xls') or file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            return False

        # Normalize column names
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
        if 'date_of_last_donation' in df.columns:
            df['date_of_last_donation'] = pd.to_datetime(df['date_of_last_donation'], errors='coerce')

        print("✅ Dataset loaded successfully.")
        return True
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return False

# API for file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    global df
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ['.csv', '.xls', '.xlsx']:
        return jsonify({"error": "Invalid file format. Upload a CSV or Excel file"}), 400
    
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    if load_dataset(file_path):
        return jsonify({"message": "File uploaded and dataset updated successfully!"})
    else:
        return jsonify({"error": "Failed to process the file"}), 500

# API to fetch insights
@app.route('/get-insights', methods=['GET'])
def get_insights():
    if df is None or 'donation_amount' not in df.columns:
        return jsonify({"error": "No valid dataset available"}), 400
    
    insights = {
        "total_donations": df['donation_amount'].sum(),
        "most_popular_cause": df['donation_cause'].value_counts().idxmax(),
        "top_donor": df.loc[df['donation_amount'].idxmax(), 'donor_id']
    }
    return jsonify(insights)

# API to get monthly trends
@app.route('/get-trends', methods=['GET'])
def get_trends():
    if df is None or 'date_of_last_donation' not in df.columns:
        return jsonify({"error": "No valid dataset available"}), 400

    monthly_donations = df.groupby(df['date_of_last_donation'].dt.to_period('M'))['donation_amount'].sum()
    return jsonify({str(k): v for k, v in monthly_donations.items()})

# API to get donation causes
@app.route('/get-causes', methods=['GET'])
def get_causes():
    if df is None:
        return jsonify({"error": "No data available"}), 400
    return jsonify(df['donation_cause'].value_counts().to_dict())

# API to get age group trends
@app.route('/get-age-groups', methods=['GET'])
def get_age_groups():
    if df is None:
        return jsonify({"error": "No data available"}), 400

    df['age_group'] = pd.cut(df['age'], bins=[18, 30, 50, 70, 100], labels=['18-30', '31-50', '51-70', '71+'])
    return jsonify(df.groupby('age_group')['donation_amount'].sum().to_dict())

# API to get gender-based donation trends
@app.route('/get-gender-trends', methods=['GET'])
def get_gender_trends():
    if df is None:
        return jsonify({"error": "No data available"}), 400
    return jsonify(df.groupby('gender')['donation_amount'].sum().to_dict())

# API to get location-based donation trends
@app.route('/get-location-trends', methods=['GET'])
def get_location_trends():
    if df is None:
        return jsonify({"error": "No data available"}), 400
    return jsonify(df.groupby('location')['donation_amount'].sum().to_dict())

# API to get donation details by gender
@app.route('/get-gender-donations', methods=['GET'])
def get_gender_donations():
    if df is None:
        return jsonify({"error": "No data available"}), 400
    return jsonify(df.groupby('gender')['donation_amount'].sum().to_dict())

# API to get donation details by location
@app.route('/get-location-donations', methods=['GET'])
def get_location_donations():
    if df is None:
        return jsonify({"error": "No data available"}), 400
    return jsonify(df.groupby('location')['donation_amount'].sum().to_dict())

# API to fetch all locations
@app.route('/get-locations', methods=['GET'])
def get_locations():
    if df is None:
        return jsonify({"error": "No data available"}), 400
    return jsonify(df['location'].unique().tolist())

# API to get filtered data based on gender, age, and location
@app.route('/get-filtered-data', methods=['GET'])
def get_filtered_data():
    if df is None:
        return jsonify({"error": "No data available"}), 400

    gender = request.args.get('gender', 'all')
    age = request.args.get('age', 'all')
    location = request.args.get('location', 'all')

    filtered_df = df.copy()

    if gender != 'all':
        filtered_df = filtered_df[filtered_df['gender'] == gender]

    if age != 'all':
        age_ranges = {'18-30': (18, 30), '31-50': (31, 50), '51-70': (51, 70), '71+': (71, 100)}
        if age in age_ranges:
            age_min, age_max = age_ranges[age]
            filtered_df = filtered_df[(filtered_df['age'] >= age_min) & (filtered_df['age'] <= age_max)]

    if location != 'all':
        filtered_df = filtered_df[filtered_df['location'] == location]

    filtered_data = filtered_df.groupby('donation_cause')['donation_amount'].sum().to_dict()
    return jsonify(filtered_data)

if __name__ == '__main__':
    app.run(debug=True)
