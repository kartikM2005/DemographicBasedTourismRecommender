import pandas as pd
import numpy as np
import pickle
import os

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

    def recommend(self, user_profile, top_n=5):
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
            base_prob = cat_prob_map.get(cat, 0.1)
            
            # 1. Seasonal alignment factor (Core research feature)
            if dest["Season"] == user_season:
                season_mult = 1.35
                season_status = "Optimal Season (Peak Experience)"
            else:
                season_mult = 0.85
                season_status = "Off-Peak Season"
                
            # 2. Budget compatibility factor
            dest_budget = dest["Budget_Tier"]
            if (user_income == "High") or (user_income == dest_budget) or (user_income == "Medium" and dest_budget == "Budget"):
                budget_mult = 1.15
            else:
                budget_mult = 0.90
                
            # 3. Popularity weight (normalized 0 to 1)
            pop_score = dest["Popularity"] / 10.0
            
            # Final Hybrid Recommendation Score
            composite_score = (base_prob * 0.55 + pop_score * 0.25) * season_mult * budget_mult
            
            # Match percentage normalized realistically between 60% and 98%
            match_pct = min(98.5, max(60.0, composite_score * 85.0))
            
            scored_dests.append({
                "DestinationID": dest["DestinationID"],
                "Name": dest["Name"],
                "State": dest["State"],
                "Category": cat,
                "BestTimeToVisit": dest["BestTimeToVisit"],
                "Destination_Season": dest["Season"],
                "Budget_Tier": dest["Budget_Tier"],
                "Popularity": dest["Popularity"],
                "Match_Percentage": round(match_pct, 1),
                "Category_Affinity_Score": round(base_prob * 100, 1),
                "Seasonal_Status": season_status
            })
            
        # Sort descending by match percentage
        scored_dests = sorted(scored_dests, key=lambda x: x["Match_Percentage"], reverse=True)
        
        return {
            "predicted_affinities": {k: round(v * 100, 1) for k, v in sorted(cat_prob_map.items(), key=lambda item: item[1], reverse=True)},
            "primary_recommended_category": self.model.predict(X_proc)[0],
            "top_recommendations": scored_dests[:top_n]
        }

if __name__ == "__main__":
    recommender = TourismRecommender()
    
    # Test case 1: 22-year-old traveler with Friends in Winter
    test_user_1 = {
        "Age": 22,
        "Gender": "Male",
        "Income_Level": "Medium",
        "Spending_Amount": 2200.0,
        "Avg_Trip_Duration": 5,
        "Travel_Group_Type": "Friends",
        "Travel_Season": "Winter"
    }
    
    res1 = recommender.recommend(test_user_1, top_n=4)
    print("="*60)
    print("TEST CASE 1: 22yo Male, Friends, Winter")
    print("Predicted Category Affinities:", res1["predicted_affinities"])
    print("Top Recommendations:")
    for d in res1["top_recommendations"]:
        print(f"  • {d['Name']} ({d['State']}) | {d['Category']} | Match: {d['Match_Percentage']}% | {d['Seasonal_Status']}")
        
    # Test case 2: 58-year-old traveler with Family in Winter
    test_user_2 = {
        "Age": 58,
        "Gender": "Female",
        "Income_Level": "High",
        "Spending_Amount": 4500.0,
        "Avg_Trip_Duration": 8,
        "Travel_Group_Type": "Family",
        "Travel_Season": "Winter"
    }
    
    res2 = recommender.recommend(test_user_2, top_n=4)
    print("\n" + "="*60)
    print("TEST CASE 2: 58yo Female, Family, Winter")
    print("Predicted Category Affinities:", res2["predicted_affinities"])
    print("Top Recommendations:")
    for d in res2["top_recommendations"]:
        print(f"  • {d['Name']} ({d['State']}) | {d['Category']} | Match: {d['Match_Percentage']}% | {d['Seasonal_Status']}")
