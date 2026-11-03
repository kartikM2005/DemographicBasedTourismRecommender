import pandas as pd
import os

files = {
    "Expanded_Destinations": "data/dataset1/Expanded_Destinations.csv",
    "Final_Updated_Expanded_Users": "data/dataset1/Final_Updated_Expanded_Users.csv",
    "Final_Updated_Expanded_Reviews": "data/dataset1/Final_Updated_Expanded_Reviews.csv",
    "Final_Updated_Expanded_UserHistory": "data/dataset1/Final_Updated_Expanded_UserHistory.csv",
    "tourism_consumer_behavior": "data/dataset2/tourism_consumer_behavior.csv"
}

print("="*60)
for name, path in files.items():
    print(f"\n--- {name} ({path}) ---")
    if os.path.exists(path):
        df = pd.read_csv(path)
        print(f"Shape: {df.shape}")
        print("Columns & Types:")
        for col in df.columns:
            sample_vals = df[col].dropna().unique()[:3].tolist()
            print(f"  • {col} ({df[col].dtype}): {sample_vals}")
    else:
        print("File not found!")
print("="*60)
