# Context-Aware and Explainable Tourism Recommendation Using a KNN-Based Stacking Ensemble with Seasonal and Real-Time Meteorological Telemetry

**Target Publication Venue:** Annals of Computer Science and Information Systems (ACSIS) / FedCSIS Conference Proceedings  
**Document Format:** IEEE 2-Column Academic Paper Specification  
**Indexing:** Scopus, Web of Science (CPCI), DBLP, DOAJ, IEEE Xplore  
**Authors:**
* **Kartik Magadum** (USN: 2SD23CS044) — *Dept. of Computer Science & Engineering, SDM College of Engineering & Technology, Dharwad, India*
* **Kumar M** (USN: 2SD23CS050) — *Dept. of Computer Science & Engineering, SDM College of Engineering & Technology, Dharwad, India*
* **Madan Gowda G B** (USN: 2SD23CS051) — *Dept. of Computer Science & Engineering, SDM College of Engineering & Technology, Dharwad, India*
* **Zahid Rashid Bhat** (USN: 2SD23CS129) — *Dept. of Computer Science & Engineering, SDM College of Engineering & Technology, Dharwad, India*
* *Under the Guidance of:* **Prathap Kumar M K†** — *Assistant Professor, Dept. of Computer Science & Engineering, SDM College of Engineering & Technology, Dharwad, India*

---

## Abstract
Personalized tourism recommender systems traditionally depend on historical interaction logs or collaborative filtering matrices, frequently failing under cold-start conditions and ignoring temporal context. While recent studies demonstrate the efficacy of demographic-driven stacking, existing models remain constrained to static local spots without seasonal adaptability, financial feasibility, or transparency. This study proposes an intelligent context-aware tourism recommendation framework using a K-Nearest Neighbors (KNN) stacking ensemble. The system integrates demographic profiling with four Indian seasonal contexts, real-time meteorological hazard telemetry via live weather APIs, and an Explainable AI (XAI) multi-factor attribution mechanism. Evaluated across 175 diverse destinations, the proposed meta-learner ensemble achieves an accuracy of 85.98%, precision of 86.06%, and F1-score of 85.62%, outperforming standalone KNN, CART, and Random Forest baselines. Coupled with numerical budget decomposition and dynamic day-by-day itinerary synthesis, the proposed architecture delivers an explainable and reliable decision-support system for nationwide tourism.

**Keywords:** Tourism Recommender Systems, Stacking Ensemble, Demographic Filtering, Context-Aware Recommender Systems, Explainable AI, Meteorological Telemetry.

---

## I. INTRODUCTION

The exponential expansion of global tourism and digital travel services has exacerbated information overload for prospective travelers. Tourists must continuously evaluate multidimensional variables, including personal interests, destination seasonality, geographical accessibility, and monetary constraints [1]. Although Collaborative Filtering (CF) and Content-Based Filtering (CBF) represent conventional paradigms in recommender systems, they exhibit severe shortcomings in tourist destination planning [2]. CF techniques suffer from severe data sparsity and the classical cold-start problem, wherein reliable recommendations cannot be formulated for new users devoid of explicit historical rating records [3]. Furthermore, conventional travel recommenders operate under static assumptions, treating destination appeal as time-invariant and detached from meteorological phenomena and seasonal transitions [4].

Recently, Marzuki et al. [5] demonstrated that user demographic attributes (such as age, occupation, and travel frequency) combined with a K-Nearest Neighbors (KNN) stacking ensemble could predict tourist attraction preferences with 86.89% accuracy. However, their experimental design was strictly restricted to 14 localized attractions in Batu City, Indonesia, and relied exclusively on static survey records. In practical scenarios, travelers require recommendations that account for seasonal weather extremes (e.g., Indian monsoons vs. winter travel), precise monetary budget allocations, real-time safety advisories, and interpretable rationale [6], [7].

To resolve these fundamental limitations, this study presents a context-aware, explainable tourism recommendation framework. The major contributions of this work are fourfold:
1. **Nationwide Multi-State Scalability:** We expand the target catalog from local town-level attractions to 175+ curated destinations spanning all states and union territories of India across five dominant categories (Leisure, Nature, Adventure, Cultural, and Religious).
2. **Seasonal Context Modeling:** We formulate a contextual recommendation vector incorporating four distinct meteorological seasons (Winter, Summer, Monsoon, and Post-Monsoon), eliminating static bias.
3. **Explainable AI (XAI) Scoring Engine:** We implement a transparent multi-factor attribution scoring mechanism that decomposes destination match percentages into Demographic Affinity, Seasonal Alignment, Budget Compatibility, and Popularity metrics.
4. **Live Telemetry and Budget Optimization:** We integrate live meteorological APIs to compute real-time ground condition hazards (landslide risk, heatwaves, extreme precipitation) paired with numerical budget decomposition and dynamic day-by-day itinerary synthesis.

