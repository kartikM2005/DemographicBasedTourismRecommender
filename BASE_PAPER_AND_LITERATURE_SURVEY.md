# Base Paper Review & Comparative Literature Survey
**Project Title:** Demographic & Seasonal Based Tourism Recommender System  
**Department:** Department of Computer Science & Engineering, SDMCET  
**Date:** November 2026  

---

## 1. Base Paper: Comprehensive Analysis

### 1.1 Bibliographic Details
* **Title:** *A KNN-Based Stacking for Tourism Destination Recommender System Based on User Demographic Data*
* **Authors:** Imam Marzuki, Djarot Hindarto, Fahmi Noor Fiqri, Nurhidayati, Yunifa Miftachul Arif, Reza Fuad Rachmadi, and Mochamad Hariadi
* **Journal:** *International Journal of Intelligent Engineering and Systems* (IJIES), Vol. 18, No. 4, pp. 219–232 (2025)
* **Publisher:** Intelligent Networks and Systems Society (INASS)
* **DOI:** [10.22266/ijies2025.0531.14](https://doi.org/10.22266/ijies2025.0531.14)
* **Publication Date:** Received: January 6, 2025; Revised: March 5, 2025; Published: 2025

---

### 1.2 Base Paper Methodology
The authors designed a 6-phase recommendation framework:

$$\text{Data Collection} \longrightarrow \text{Preprocessing \& Encoding} \longrightarrow \text{Feature Selection (ANOVA)} \longrightarrow \text{KNN-Based Stacking} \longrightarrow \text{Prediction} \longrightarrow \text{10-Fold CV Evaluation}$$

1. **Data Collection Stage:**
   * Administered structured questionnaires to **1,000 tourist respondents** visiting Batu City, East Java, Indonesia.
   * Captured personal experiences, past visited spots, demographic traits, and motivations for destination selection.
2. **Preprocessing & Categorical Encoding:**
   * Data cleaning, standardization, and missing-value handling.
   * **Label Encoding:** Converted all categorical features into numerical representations via:
     $$f(x) = i \quad \text{where } x = x_i \text{ and } i \in [0, c-1]$$
     where $c$ is the total count of distinct categorical classes.
3. **Feature Selection (One-Way ANOVA):**
   * Applied Analysis of Variance (ANOVA) to identify which demographic variables have statistically significant variance differences relative to tourist destination preferences:
     $$F = \frac{\text{MSB}}{\text{MSW}} = \frac{\text{SSB} / (k - 1)}{\text{SSW} / (N - k)}$$
   * Irrelevant or low-significance attributes were eliminated to reduce dimensionality.
4. **Model Architecture (KNN-Based Stacking):**
   * **Level-0 (Base Learners):** Multiple K-Nearest Neighbors (KNN) models configured with different neighborhood hyperparameters ($k = 10, 15, 20$) using Euclidean distance:
     $$d(p, q) = \sqrt{\sum_{i=1}^n (p_i - q_i)^2}$$
     Multiple $k$ values allow the model to capture both tight local demographic clusters ($k=10$) and wider demographic trends ($k=20$).
   * **Level-1 (Meta-Learner):** **Logistic Regression** trained on the predictive probability distributions output by the base KNN learners. This meta-model learns the optimal weighting across the different $k$ perspectives, effectively eliminating hyperparameter sensitivity.
5. **Validation Scheme:**
   * **10-Fold Cross-Validation** was used across the 1,000 samples to prevent overfitting and guarantee objective evaluation.
6. **Evaluation Pipeline:**
   * Evaluated via a multi-class Confusion Matrix using Accuracy, Precision, Recall, and F1-Score:
     $$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}, \quad \text{Precision} = \frac{TP}{TP + FP}$$
     $$\text{Recall} = \frac{TP}{TP + FN}, \quad \text{F1-Score} = \frac{2 \times (\text{Precision} \times \text{Recall})}{\text{Precision} + \text{Recall}}$$

---

### 1.3 Features Used in the Base Paper

#### A. Input Demographic & Behavioral Features ($X_1$ to $X_{10}$)
| Code | Feature Attribute | Feature Values / Categories in Paper |
| :--- | :--- | :--- |
| **$X_1$** | **Home Area** | Rural, Suburban, Urban |
| **$X_2$** | **Age** | 7–11, 12–25, 26–45, > 45 |
| **$X_3$** | **Gender** | Female, Male |
| **$X_4$** | **Hobby** | Gaming, Hiking, Photography, Reading, Swimming, Travelling |
| **$X_5$** | **Marital Status** | Single, Married |
| **$X_6$** | **Education** | Elementary School, High School, College |
| **$X_7$** | **Work / Occupation** | Student, Civil Servant, Entrepreneurship, Private Employees |
| **$X_8$** | **Travel Frequency (Last Year)** | Never, Rarely (1–2x), Occasionally (3–5x), Frequently (6–10x), Very Frequently (>10x) |
| **$X_9$** | **Types of Tourism Visited** | Adventure, Culinary, Cultural, Nature, Urban |
| **$X_{10}$** | **Reason for Travelling** | Business, Education, Family Visit, Health, Recreation, Others |

