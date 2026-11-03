# Demographic & Seasonal-Based Tourism Recommender System

An intelligent, context-aware tourism recommendation engine powered by a **KNN-Based Stacking Ensemble Machine Learning Architecture**, scaling the foundational methodology of **Marzuki et al. (2025)** to a nationwide catalog across all Indian States and Union Territories.

---

## 🌟 Key Highlights & Novel Contributions
* **KNN-Stacking Ensemble Architecture:** Integrates multi-scale $k$-Nearest Neighbors base learners ($k=3, 5, 7, 9$) with Random Forest, synthesized via a **Logistic Regression** meta-classifier to eliminate hyperparameter sensitivity.
* **Real-Time Live Ground Telemetry & Hazard Intelligence:** Live meteorological queries via Open-Meteo for real-time temperature, precipitation, wind speed, and terrain-specific risk alerts (mountain landslide hazard, thunderstorm warnings, extreme heat advisories, and coastal surf advisories).
* **Explainable AI (XAI) Attribution Breakdown:** Transparent 4-factor scoring on each destination card (Demographic Fit, Seasonal Alignment, Budget Compatibility, and Historical Popularity).
* **Dynamic Day-by-Day Itinerary Planner:** Synthesizes an intelligent, customized day-by-day travel schedule tailored to the traveler's exact trip duration (2 to 10 days) and companion group.
* **Smart Financial Budget Decomposition:** Decomposes user spending into itemized allocations: Accommodation (40%), Transit (25%), Dining (20%), and Sightseeing (15%) with automated financial feasibility status.
* **4 Indian Travel Seasons:** Incorporates dynamic seasonal context (Winter, Summer, Monsoon, Post-Monsoon) to prevent out-of-season recommendations.
* **National Catalog Scope:** Scaled from the base paper's 14 local municipal spots to **175+ curated Indian tourist destinations** with GPS coordinates across all Indian States & UTs.
* **Interactive Full-Stack Web Application:** Built with Flask, vanilla JavaScript, responsive modern CSS UI, and REST API endpoints.

---

## 📊 Benchmark Evaluation Results

Evaluated on the unified demographic dataset using 80/20 stratified splitting and cross-validation:

| Model / Algorithm | Accuracy (%) | Precision (%) | Recall (%) | F1-Score (%) |
| :--- | :---: | :---: | :---: | :---: |
| **KNN Stacking Ensemble (Proposed)** | **85.98%** | **86.06%** | **85.98%** | **85.62%** |
| Random Forest | 85.57% | 85.81% | 85.57% | 84.90% |
| Decision Tree (CART) | 85.37% | 85.34% | 85.37% | 85.25% |
| Baseline KNN ($k=5$) | 77.03% | 77.52% | 77.03% | 76.36% |

---

## 📂 Repository Structure

```
├── app.py                            # Flask web application server & REST APIs
├── recommender_engine.py             # Core hybrid recommendation inference engine
├── weather_service.py                # Real-time meteorological telemetry & hazard alerts
├── itinerary_service.py              # Dynamic day-by-day planner & budget decomposition
├── train_knn_stacking.py             # Machine learning training pipeline & evaluation
├── prepare_unified_dataset.py        # Dataset merging & preprocessing pipeline
├── expand_catalog_150.py             # Catalog generator (175+ Indian destinations)
├── test_client.py                    # Verification script for recommendation API
├── BASE_PAPER_AND_LITERATURE_SURVEY.md # Detailed academic review of base & related papers
├── marzuki_base_paper.pdf            # Original reference paper (Marzuki et al., 2025)
├── models/
│   ├── stacking_model.pkl            # Trained StackingClassifier model
│   ├── preprocessor.pkl              # Feature scaling and encoding pipeline
│   └── evaluation_results.csv        # Benchmark metrics across models
├── data/
│   ├── enriched_destinations.csv     # 175+ destination catalog with metadata
│   └── unified_tourism_dataset.csv   # Unified traveler interaction dataset
├── templates/
│   └── index.html                    # Frontend user interface
└── static/
    ├── css/style.css                 # Custom modern styling & animations
    └── js/app.js                     # Dynamic client-side application logic
```

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.9+ (Tested on Python 3.13)
* Git

### 2. Installation
Clone the repository:
```bash
git clone https://github.com/kartikM2005/DemographicBasedTourismRecommender.git
cd DemographicBasedTourismRecommender
```

Install required dependencies:
```bash
pip install flask pandas numpy scikit-learn
```

### 3. Running the Application
Launch the Flask development server:
```bash
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

### 4. Retraining the ML Pipeline (Optional)
To retrain the KNN-Stacking ensemble model and reproduce the evaluation benchmarks:
```bash
python train_knn_stacking.py
```

---

## 📡 REST API Reference

### `POST /api/recommend`
Generates top-$N$ personalized tourist recommendations.

**Request Payload:**
```json
{
  "Age": 28,
  "Gender": "Female",
  "Income_Level": "Medium",
  "Spending_Amount": 2500,
  "Avg_Trip_Duration": 5,
  "Travel_Group_Type": "Friends",
  "Travel_Season": "Winter",
  "top_n": 5
}
```

**Response Example:**
```json
{
  "status": "success",
  "data": {
    "primary_recommended_category": "Adventure",
    "top_recommendations": [
      {
        "Name": "Auli Ski Slopes & Ropeway",
        "State": "Uttarakhand",
        "Category": "Adventure",
        "BestTimeToVisit": "Nov-Mar",
        "Match_Percentage": 96.8,
        "Seasonal_Status": "Optimal Season (Peak Experience)"
      }
    ]
  }
}
```

---

## 📖 Academic Base Reference
* **Paper:** *A KNN-Based Stacking for Tourism Destination Recommender System Based on User Demographic Data*  
* **Authors:** I. Marzuki, D. Hindarto, F. N. Fiqri, N. Nurhidayati, Y. M. Arif, R. F. Rachmadi, M. Hariadi  
* **Journal:** *International Journal of Intelligent Engineering and Systems* (IJIES), Vol. 18, No. 4, pp. 219–232, 2025.  
* **DOI:** [10.22266/ijies2025.0531.14](https://doi.org/10.22266/ijies2025.0531.14)

