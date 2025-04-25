from flask import Flask, render_template, jsonify
import pandas as pd

app = Flask(__name__)

# Load datasets
def load_data():
    df_licensed = pd.read_csv("csv/LincensedDriver1.csv")
    df_vehicle = pd.read_csv("csv/Motor_Vehicle_Registrations.csv")
    df_violations = pd.read_csv("csv/Traffic_Violations.csv")
    
    return df_licensed, df_vehicle, df_violations

# -------------------- Licensed Driver Analysis --------------------

def get_gender_distribution():
    df_licensed, _, _ = load_data()
    df_filtered = df_licensed[(df_licensed['Year1'] >= 2000) & (df_licensed['Year1'] <= 2020)]
    df_filtered = df_filtered.dropna(subset=['Licensed'])
    gender_distribution = df_filtered.groupby('Gender')['Licensed'].sum()

    # Force order: Male first, then Female
    male_total = int(gender_distribution.get('Male', 0))
    female_total = int(gender_distribution.get('Female', 0))
    total_drivers = male_total + female_total

    # Percentages
    male_percent = round((male_total / total_drivers) * 100, 2) if total_drivers else 0
    female_percent = round((female_total / total_drivers) * 100, 2) if total_drivers else 0

    formatted_labels = [
        f"Male ({male_total:,}, {male_percent}%)",
        f"Female ({female_total:,}, {female_percent}%)"
    ]

    return {
    "labels": [
        f"Male ({male_total:,}, {male_percent}%)",
        f"Female ({female_total:,}, {female_percent}%)"
    ],
    "values": [male_percent, female_percent],
}





def get_top_10_states():
    df_licensed, _, _ = load_data()
    df_filtered = df_licensed[df_licensed["Year1"] == 2020]
    top_10 = df_filtered.groupby("State1")["Licensed"].sum().nlargest(10).reset_index()
    return {"labels": top_10["State1"].tolist(), "values": top_10["Licensed"].tolist()}

def get_age_distribution():
    df_licensed, _, _ = load_data()
    df_filtered = df_licensed[df_licensed["Year1"] == 2020]
    age_groups = df_filtered.groupby("Age1")["Licensed"].sum().reset_index()
    return {"labels": age_groups["Age1"].tolist(), "values": age_groups["Licensed"].tolist()}

# -------------------- Motor Vehicle Registration Analysis --------------------

def get_top_10_autos():
    _, df_vehicle, _ = load_data()
    top_10 = df_vehicle.groupby("Year2")["Auto2"].sum().nlargest(10).reset_index()
    return {"labels": top_10["Year2"].tolist(), "values": top_10["Auto2"].tolist()}

def get_total_buses_trucks_2010_2020():
    _, df_vehicle, _ = load_data()
    df_filtered = df_vehicle[(df_vehicle["Year2"] >= 1900) & (df_vehicle["Year2"] <= 2020)]
    total_buses = df_filtered["Bus2"].sum()
    total_trucks = df_filtered["Truck2"].sum()
    return {"labels": ["Buses", "Trucks"], "values": [total_buses, total_trucks]}


def get_top_10_motorcycles_2020():
    _, df_vehicle, _ = load_data()
    df_filtered = df_vehicle[df_vehicle["Year2"] == 2020]
    top_10 = df_filtered.groupby("State2")["Motorcycle2"].sum().nlargest(10).reset_index()
    return {"labels": top_10["State2"].tolist(), "values": top_10["Motorcycle2"].tolist()}

# -------------------- Traffic Violations Analysis --------------------

def get_top_5_sub_agencies():
    _, _, df_violations = load_data()
    df_filtered = df_violations[(df_violations["Year"] >= 2020) & (df_violations["Year"] <= 2024)]
    top_5 = df_filtered["SubAgency"].value_counts().nlargest(5).reset_index()
    top_5.columns = ["SubAgency", "ViolationCount"]
    return {"labels": top_5["SubAgency"].tolist(), "values": top_5["ViolationCount"].tolist()}

def get_top_violations():
    _, _, df_violations = load_data()
    df_filtered = df_violations[(df_violations["Year"] >= 2020) & (df_violations["Year"] <= 2024)]
    top10_violations = df_filtered["Violation"].value_counts().head(10).reset_index()
    top10_violations.columns = ["Violation", "Count"]
    return {"labels": top10_violations["Violation"].tolist(), "values": top10_violations["Count"].tolist()}


def get_top_5_vehicle_types():
    _, _, df_violations = load_data()
    df_filtered = df_violations[(df_violations["Year"] >= 2020) & (df_violations["Year"] <= 2024)]
    top_5 = df_filtered["VehicleType"].value_counts().nlargest(5).reset_index()
    top_5.columns = ["VehicleType", "Count"]
    return {"labels": top_5["VehicleType"].tolist(), "values": top_5["Count"].tolist()}

# -------------------- Routes --------------------

@app.route('/')
def index():
    return render_template('index.html')

# Licensed Driver API routes
@app.route('/gender_distribution')
def gender_distribution():
    return jsonify(get_gender_distribution())

@app.route('/top10_states')
def top10_states():
    return jsonify(get_top_10_states())

@app.route('/age_distribution')
def age_distribution():
    return jsonify(get_age_distribution())

# Motor Vehicle Registration API routes
@app.route('/top10_autos')
def top10_autos():
    return jsonify(get_top_10_autos())

@app.route('/total_buses_trucks_2010_2020')
def total_buses_trucks_2010_2020():
    return jsonify(get_total_buses_trucks_2010_2020())

@app.route('/top10_motorcycles_2020')
def top10_motorcycles_2020():
    return jsonify(get_top_10_motorcycles_2020())

# Traffic Violations API routes
@app.route('/top5_sub_agencies')
def top5_sub_agencies():
    return jsonify(get_top_5_sub_agencies())

@app.route('/top10_violations')
def top10_violations():
    return jsonify(get_top_violations())

@app.route('/top5_vehicle_types')
def top5_vehicle_types():
    return jsonify(get_top_5_vehicle_types())

if __name__ == '__main__':  
    app.run(debug=True)