---

## II. RELATED WORK AND BASE PAPER ANALYSIS

### A. Tourism Recommender Systems
Recommender systems in the tourism sector have evolved through multiple algorithmic phases. Early architectures utilized demographic filtering (DF) to group users according to general socio-economic profiles [3]. While DF effectively circumvents user cold-start hurdles, pure demographic heuristics often lack granular personalization [2]. Huda et al. [8] addressed this by coupling demographic profiles with content-boosted collaborative filtering and aspect-based sentiment analysis, reducing rating error to an MAE of 0.62. Similarly, Shrestha et al. [9] leveraged gradient boosting and random forests over demographic questionnaires in Pokhara, Nepal, reporting an ROC-AUC above 0.88. Nevertheless, their approach required tourists to complete 125 questionnaire items, inducing substantial user friction.

Context-Aware Recommender Systems (CARS) incorporate environmental and temporal conditions into the prediction loop [4], [10]. Yoon and Choi [6] introduced R2Tour, validating that pairing tourist demographic attributes with real-time temperature and weather conditions significantly improved recommendation precision on Jeju Island (77.30% accuracy). However, their operational radius remained confined to local short-range travel rather than comprehensive vacation planning.

### B. Base Paper Benchmark: Marzuki et al. (2025)
In 2025, Marzuki et al. [5] proposed a KNN-based stacking ensemble for tourism destination recommendation. Their framework surveyed 1,000 respondents using 10 demographic attributes ($X_1$ to $X_{10}$), employed One-Way ANOVA for feature selection, and trained multiple base KNN classifiers configured with varying neighborhood sizes ($k \in \{10, 15, 20\}$) mapped to a Logistic Regression meta-learner. Their ensemble achieved 86.89% accuracy, outperforming standalone KNN (86.53%), Random Forest (86.09%), and CART Decision Trees (83.49%).

Despite its mathematical viability, critical analytical gaps remain in the base paper:
* **Severe Spatial Constraint:** Predictions were restricted to only 14 attractions in Batu City, Indonesia, preventing generalization to diverse tourism hubs.
* **Zero Seasonal Awareness:** The model assumed constant preference throughout the year, failing to capture weather-driven tourist migration patterns.
* **Absence of Financial Modeling:** Budgetary limitations, trip duration, and group travel dynamics (e.g., solo vs. family) were omitted.
* **Black-Box Single-Class Output:** The system output a single categorical class rather than a ranked Top-$N$ portfolio with explainable recommendation justification.

---

## III. PROPOSED SYSTEM ARCHITECTURE AND METHODOLOGY

The proposed framework operates via a pipelined architecture comprising demographic feature encoding, base-level classification, meta-learner stacking, and Explainable AI (XAI) multi-factor attribution.

### A. Demographic and Contextual Feature Encoding
Let the user profile be defined as an input vector:
$$\mathbf{u} = \left[ \text{Age}, \text{Gender}, \text{IncomeLevel}, \text{SpendingAmount}, \text{Duration}, \text{GroupType}, \text{Season} \right] \tag{1}$$

where categorical features are standardized via one-hot and integer ordinal mapping $f: X_j \to \mathbb{R}^d$. Numerical variables ($\text{Age}, \text{SpendingAmount}, \text{Duration}$) are normalized using standard z-score scaling:
$$z = \frac{x - \mu}{\sigma} \tag{2}$$
where $\mu$ and $\sigma$ denote the empirical mean and standard deviation of the respective feature dimensions across training splits.

### B. Base-Level Classifiers (Level-0)
To capture both localized non-parametric boundaries and hierarchical decision splits, Level-0 utilizes three heterogeneous base learners:
1. **K-Nearest Neighbors ($M_1$):** Configured with $k=5$ under Euclidean metric space:
   $$d(\mathbf{x}, \mathbf{x}') = \sqrt{\sum_{i=1}^n (x_i - x_i')^2} \tag{3}$$
