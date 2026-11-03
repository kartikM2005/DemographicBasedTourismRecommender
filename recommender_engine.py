import pandas as pd
import numpy as np
import pickle
import os
from weather_service import get_live_weather
from itinerary_service import generate_itinerary

class TourismRecommender:
    def __init__(self, models_dir="models", data_dir="data"):
        # Load preprocessor and model
        with open(os.path.join(models_dir, "preprocessor.pkl"), "rb") as f:
            self.preprocessor = pickle.load(f)
            
        with open(os.path.join(models_dir, "stacking_model.pkl"), "rb") as f:
            self.model = pickle.load(f)
            
        self.data_dir = data_dir
        self.dest_path = os.path.join(data_dir, "enriched_destinations.csv")
        self.dest_df = pd.read_csv(self.dest_path)
        self.categories = list(self.model.classes_)

    def reload_catalog(self):
        if os.path.exists(self.dest_path):
            self.dest_df = pd.read_csv(self.dest_path)

    def recommend(self, user_profile, top_n=6):
        self.reload_catalog()
        """
        user_profile: dict with keys:
            Age (int)
            Gender (str: Male/Female/Other)
            Income_Level (str: Low/Medium/High)
            Spending_Amount (float)
            Avg_Trip_Duration (int: days)
            Travel_Group_Type (str: Solo/Couple/Family/Friends)
            Travel_Season (str: Winter/Summer/Monsoon/Post-Monsoon)
        """
        # Convert to DataFrame
        user_df = pd.DataFrame([user_profile])
        
        # Transform features
        X_proc = self.preprocessor.transform(user_df)
        
        # Predict class probabilities from KNN Stacking Ensemble
        class_probs = self.model.predict_proba(X_proc)[0]
        cat_prob_map = dict(zip(self.categories, class_probs))
        
        # Score each destination in the catalog
        scored_dests = []
        user_season = user_profile.get("Travel_Season", "Winter")
        user_income = user_profile.get("Income_Level", "Medium")
        
        for _, dest in self.dest_df.iterrows():
            cat = dest["Category"]
            base_prob = float(cat_prob_map.get(cat, 0.1))
            
            # 1. Seasonal alignment factor (Core research feature)
            if dest["Season"] == user_season:
                season_mult = 1.35
                season_status = "Optimal Season (Peak Experience)"
                season_score = 96.0
            else:
                season_mult = 0.85
                season_status = "Off-Peak Season"
                season_score = 68.0
                
            # 2. Budget compatibility factor
            dest_budget = str(dest["Budget_Tier"])
            if (user_income == "High") or (user_income == dest_budget) or (user_income == "Medium" and dest_budget == "Budget"):
                budget_mult = 1.15
                budget_score = 94.0
            else:
                budget_mult = 0.90
                budget_score = 72.0
                
            # 3. Popularity weight (normalized 0 to 1)
            pop_score = float(dest["Popularity"]) / 10.0
            
            # Final Hybrid Recommendation Score
            composite_score = (base_prob * 0.55 + pop_score * 0.25) * season_mult * budget_mult
            
            # Match percentage normalized realistically between 60% and 98%
            match_pct = min(98.5, max(60.0, composite_score * 85.0))
            
            lat = float(dest.get("Latitude", 20.5937))
            lon = float(dest.get("Longitude", 78.9629))
            
            scored_dests.append({
                "DestinationID": int(dest["DestinationID"]),
                "Name": str(dest["Name"]),
                "State": str(dest["State"]),
                "Category": cat,
                "BestTimeToVisit": str(dest["BestTimeToVisit"]),
                "Destination_Season": str(dest["Season"]),
                "Budget_Tier": dest_budget,
                "Popularity": float(dest["Popularity"]),
                "Latitude": lat,
                "Longitude": lon,
                "Match_Percentage": round(match_pct, 1),
                "Category_Affinity_Score": round(base_prob * 100, 1),
                "Seasonal_Status": season_status,
                "XAI_Breakdown": {
                    "demographic_affinity": round(base_prob * 100, 1),
                    "seasonal_alignment": season_score,
                    "budget_compatibility": budget_score,
                    "popularity_rating": round(float(dest["Popularity"]) * 10, 1)
                }
            })
            
        # Sort descending by match percentage
        scored_dests = sorted(scored_dests, key=lambda x: x["Match_Percentage"], reverse=True)
        top_dests = scored_dests[:top_n]
        
        # Enrich the Top-N recommendations with Live Weather, Real-Time Hazard Alerts, and Custom Itinerary
        trip_duration = int(user_profile.get("Avg_Trip_Duration", 5))
        trip_spending = float(user_profile.get("Spending_Amount", 25000.0))
        trip_group = str(user_profile.get("Travel_Group_Type", "Friends"))

        for d in top_dests:
            d["Live_Ground_Condition"] = get_live_weather(
                d["Latitude"],
                d["Longitude"],
                d["Name"],
                d["State"],
                d["Category"]
            )
            d["Itinerary"] = generate_itinerary(
                dest_name=d["Name"],
                state=d["State"],
                category=d["Category"],
                duration=trip_duration,
                group_type=trip_group,
                spending=trip_spending,
                budget_tier=d["Budget_Tier"]
            )
        
        return {
            "predicted_affinities": {k: round(v * 100, 1) for k, v in sorted(cat_prob_map.items(), key=lambda item: item[1], reverse=True)},
            "primary_recommended_category": self.model.predict(X_proc)[0],
            "top_recommendations": top_dests
        }

if __name__ == "__main__":
    recommender = TourismRecommender()
    
    test_user_1 = {
        "Age": 22,
        "Gender": "Male",
        "Income_Level": "Medium",
        "Spending_Amount": 2200.0,
        "Avg_Trip_Duration": 5,
        "Travel_Group_Type": "Friends",
        "Travel_Season": "Winter"
    }
    
    res1 = recommender.recommend(test_user_1, top_n=3)
    print("="*60)
    print("TEST WITH LIVE WEATHER & HAZARD INTELLIGENCE:")
    for d in res1["top_recommendations"]:
        w = d["Live_Ground_Condition"]
        print(f"\n* {d['Name']} ({d['State']}) | {d['Category']} | Match: {d['Match_Percentage']}%")
        print(f"  Live: {w['temperature']} deg C, {w['condition']} | Wind: {w['wind_speed']} km/h")
        print(f"  Hazard Level: {w['hazard_level']}")
        print(f"  Advisory: {w['advisory']}")
        print(f"  XAI Scores: {d['XAI_Breakdown']}")