#### B. Target Output Classes ($Y_1$ to $Y_{14}$)
The target classes were **14 specific tourist attractions in Batu City, Indonesia**:
1. Jatim Park 1 ($Y_1$)
2. Jatim Park 2 ($Y_2$)
3. Jatim Park 3 ($Y_3$)
4. Museum Angkut ($Y_4$)
5. Selecta ($Y_5$)
6. Batu Night Spectacular / BNS ($Y_6$)
7. Eco Green Park ($Y_7$)
8. Alun-Alun Kota Batu ($Y_8$)
9. Kusuma Agro ($Y_9$)
10. Cangar Hot Springs ($Y_{10}$)
11. Coban Talun Waterfall ($Y_{11}$)
12. Pemandian Songgoriti ($Y_{12}$)
13. Coban Rais Waterfall ($Y_{13}$)
14. Predator Fun Park ($Y_{14}$)

---

### 1.4 Accuracies & Performance Benchmarking Met

The authors evaluated their KNN-Based Stacking architecture against individual standalone classifiers on their dataset:

| Model / Algorithm | Accuracy (%) | Precision (%) | Recall (%) | F1-Score (%) |
| :--- | :---: | :---: | :---: | :---: |
| **KNN-Based Stacking (Proposed)** | **86.89%** | **87.18%** | **86.89%** | **86.93%** |
| **KNN ($k = 15$)** | 86.53% | 86.98% | 86.53% | 86.59% |
| **KNN ($k = 20$)** | 86.43% | 86.90% | 86.43% | 86.49% |
| **KNN ($k = 10$)** | 86.06% | 86.38% | 86.06% | 86.08% |
| **Random Forest** | 86.09% | 86.33% | 86.09% | 86.15% |
| **Naïve Bayes** | 84.18% | 84.21% | 84.18% | 84.17% |
| **CART (Decision Tree)** | 83.49% | 83.40% | 83.49% | 83.40% |
| **SVM (Support Vector Machine)** | 80.35% | 81.97% | 80.35% | 80.54% |

**Key Academic Insight:** Standalone KNN suffers from extreme sensitivity to neighborhood size selection ($k$), while standard decision trees (CART) and SVM overfit or struggle with mixed categorical demographics. Combining multiple KNN neighborhood sizes via a Logistic Regression meta-classifier yields higher accuracy (**86.89%**) and balanced precision/recall.

---

### 1.5 Critical Limitations of the Base Paper
*(Use these exact points when explaining the project rationale to your guide)*

1. **Severe Geographic & Catalog Constraint:**
   * The scope is restricted to **only 14 attractions in Batu City, Indonesia**. It cannot generalize to regional, state-wide, or national tourism markets.
2. **Small, Offline Questionnaire Dataset:**
   * Relies on only **1,000 survey responses**. Questionnaire responses are susceptible to respondent recall bias and do not reflect continuous, real-time traveler behavior.
3. **No Contextual or Temporal Awareness (Zero Seasonality/Weather):**
   * The model assumes traveler preferences are static 365 days a year. It completely ignores weather, monsoons, summer heatwaves, or winter snow seasons, which are critical drivers in real tourism decisions.
4. **Absence of Financial & Operational Constraints:**
   * Key real-world travel limitations such as budget brackets, accommodation spending, trip duration (short weekend vs. extended holiday), and travel group composition (solo vs. family with children) were not incorporated.
5. **Classification vs. Recommendation Limitation:**
   * The paper models recommendation as a **flat multi-class classification** (predicting a binary match for a destination). Real-world travelers require a **Ranked Top-$N$ List** with similarity match percentages and personalized explanations.
6. **High Demographic Collinearity & Regional Bias:**
   * In their dataset, Age and Education showed an extreme negative correlation ($-0.98$), which was an artifact of the specific local sample and does not represent global or diverse traveler demographics.
7. **Cold-Start for New Destinations:**
   * New destinations cannot be introduced into the system without administering a completely new round of questionnaires for that specific location.

---

## 2. Comparison: Base Paper vs. Your Implemented System