2. **CART Decision Tree ($M_2$):** Evaluated using Gini impurity minimization:
   $$I_G(p) = 1 - \sum_{k=1}^C p_k^2 \tag{4}$$
3. **Random Forest Ensemble ($M_3$):** Composed of $B=100$ bootstrapped trees aggregating sub-space variance:
   $$P_{RF}(C_k \mid \mathbf{x}) = \frac{1}{B} \sum_{b=1}^B P_b(C_k \mid \mathbf{x}) \tag{5}$$

### C. Meta-Learner Stacking Formulation (Level-1)
Following stacked generalization theory [11], [12], the predictive class probability vectors generated by the base models serve as meta-features:
$$\mathbf{z}_i = \left[ \mathbf{P}_{M_1}(\mathbf{y} \mid \mathbf{x}_i), \mathbf{P}_{M_2}(\mathbf{y} \mid \mathbf{x}_i), \mathbf{P}_{M_3}(\mathbf{y} \mid \mathbf{x}_i) \right] \in \mathbb{R}^{3 \times C} \tag{6}$$

A regularized multi-class Logistic Regression model functions as the Level-1 meta-classifier:
$$P(Y = C_k \mid \mathbf{z}) = \frac{\exp(\mathbf{w}_k^T \mathbf{z} + b_k)}{\sum_{j=1}^C \exp(\mathbf{w}_j^T \mathbf{z} + b_j)} \tag{7}$$

Parameter optimization is achieved by minimizing the categorical cross-entropy loss with $L_2$ Tikhonov regularization:
$$\mathcal{L}(\mathbf{W}) = -\sum_{i=1}^N \sum_{k=1}^C y_{ik} \log P(Y = C_k \mid \mathbf{z}_i) + \frac{\lambda}{2} \|\mathbf{W}\|_2^2 \tag{8}$$

### D. Explainable AI (XAI) Multi-Factor Scoring Engine
Rather than delivering uninterpretable classifications, our architecture scores every candidate destination $d \in \mathcal{D}$ using a weighted four-factor transparent utility function:
$$\text{MatchScore}(u, d) = w_1 \cdot D_{\text{aff}} + w_2 \cdot S_{\text{align}} + w_3 \cdot B_{\text{compat}} + w_4 \cdot P_{\text{pop}} \tag{9}$$

subject to $\sum_{i=1}^4 w_i = 1.0$, empirically calibrated to $[0.35, 0.30, 0.20, 0.15]$.

* **Demographic Affinity ($D_{\text{aff}}$):** Derived directly from the meta-classifier's posterior probability for destination category $c_d$:
  $$D_{\text{aff}} = P(Y = c_d \mid \mathbf{z}_u) \times 100 \tag{10}$$
* **Seasonal Alignment ($S_{\text{align}}$):** Evaluates compatibility between intended travel season $s_u$ and destination peak period $s_d$:
  $$S_{\text{align}} = \begin{cases} 96.0\%, & \text{if } s_u = s_d \text{ (Peak Optimal)} \\ 82.0\%, & \text{if } s_u \text{ is adjacent shoulder season} \\ 60.0\%, & \text{if } s_u \text{ is off-peak/monsoon} \end{cases} \tag{11}$$
* **Budget Compatibility ($B_{\text{compat}}$):** Measures numerical proximity between user total budget $B_u$ and typical destination requirement $B_d$:
  $$B_{\text{compat}} = \max\left(40.0, 100.0 - \frac{|B_u - B_d|}{B_d} \times 50.0\right) \tag{12}$$
* **Popularity Normalization ($P_{\text{pop}}$):** Scaled user rating score $\frac{\text{Rating}}{10.0} \times 100$.

---

## IV. DYNAMIC TELEMETRY AND BUDGET OPTIMIZATION

### A. Real-Time Ground Weather and Terrain Hazard Alerts
A notable flaw in academic recommenders is recommending geographically valid spots during active natural hazards (e.g., hill stations during torrential cloudbursts). Our framework connects to Open-Meteo meteorological endpoints [13] via reverse-geocoded coordinates $(\text{Lat}_d, \text{Lon}_d)$. Real-time telemetry evaluates a localized hazard automaton:
$$\text{HazardLevel} = \begin{cases} \text{WARNING (Landslide Risk)}, & \text{if } c_d = \text{Nature} \land \text{Precip} \ge 7.0\text{ mm} \\ \text{WARNING (Heatwave Alert)}, & \text{if } T_{\text{ground}} \ge 39.5^\circ\text{C} \\ \text{ADVISORY (Coastal Gale)}, & \text{if } c_d = \text{Leisure} \land V_{\text{wind}} \ge 35\text{ km/h} \\ \text{SAFE (Optimal Climate)}, & \text{otherwise} \end{cases} \tag{13}$$

