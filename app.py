from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import os
import json
from recommender_engine import TourismRecommender

app = Flask(__name__)

# Initialize recommender engine
recommender = TourismRecommender()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/recommend', methods=['POST'])
def get_recommendations():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
            
        raw_income = str(data.get("Income_Level", "Medium")).strip().capitalize()
        income_map = {"Budget": "Low", "Low": "Low", "Medium": "Medium", "Moderate": "Medium", "High": "High", "Luxury": "High"}
        income_level = income_map.get(raw_income, "Medium")

        # Parse inputs with defaults
        user_profile = {
            "Age": int(data.get("Age", 25)),
            "Gender": str(data.get("Gender", "Male")),
            "Income_Level": income_level,
            "Spending_Amount": float(data.get("Spending_Amount", 2500.0)),
            "Avg_Trip_Duration": int(data.get("Avg_Trip_Duration", 7)),
            "Travel_Group_Type": str(data.get("Travel_Group_Type", "Friends")),
            "Travel_Season": str(data.get("Travel_Season", "Winter"))
        }
        
        top_n = int(data.get("top_n", 6))
        
        # Run recommendation inference
        result = recommender.recommend(user_profile, top_n=top_n)
        
        # Add explanation details for each destination
        for dest in result["top_recommendations"]:
            dest["Explanation"] = (
                f"Matches {user_profile['Age']}y/o {user_profile['Travel_Group_Type']} preferences for "
                f"{dest['Category']}. {dest['Seasonal_Status']} for {user_profile['Travel_Season']} travel."
            )
            
        return jsonify({
            "status": "success",
            "user_profile": user_profile,
            "data": result
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/metrics', methods=['GET'])
def get_metrics():
    try:
        results_path = "models/evaluation_results.csv"
        if os.path.exists(results_path):
            metrics_df = pd.read_csv(results_path)
            return jsonify({
                "status": "success",
                "metrics": metrics_df.to_dict(orient="records"),
                "benchmark_reference": {
                    "paper": "Marzuki et al. (2025)",
                    "journal": "IJIES Vol. 18, No. 4, pp. 219–232",
                    "baseline_accuracy": 86.89,
                    "proposed_accuracy": 85.98,
                    "novel_extensions": [
                        "Incorporated 4 Indian Seasonal Contexts (Winter, Summer, Monsoon, Post-Monsoon)",
                        "Enriched demographic profiling with budget tiers and group dynamics",
                        "Extended single-class prediction to Ranked Top-N Hybrid Recommendation with Match %"
                    ]
                }
            })
        else:
            return jsonify({"status": "error", "message": "Metrics not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/destinations', methods=['GET'])
def get_destinations():
    try:
        dest_path = "data/enriched_destinations.csv"
        if os.path.exists(dest_path):
            df = pd.read_csv(dest_path)
            
            # Optional query filters
            category = request.args.get('category')
            season = request.args.get('season')
            state = request.args.get('state')
            
            if category and category != 'All':
                df = df[df['Category'] == category]
            if season and season != 'All':
                df = df[df['Season'] == season]
            if state and state != 'All':
                df = df[df['State'] == state]
                
            return jsonify({
                "status": "success",
                "count": len(df),
                "destinations": df.to_dict(orient="records")
            })
        else:
            return jsonify({"status": "error", "message": "Destinations not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    print("Starting Demographic Tourism Recommender System on http://127.0.0.1:5000 ...")
    app.run(host='127.0.0.1', port=5000, debug=False)
