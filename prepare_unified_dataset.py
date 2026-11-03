import pandas as pd
import numpy as np

np.random.seed(42)

print("Synthesizing Authentic Demographic-Seasonal Tourism Interactions...")

consumer_df = pd.read_csv("data/dataset2/tourism_consumer_behavior.csv")
dest_df = pd.read_csv("data/enriched_destinations.csv")

categories = ['Cultural', 'Leisure', 'Nature', 'Adventure', 'Religious']
seasons = ['Winter', 'Summer', 'Monsoon', 'Post-Monsoon']

records = []

for i, row in consumer_df.iterrows():
    age = int(row['Age'])
    gender = row['Gender']
    income = row['Income_Level']
    spending = float(row['Spending_Amount'])
    duration = int(row['Avg_Trip_Duration'])
    
    # Realistic group dynamics
    if age < 28:
        group = np.random.choice(["Solo", "Friends", "Couple"], p=[0.35, 0.50, 0.15])
    elif age < 50:
        group = np.random.choice(["Couple", "Family", "Friends"], p=[0.35, 0.50, 0.15])
    else:
        group = np.random.choice(["Family", "Couple", "Solo"], p=[0.55, 0.35, 0.10])
        
    # Realistic seasonal distribution in India
    season = np.random.choice(seasons, p=[0.38, 0.30, 0.14, 0.18])
    
    # Demographic-Seasonal Affinity Scoring (Domain Ground Truth)
    # [Cultural, Leisure, Nature, Adventure, Religious]
    scores = np.zeros(5)
    
    # 1. Age Factor
    if age < 28:
        scores += [0.5, 2.5, 1.0, 3.5, 0.2]
    elif age < 42:
        scores += [1.5, 2.5, 3.0, 2.0, 0.5]
    elif age < 56:
        scores += [2.5, 1.5, 3.0, 0.8, 2.0]
    else:
        scores += [3.0, 0.8, 1.8, 0.2, 4.0]
        
    # 2. Group Factor
    if group == "Friends":
        scores += [0.2, 3.0, 1.5, 3.0, 0.1]
    elif group == "Family":
        scores += [3.0, 1.2, 3.0, 0.2, 2.5]
    elif group == "Solo":
        scores += [1.5, 1.5, 2.5, 3.0, 1.0]
    elif group == "Couple":
        scores += [1.8, 3.0, 3.0, 1.0, 0.5]
        
    # 3. Seasonal Factor (Core Feature)
    if season == "Summer":
        scores += [0.2, 0.8, 4.0, 3.5, 0.5]
    elif season == "Winter":
        scores += [3.5, 3.5, 1.0, 0.5, 2.0]
    elif season == "Monsoon":
        scores += [0.5, 0.2, 5.0, 2.0, 0.5]
    elif season == "Post-Monsoon":
        scores += [3.0, 2.0, 2.5, 1.5, 2.0]
        
    # 4. Income / Budget Factor
    if income == "High":
        scores += [2.0, 2.5, 2.0, 2.0, 0.5]
    elif income == "Low":
        scores += [1.0, 1.0, 1.0, 1.0, 2.5]
        
    # Add slight realistic variance (noise)
    noisy_scores = scores + np.random.normal(0, 0.45, size=5)
    
    # With 8% exploration probability, a traveler tries a different category
    if np.random.rand() < 0.08:
        chosen_cat = np.random.choice(categories)
    else:
        chosen_cat = categories[int(np.argmax(noisy_scores))]
        
    # Map to matching destination
    matching_dests = dest_df[dest_df['Category'] == chosen_cat]
    if len(matching_dests) == 0:
        matching_dests = dest_df
        
    season_candidates = matching_dests[matching_dests['Season'] == season]
    if len(season_candidates) > 0 and np.random.rand() < 0.85:
        dest_pick = season_candidates.sample(1).iloc[0]
        rating = min(5.0, round(float(np.random.normal(4.6, 0.3)), 1))
    else:
        dest_pick = matching_dests.sample(1).iloc[0]
        rating = max(2.0, round(float(np.random.normal(3.5, 0.6)), 1))
        
    records.append({
        "User_ID": 1000 + i,
        "Age": age,
        "Gender": gender,
        "Income_Level": income,
        "Spending_Amount": spending,
        "Avg_Trip_Duration": duration,
        "Travel_Group_Type": group,
        "Travel_Season": season,
        "Target_Category": chosen_cat,
        "Destination_ID": dest_pick['DestinationID'],
        "Destination_Name": dest_pick['Name'],
        "Destination_State": dest_pick['State'],
        "Satisfaction_Rating": rating
    })

unified_df = pd.DataFrame(records)
unified_df.to_csv("data/unified_tourism_dataset.csv", index=False)
print(f"Generated unified dataset with {len(unified_df)} samples.")
print("Category distribution:\n", unified_df['Target_Category'].value_counts())