### B. Dynamic Day-by-Day Itinerary and Itemized Budget Split
To translate recommendations into actionable logistics, an itinerary synthesis engine decomposes total trip budget $B_u$ across user trip duration $T$ days:
* **Stays & Lodging:** $0.40 \times B_u$, with per-night allocation $\frac{0.40 B_u}{T-1}$.
* **Transit & Local Mobility:** $0.25 \times B_u$.
* **Dining & Regional Gastronomy:** $0.20 \times B_u$.
* **Sightseeing Passes & Activities:** $0.15 \times B_u$.

---

## V. EXPERIMENTAL EVALUATION AND RESULTS

### A. Dataset Formulation and Validation Protocol
The benchmark dataset comprises 175 thoroughly curated destination profiles across 28 Indian states and 8 union territories, spanning five target categories. User interactions were simulated using stratified demographic distributions mirroring real-world tourism surveys (age ranges 18–70, income tiers, travel group types, and four seasonal preferences).

Model validation employed stratified **10-Fold Cross-Validation** to ensure zero data leakage across evaluation folds. Performance metrics include Accuracy, Macro-Precision, Macro-Recall, and Macro-F1 score:
$$\text{Accuracy} = \frac{\sum_{k=1}^C TP_k}{N}, \quad \text{Precision} = \frac{1}{C}\sum_{k=1}^C \frac{TP_k}{TP_k + FP_k} \tag{14}$$
$$\text{Recall} = \frac{1}{C}\sum_{k=1}^C \frac{TP_k}{TP_k + FN_k}, \quad \text{F1} = \frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}} \tag{15}$$

### B. Comparative Model Benchmarks
The proposed KNN-Stacking ensemble was evaluated against individual standalone classifiers:

#### TABLE I. Performance Comparison of Recommender Classifiers
| Model / Algorithm | Accuracy (%) | Precision (%) | Recall (%) | F1-Score (%) |
| :--- | :---: | :---: | :---: | :---: |
| Baseline KNN ($k=5$) | 77.03 | 77.52 | 77.03 | 76.36 |
| CART Decision Tree | 85.37 | 85.34 | 85.37 | 85.25 |
| Random Forest ($B=100$) | 85.57 | 85.81 | 85.57 | 84.90 |
| **KNN-Stacking Ensemble (Proposed)** | **85.98** | **86.06** | **85.98** | **85.62** |

As documented in Table I, standalone KNN achieves 77.03% accuracy due to metric sensitivity in mixed demographic-categorical spaces. Decision Trees and Random Forests improve accuracy to 85.37% and 85.57%, respectively. The proposed KNN-Stacking ensemble achieves the highest overall accuracy (**85.98%**) and F1-score (**85.62%**), confirming that meta-learning across diverse decision boundaries effectively eliminates single-model variance.

### C. Comparison with the Base Paper
Table II contrasts our architectural attributes with the base benchmark of Marzuki et al. [5].

#### TABLE II. Architectural Benchmark: Base Paper vs. Proposed Framework
| Dimension | Marzuki et al. (2025) [5] | Proposed System |
| :--- | :--- | :--- |
| **Geographic Scope** | 14 spots (Batu City, Indonesia) | **175+ curated hubs (Pan-India)** |
| **Target Scope** | Municipal local level | **Nationwide multi-state** |
| **Temporal Awareness** | None (Static year-round) | **4 Indian Seasons** |
| **Real-Time Telemetry** | None | **Live Open-Meteo Weather API** |
| **Explainability** | Black-box single label | **4-Factor XAI Score Breakdown** |
| **Budget Optimization** | Absent | **Exact INR Itemized Decomposition** |
| **User Interface** | Offline script | **Full-Stack Web App + Leaflet Map** |

---

## VI. DISCUSSION AND SYSTEM IMPLEMENTATION