| Feature Dimension | Base Paper (Marzuki et al., 2025) | Your Major Project System |
| :--- | :--- | :--- |
| **Geographic Coverage** | 14 local spots in 1 city (Batu City) | **175+ curated destinations across all Indian States & UTs** |
| **Seasonal Context** | None (Static year-round) | **4 Indian Seasons:** Summer, Monsoon, Post-Monsoon, Winter |
| **Financial Profiling** | None (No budget or expenditure data) | **Budget Tiers:** Low, Medium, High + Spending Amount tracking |
| **Group Dynamics** | None (Individual respondent only) | **Travel Groups:** Solo, Couple, Family, Friends |
| **Trip Duration** | Not considered | **Explicit Duration Tracking (Days)** |
| **Algorithmic Core** | KNN-Stacking ($k=10, 15, 20$ + Logistic Regression) | **KNN Stacking Pipeline + Distance Metric Weights + Content Matching** |
| **Recommendation Output** | Single destination class label | **Ranked Top-$N$ Itinerary with Dynamic Match % & Explanations** |
| **System Delivery** | Offline academic paper script | **Full-Stack Web Application with REST API** (`app.py`) |

---

## 3. Closely Related Literature Survey (2023–2025)

### Paper 1: Data-Driven Machine Learning Tourist Profiling
* **Title:** *Personalized Tourist Recommender System: A Data-Driven and Machine-Learning Approach*
* **Authors:** D. Shrestha, T. Wenan, D. Shrestha, N. Rajkarnikar, S.-R. Jeong
* **Journal:** *Computation* (MDPI), Vol. 12, No. 3, Art. no. 59 (2024)
* **DOI:** [10.3390/computation12030059](https://doi.org/10.3390/computation12030059)
* **Relevance:** Demonstrates how detailed demographic profiling combined with machine learning (Random Forest, Gradient Boosting) improves destination recommendation accuracy over conventional heuristic systems.
* **Methodology:** Multi-sub-model architecture processing user profiles, destination database, and decision logic for Pokhara, Nepal.
* **Dataset:** 2,400 tourists answering 125 questionnaire variables.
* **Performance:** ROC AUC $> 0.88$, high Lift curve metrics; outperformed Google Maps and TripAdvisor generic ranking.
* **Limitations:** 125 survey variables cause severe user fatigue; static dataset with no dynamic seasonal awareness.

---

### Paper 2: Hybrid Demographic & Collaborative Filtering
* **Title:** *Smart Tourism Recommender System Modeling Based on Hybrid Technique and Content Boosted Collaborative Filtering*
* **Authors:** C. Huda, Y. Heryadi, Lukas, W. Budiharto
* **Journal:** *IEEE Access*, Vol. 12, pp. 131794–131808 (2024)
* **DOI:** [10.1109/ACCESS.2024.3435160](https://doi.org/10.1109/ACCESS.2024.3435160)
* **Relevance:** Validates using Demographic Filtering (DF) specifically to eliminate the **Cold-Start Problem** when new users enter a tourism platform without prior interaction history.
* **Methodology:** Fuses Demographic Filtering (DF), User-Based Collaborative Filtering (UBCF), Content-Boosted Filtering (CBCF), and NLP Aspect-Based Sentiment Analysis.
* **Dataset:** Multi-source destination metadata + user rating logs + text reviews.
* **Performance:** Substantially lowered error rates: **MAE = 0.62**, **RMSE = 0.81** (compared to standalone CF $> 1.12$).
* **Limitations:** Heavy computational burden requiring active user text reviews and dense interaction matrices.

---

### Paper 3: Real-Time Context-Aware Environmental Recommendation (R2Tour)
* **Title:** *Real-Time Context-Aware Recommendation System for Tourism (R2Tour)*
* **Authors:** JunHo Yoon and Chang Choi
* **Journal:** *Sensors* (MDPI), Vol. 23, No. 7, Art. no. 3679 (2023)
* **DOI:** [10.3390/s23073679](https://doi.org/10.3390/s23073679)
* **Relevance:** Direct academic proof that coupling **demographic variables (Age, Gender)** with **dynamic temporal/environmental factors (Weather, Temperature)** dramatically enhances recommendation precision.
* **Methodology:** Evaluated 6 ML algorithms (including KNN, SVM, and MLP) to generate real-time ranked Top-5 attraction recommendations on Jeju Island, South Korea.
* **Dataset:** Tourist movement tracks paired with meteorological weather records.
* **Performance:** Reached **77.30% Accuracy** and **0.773 Micro-F1** under real-time weather constraints.
* **Limitations:** Micro-scale radius focus (immediate nearby spots within kilometers) rather than comprehensive vacation or holiday destination itinerary planning.

---

### Paper 4: Multi-Level Demographic & Group Dynamics
* **Title:** *A Multi-Level Tourism Destination Recommender System*
* **Authors:** H. Alrasheed, A. Alzeer, A. Alhowimel, N. Shameri, A. Althyabi
* **Journal:** *Procedia Computer Science* (Elsevier), Vol. 170, pp. 333–340 (2020/2021)
* **DOI:** [10.1016/j.procs.2020.03.047](https://doi.org/10.1016/j.procs.2020.03.047)
* **Relevance:** Directly explores the multi-attribute demographic constraints utilized in our system: **Group Dynamics (Family vs. Solo vs. Friends)** and **Budget Brackets**.
* **Methodology:** Multi-layer constraint satisfaction and hierarchical similarity filtering.
* **Dataset:** Multi-category destination repository evaluated with traveler user groups.
* **Performance:** $>82\%$ user satisfaction rating for multi-attribute group travel matching.
* **Limitations:** Uses rule-based heuristic trees rather than machine learning models that adapt to non-linear patterns.

---

### Paper 5: Sequential & POI Contextual Modeling
* **Title:** *A BERT-Based Sequential POI Recommender System in Social Media*
* **Authors:** A. Noorian
* **Journal:** *Computer Standards & Interfaces* (Elsevier), Vol. 87, Art. no. 103766 (2024)
* **DOI:** [10.1016/j.csi.2023.103766](https://doi.org/10.1016/j.csi.2023.103766)
* **Relevance:** Examines deep learning representations of user demographic and sequential context for points of interest (POI).
* **Methodology:** Transformer/BERT-based sequential POI recommendation incorporating contextual check-in logs.
* **Dataset:** Evaluated on benchmark Yelp and Flickr social media check-in datasets.
* **Performance:** Outperformed traditional Markov Chains and RNNs in Recall@K and NDCG@K.
* **Limitations:** Black-box architecture requiring millions of check-in traces; computationally impractical for real-time edge or lightweight web deployment.

---

## 4. Master Comparative Literature Survey Matrix

| # | Research Paper & Citation | Key Methodology / Model | Demographic Attributes Used | Context / Seasonality | Scope of Destinations | Reported Benchmark Performance | Key Limitation Addressed by Our Project |
| :-: | :--- | :--- | :--- | :---: | :--- | :--- | :--- |
| **1** | **Marzuki et al. (2025)**<br>*IJIES (INASS)*<br>**[BASE PAPER]** | KNN-Stacking ($k=10, 15, 20$) + Logistic Regression | Age, Gender, Education, Job, Hobby | ❌ None (Static) | 14 local spots (Batu City) | **Accuracy: 86.89%**<br>Precision: 87.18%<br>Recall: 86.89%<br>F1: 86.93% | Confined to 14 spots in one town; no temporal/seasonal context; single-class output. |
| **2** | **Shrestha et al. (2024)**<br>*Computation (MDPI)* | Random Forest, Gradient Boosting | Age, Gender, Group, Budget | ❌ None | City-wide (Pokhara) | ROC AUC $> 0.88$<br>High Lift curves | 125 questionnaire features cause severe user onboarding friction. |
| **3** | **Huda et al. (2024)**<br>*IEEE Access* | Hybrid DF + UBCF + Sentiment Analysis | Age, Gender, Origin | ❌ None | Regional | MAE: 0.62<br>RMSE: 0.81 | Requires extensive historical rating matrices and text reviews. |
| **4** | **Yoon & Choi (2023)**<br>*Sensors (MDPI)*<br>*(R2Tour)* | Context-Aware KNN & SVM | Age, Gender | ✔ Weather, Temp, Distance | Localized (Jeju Island) | **Accuracy: 77.30%**<br>Micro-F1: 0.773 | Short-range radius filter only; lacks nationwide holiday travel planning scope. |
| **5** | **Alrasheed et al. (2021)**<br>*Procedia Comp. Sci.* | Multi-Level Hierarchical Rule Filtering | Age, Group Type, Budget | ❌ None | Regional | $>82\%$ User Satisfaction | Static heuristic hierarchy; lacks predictive machine learning generalization. |
| **6** | **Our Proposed System**<br>*(SDMCET 2026-27)* | **KNN-Stacking Ensemble + Hybrid Scoring Engine** | **Age, Gender, Income/Budget, Group Type, Duration** | **✔ 4 Indian Seasons (Winter, Summer, Monsoon, Post-Monsoon)** | **175+ Curated Destinations across India** | **Stacking Accuracy: 85.98%**<br>Ranked Top-$N$ with Match % | **Overcomes base paper limitations by scaling to nationwide catalog, 4 seasons, budget constraints, and interactive web deployment.** |

---
*Document prepared for academic guide review, VII Semester Major Project, SDMCET.*

