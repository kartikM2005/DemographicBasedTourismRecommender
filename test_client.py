import urllib.request
import json

payload = {
    "Age": 45,
    "Gender": "Female",
    "Income_Level": "Medium",
    "Spending_Amount": 3000,
    "Avg_Trip_Duration": 7,
    "Travel_Group_Type": "Family",
    "Travel_Season": "Summer",
    "top_n": 5
}

data = json.dumps(payload).encode()
req = urllib.request.Request("http://127.0.0.1:5000/api/recommend", data=data, headers={"Content-Type": "application/json"})
res = urllib.request.urlopen(req)

result = json.loads(res.read())
recs = result["data"]["top_recommendations"]
print(f"Top 5 Recommendations for 45yo Family in Summer (out of 175 destinations):")
for r in recs:
    print(f"  • {r['Name']} ({r['State']}) | {r['Category']} | Match: {r['Match_Percentage']}%")