The algorithmic pipeline is fully deployed within a production-ready web application built on Flask, styled with responsive modern CSS, and backed by Leaflet.js interactive geospatial visualization. When a user configures their demographic profile (e.g., a 25-year-old solo traveler with a ₹25,000 budget in Winter), the system invokes the stacking model in sub-100ms inference time, populates top recommendations, overlays real-time weather telemetry, and plots categorized interactive pins across India. The explainability component allows tourists to inspect why a destination was recommended, substantially increasing user trust and adoption compared to conventional opaque recommendation engines [14], [15].

---

## VII. CONCLUSION AND FUTURE SCOPE

This paper presented a context-aware, explainable tourism recommender system powered by a KNN-based stacking ensemble. By addressing the critical limitations of Marzuki et al. (2025), our architecture successfully incorporates nationwide multi-state destinations, four seasonal contexts, live meteorological hazard alerts, Explainable AI attribution scoring, and numerical budget allocation. Rigorous empirical validation demonstrates an accuracy of 85.98% and an F1-score of 85.62%, outperforming standalone baselines.

Future work will explore integrating graph neural networks (GNNs) for multi-destination route chaining, transformer-based sequential check-in representations, and direct feedback reinforcement learning to continuously adapt to evolving traveler behaviors.

---

## Acknowledgment
The authors express their sincere gratitude to the Department of Computer Science and Engineering, SDM College of Engineering and Technology, Dharwad, for providing technical resources and laboratory facilities to conduct this research.

---

## References

1. J. Borràs, A. Moreno, and A. Valls, "Intelligent Tourism Recommender Systems: A Survey," *Expert Systems with Applications*, vol. 41, no. 16, pp. 7370–7389, 2014. [DOI: 10.1016/j.eswa.2014.04.028](http://dx.doi.org/10.1016/j.eswa.2014.04.028)
2. R. Burke, "Hybrid Recommender Systems: Survey and Experiments," *User Modeling and User-Adapted Interaction*, vol. 12, no. 4, pp. 331–370, 2002. [DOI: 10.1023/A:1021240730564](http://dx.doi.org/10.1023/A:1021240730564)
3. M. J. Pazzani, "A Framework for Collaborative, Content-Based and Demographic Filtering," *Artificial Intelligence Review*, vol. 13, no. 5, pp. 393–408, 1999. [DOI: 10.1023/A:1006544522159](http://dx.doi.org/10.1023/A:1006544522159)
4. G. Adomavicius and A. Tuzhilin, "Context-Aware Recommender Systems," in *Recommender Systems Handbook*, Springer, pp. 217–253, 2011. [DOI: 10.1007/978-0-387-85820-3_7](http://dx.doi.org/10.1007/978-0-387-85820-3_7)
5. I. Marzuki, D. Hindarto, F. N. Fiqri, Nurhidayati, Y. M. Arif, R. F. Rachmadi, and M. Hariadi, "A KNN-Based Stacking for Tourism Destination Recommender System Based on User Demographic Data," *International Journal of Intelligent Engineering and Systems*, vol. 18, no. 4, pp. 219–232, 2025. [DOI: 10.22266/ijies2025.0531.14](http://dx.doi.org/10.22266/ijies2025.0531.14)
6. J. Yoon and C. Choi, "Real-Time Context-Aware Recommendation System for Tourism (R2Tour)," *Sensors*, vol. 23, no. 7, p. 3679, 2023. [DOI: 10.3390/s23073679](http://dx.doi.org/10.3390/s23073679)
7. Y. Zhang and X. Chen, "Explainable Recommendation: A Survey and New Perspectives," *Foundations and Trends in Information Retrieval*, vol. 14, no. 1, pp. 1–101, 2020. [DOI: 10.1561/1500000066](http://dx.doi.org/10.1561/1500000066)
8. C. Huda, Y. Heryadi, Lukas, and W. Budiharto, "Smart Tourism Recommender System Modeling Based on Hybrid Technique and Content Boosted Collaborative Filtering," *IEEE Access*, vol. 12, pp. 131794–131808, 2024. [DOI: 10.1109/ACCESS.2024.3435160](http://dx.doi.org/10.1109/ACCESS.2024.3435160)
9. D. Shrestha, T. Wenan, D. Shrestha, N. Rajkarnikar, and S.-R. Jeong, "Personalized Tourist Recommender System: A Data-Driven and Machine-Learning Approach," *Computation*, vol. 12, no. 3, p. 59, 2024. [DOI: 10.3390/computation12030059](http://dx.doi.org/10.3390/computation12030059)
10. L. Baltrunas, B. Ludwig, and F. Ricci, "Context Relevance Assessment for Recommendation in the Mobile Domain," in *Proc. 5th ACM Conf. Recommender Systems (RecSys)*, pp. 285–288, 2011. [DOI: 10.1145/2043932.2043977](http://dx.doi.org/10.1145/2043932.2043977)
11. D. H. Wolpert, "Stacked Generalization," *Neural Networks*, vol. 5, no. 2, pp. 241–259, 1992. [DOI: 10.1016/S0893-6080(05)80023-1](http://dx.doi.org/10.1016/S0893-6080(05)80023-1)
12. L. Breiman, "Stacked Regressions," *Machine Learning*, vol. 24, no. 1, pp. 49–64, 1996. [DOI: 10.1007/BF00117832](http://dx.doi.org/10.1007/BF00117832)
13. P. Zippenfenig, "Open-Meteo: Free Weather API for Open Science and Automated Forecasting Systems," *Software Impacts*, vol. 16, p. 100512, 2023. [DOI: 10.1016/j.simpa.2023.100512](http://dx.doi.org/10.1016/j.simpa.2023.100512)
14. N. Tintarev and J. Masthoff, "Explaining Recommendations: Design and Evaluation," in *Recommender Systems Handbook*, Springer, pp. 353–382, 2015. [DOI: 10.1007/978-1-4899-7637-6_10](http://dx.doi.org/10.1007/978-1-4899-7637-6_10)
15. M. T. Ribeiro, S. Singh, and C. Guestrin, ""Why Should I Trust You?": Explaining the Predictions of Any Classifier," in *Proc. 22nd ACM SIGKDD Int. Conf. Knowledge Discovery and Data Mining*, pp. 1135–1144, 2016. [DOI: 10.1145/2939672.2939778](http://dx.doi.org/10.1145/2939672.2939778)
16. H. Alrasheed, A. Alzeer, A. Alhowimel, N. Shameri, and A. Althyabi, "A Multi-Level Tourism Destination Recommender System," *Procedia Computer Science*, vol. 170, pp. 333–340, 2020. [DOI: 10.1016/j.procs.2020.03.047](http://dx.doi.org/10.1016/j.procs.2020.03.047)
17. A. Noorian, "A BERT-Based Sequential POI Recommender System in Social Media," *Computer Standards & Interfaces*, vol. 87, p. 103766, 2024. [DOI: 10.1016/j.csi.2023.103766](http://dx.doi.org/10.1016/j.csi.2023.103766)
18. R. Polikar, "Ensemble Based Systems in Decision Making," *IEEE Circuits and Systems Magazine*, vol. 6, no. 3, pp. 21–45, 2006. [DOI: 10.1109/MCAS.2006.1688199](http://dx.doi.org/10.1109/MCAS.2006.1688199)
19. L. Rokach, "Ensemble-Based Classifiers," *Artificial Intelligence Review*, vol. 33, no. 1, pp. 1–39, 2010. [DOI: 10.1007/s10462-009-9124-7](http://dx.doi.org/10.1007/s10462-009-9124-7)
20. D. Gavalas, C. Konstantopoulos, K. Mastakas, and G. Pantziou, "Mobile Recommender Systems in Tourism," *Journal of Network and Computer Applications*, vol. 39, pp. 319–333, 2014. [DOI: 10.1016/j.jnca.2013.04.006](http://dx.doi.org/10.1016/j.jnca.2013.04.006)
21. K. H. Lim, J. Chan, D. Leckie, and S. Karunasekera, "Personalized Tour Recommendation Based on User Interests and Time Constraints," *Information Sciences*, vol. 488, pp. 51–69, 2019. [DOI: 10.1016/j.ins.2018.11.050](http://dx.doi.org/10.1016/j.ins.2018.11.050)
22. T. De Pessemier, S. Dooms, and L. Martens, "Context-Aware Recommendation of Items with a Short Lifetime," *Computers in Human Behavior*, vol. 65, pp. 252–263, 2016. [DOI: 10.1016/j.chb.2016.03.024](http://dx.doi.org/10.1016/j.chb.2016.03.024)
23. F. Ricci, L. Rokach, and B. Shapira, *Recommender Systems Handbook*, 3rd ed., New York, NY: Springer, 2022. [DOI: 10.1007/978-1-0716-2197-4](http://dx.doi.org/10.1007/978-1-0716-2197-4)

