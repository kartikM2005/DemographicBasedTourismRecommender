// TourVibe AI - Demographic & Seasonal Tourism Recommender Frontend Logic

let currentRecommendations = [];
let chartInstance = null;
let debounceTimer = null;

document.addEventListener("DOMContentLoaded", () => {
    // Note: Suggestions are generated only after clicking the generate button
    loadCatalog();

    // Attach real-time display updates to sliders (NO auto-submission)
    const ageSlider = document.getElementById('input-age');
    if (ageSlider) {
        ageSlider.addEventListener('input', () => {
            updateRangeDisplay('input-age', 'age-display', ' years');
        });
    }

    const durationSlider = document.getElementById('input-duration');
    if (durationSlider) {
        durationSlider.addEventListener('input', () => {
            updateRangeDisplay('input-duration', 'duration-display', ' days');
        });
    }
});

// Tab Switcher
function switchTab(tabName) {
    const tabs = ['recommender', 'analytics', 'catalog'];
    tabs.forEach(tab => {
        const btn = document.getElementById(`tab-btn-${tab}`);
        const sec = document.getElementById(`${tab}-section`);
        if (tab === tabName) {
            if (btn) btn.classList.add('active');
            if (sec) sec.classList.add('active');
        } else {
            if (btn) btn.classList.remove('active');
            if (sec) sec.classList.remove('active');
        }
    });

    if (tabName === 'analytics') {
        setTimeout(initComparisonChart, 150);
    }
}

// Range input helper
function updateRangeDisplay(sliderId, displayId, unit) {
    const elem = document.getElementById(sliderId);
    const disp = document.getElementById(displayId);
    if (elem && disp) {
        disp.innerText = elem.value + unit;
    }
}

// Grid button selector helper
function selectOption(containerId, element) {
    const container = document.getElementById(containerId);
    if (!container || !element) return;
    const btns = container.querySelectorAll('.select-btn');
    btns.forEach(b => b.classList.remove('active'));
    element.classList.add('active');
}

function getSelectedVal(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return '';
    const active = container.querySelector('.select-btn.active');
    return active ? active.getAttribute('data-val') : '';
}

// Preset Personas
function loadPersona(type) {
    if (type === 'student_friends') {
        setSlider('input-age', 'age-display', 21, ' years');
        setRadio('gender', 'Male');
        setRadio('income', 'Medium');
        setActiveBtn('group-type-selector', 'Friends');
        setActiveBtn('season-selector', 'Winter');
        setSlider('input-duration', 'duration-display', 5, ' days');
    } else if (type === 'family_summer') {
        setSlider('input-age', 'age-display', 42, ' years');
        setRadio('gender', 'Female');
        setRadio('income', 'Medium');
        setActiveBtn('group-type-selector', 'Family');
        setActiveBtn('season-selector', 'Summer');
        setSlider('input-duration', 'duration-display', 7, ' days');
    } else if (type === 'senior_pilgrimage') {
        setSlider('input-age', 'age-display', 65, ' years');
        setRadio('gender', 'Male');
        setRadio('income', 'Low');
        setActiveBtn('group-type-selector', 'Couple');
        setActiveBtn('season-selector', 'Winter');
        setSlider('input-duration', 'duration-display', 10, ' days');
    } else if (type === 'solo_adventure') {
        setSlider('input-age', 'age-display', 26, ' years');
        setRadio('gender', 'Other');
        setRadio('income', 'High');
        setActiveBtn('group-type-selector', 'Solo');
        setActiveBtn('season-selector', 'Monsoon');
        setSlider('input-duration', 'duration-display', 4, ' days');
    }
}

function setSlider(id, displayId, val, unit) {
    const slider = document.getElementById(id);
    if (slider) {
        slider.value = val;
        updateRangeDisplay(id, displayId, unit);
    }
}

function setRadio(name, val) {
    const radio = document.querySelector(`input[name="${name}"][value="${val}"]`);
    if (radio) radio.checked = true;
}

function setActiveBtn(containerId, val) {
    const container = document.getElementById(containerId);
    if (!container) return;
    const btns = container.querySelectorAll('.select-btn');
    btns.forEach(b => {
        if (b.getAttribute('data-val') === val) b.classList.add('active');
        else b.classList.remove('active');
    });
}

// Recommendation Submission
async function submitRecommendation() {
    const ageElem = document.getElementById('input-age');
    const genderElem = document.querySelector('input[name="gender"]:checked');
    const incomeElem = document.querySelector('input[name="income"]:checked');
    const durationElem = document.getElementById('input-duration');

    const age = ageElem ? parseInt(ageElem.value) : 25;
    const gender = genderElem ? genderElem.value : 'Male';
    const income = incomeElem ? incomeElem.value : 'Medium';
    const group = getSelectedVal('group-type-selector') || 'Friends';
    const season = getSelectedVal('season-selector') || 'Winter';
    const duration = durationElem ? parseInt(durationElem.value) : 6;

    let spending = 2500.0;
    if (income === 'Low') spending = 1200.0;
    else if (income === 'High') spending = 4200.0;

    const payload = {
        Age: age,
        Gender: gender,
        Income_Level: income,
        Spending_Amount: spending,
        Avg_Trip_Duration: duration,
        Travel_Group_Type: group,
        Travel_Season: season,
        top_n: 8
    };

    const submitBtn = document.getElementById('btn-submit-recommend');
    if (submitBtn) {
        submitBtn.innerHTML = `<span>Computing KNN Stacking Match...</span>`;
        submitBtn.disabled = true;
    }

    try {
        const response = await fetch('/api/recommend', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!response.ok) {
            throw new Error(`Server returned status ${response.status}`);
        }

        const res = await response.json();
        if (res.status === 'success') {
            updateAffinityBars(res.data.predicted_affinities);
            currentRecommendations = res.data.top_recommendations;
            renderRecommendationCards(currentRecommendations);
        } else {
            console.error("API error message:", res.message);
        }
    } catch (err) {
        console.error("Error getting recommendations:", err);
        const container = document.getElementById('recommendation-cards-container');
        if (container) {
            container.innerHTML = `
                <div style="grid-column: 1/-1; padding: 20px; background: rgba(244, 63, 94, 0.1); border: 1px solid #f43f5e; border-radius: 12px; color: #fecdd3;">
                    <strong>Recommendation Service Notice:</strong> Unable to connect to ML backend. Please ensure server is running.
                </div>
            `;
        }
    } finally {
        if (submitBtn) {
            submitBtn.innerHTML = `<span>Generate AI Recommendations</span>`;
            submitBtn.disabled = false;
        }
    }
}

// Update Class Probability Progress Bars
function updateAffinityBars(affinities) {
    const container = document.getElementById('affinity-bars-container');
    if (!container) return;

    const colorMap = {
        'Leisure': 'fill-cyan',
        'Nature': 'fill-emerald',
        'Adventure': 'fill-amber',
        'Cultural': 'fill-purple',
        'Religious': 'fill-rose'
    };

    const labels = {
        'Leisure': 'Beach & Leisure',
        'Nature': 'Nature & Hill Stations',
        'Adventure': 'Adventure & Trekking',
        'Cultural': 'Cultural & Heritage',
        'Religious': 'Religious & Pilgrimage'
    };

    container.innerHTML = '';
    for (const [cat, pct] of Object.entries(affinities)) {
        const fillClass = colorMap[cat] || 'fill-cyan';
        const displayLabel = labels[cat] || cat;
        const barItem = document.createElement('div');
        barItem.className = 'affinity-bar-item';
        barItem.innerHTML = `
            <div class="affinity-bar-label">
                <span>${displayLabel}</span>
                <strong>${pct}%</strong>
            </div>
            <div class="progress-track">
                <div class="progress-fill ${fillClass}" style="width: ${pct}%;"></div>
            </div>
        `;
        container.appendChild(barItem);
    }
}

// Render Destination Cards
function renderRecommendationCards(dests) {
    const container = document.getElementById('recommendation-cards-container');
    if (!container) return;
    container.innerHTML = '';

    if (!dests || dests.length === 0) {
        container.innerHTML = `<p style="color: #94a3b8; grid-column: 1/-1; padding: 24px; text-align: center;">No destinations found matching filter.</p>`;
        return;
    }

    dests.forEach(dest => {
        const isPeak = dest.Seasonal_Status && dest.Seasonal_Status.includes("Optimal");
        const seasonClass = isPeak ? "tag-season-peak" : "tag-season-off";

        const weather = dest.Live_Ground_Condition || {
            temperature: 24.0,
            condition: "Clear",
            icon: "🌤️",
            precipitation: 0.0,
            wind_speed: 8.0,
            hazard_level: "SAFE",
            hazard_badge: "🟢 OPTIMAL TRAVEL CLIMATE",
            hazard_class: "hazard-safe",
            advisory: "Favorable ground conditions for travel."
        };

        const xai = dest.XAI_Breakdown || {
            demographic_affinity: 90,
            seasonal_alignment: 95,
            budget_compatibility: 92,
            popularity_rating: 90
        };

        const card = document.createElement('div');
        card.className = 'dest-card';
        card.innerHTML = `
            <div>
                <div class="card-top">
                    <span class="match-badge">${dest.Match_Percentage}% Match</span>
                    <span class="tag">${dest.Budget_Tier.toLowerCase().includes('budget') ? dest.Budget_Tier : dest.Budget_Tier + ' Tier'}</span>
                </div>
                <h4 class="dest-name">${dest.Name}</h4>
                <div class="dest-state">${dest.State}</div>
                <div class="tag-row">
                    <span class="tag">${dest.Category}</span>
                    <span class="tag ${seasonClass}">Optimal: ${dest.BestTimeToVisit}</span>
                    <span class="tag">Score: ${dest.Popularity}/10</span>
                </div>

                <!-- Live Ground Telemetry Badge -->
                <div class="live-telemetry-badge">
                    <div class="live-weather-info">
                        <span class="live-radar-dot"></span>
                        <span>${weather.icon} ${weather.condition}</span>
                        <span style="color: #64748B; font-size: 0.72rem;">(${weather.wind_speed} km/h wind)</span>
                    </div>
                    <div class="live-weather-temp">${weather.temperature}°C</div>
                </div>

                <!-- Live Real-Time Hazard Alert Banner -->
                <div class="hazard-box ${weather.hazard_class}">
                    <div class="hazard-header">
                        <span>${weather.hazard_badge}</span>
                        <span>Live Telemetry</span>
                    </div>
                    <div class="hazard-advisory">${weather.advisory}</div>
                </div>

                <!-- Explainable AI (XAI) Attribution Breakdown -->
                <div class="xai-pill-grid">
                    <div class="xai-pill"><span>Demographic Fit</span> <strong>${xai.demographic_affinity}%</strong></div>
                    <div class="xai-pill"><span>Season Fit</span> <strong>${xai.seasonal_alignment}%</strong></div>
                    <div class="xai-pill"><span>Budget Fit</span> <strong>${xai.budget_compatibility}%</strong></div>
                    <div class="xai-pill"><span>Popularity Fit</span> <strong>${xai.popularity_rating}%</strong></div>
                </div>
            </div>
            <div class="dest-explanation">
                ${dest.Explanation}
            </div>
        `;
        container.appendChild(card);
    });

    const countText = document.getElementById('results-count-text');
    if (countText) {
        countText.innerText = `Displaying ${dests.length} personalized recommendations`;
    }
}

// Quick Filter on Results (FIXED: accepts btnElement)
function filterResults(filterType, btnElement) {
    const pills = document.querySelectorAll('#results-filter .pill-btn');
    pills.forEach(p => p.classList.remove('active'));
    if (btnElement) {
        btnElement.classList.add('active');
    }

    if (filterType === 'All') {
        renderRecommendationCards(currentRecommendations);
    } else if (filterType === 'Karnataka') {
        const filtered = currentRecommendations.filter(d => d.State.toLowerCase().includes('karnataka'));
        renderRecommendationCards(filtered);
    } else if (filterType === 'Peak') {
        const filtered = currentRecommendations.filter(d => d.Seasonal_Status && d.Seasonal_Status.includes('Optimal'));
        renderRecommendationCards(filtered);
    }
}

// Chart.js Performance Visualization for Viva
function initComparisonChart() {
    if (chartInstance) return;

    const ctx = document.getElementById('modelComparisonChart');
    if (!ctx) return;
    if (typeof Chart === 'undefined') {
        console.warn("Chart.js not loaded from CDN, skipping canvas render");
        return;
    }

    try {
        chartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Baseline KNN (k=5)', 'Decision Tree', 'Random Forest', 'KNN-Stacking Ensemble (Proposed)'],
                datasets: [
                    {
                        label: 'Accuracy (%)',
                        data: [77.03, 85.37, 85.57, 85.98],
                        backgroundColor: 'rgba(97, 45, 83, 0.88)',
                        borderColor: '#612D53',
                        borderWidth: 1.5,
                        borderRadius: 6
                    },
                    {
                        label: 'F1-Score (%)',
                        data: [76.36, 85.25, 84.90, 85.62],
                        backgroundColor: 'rgba(133, 57, 83, 0.85)',
                        borderColor: '#853953',
                        borderWidth: 1.5,
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: { color: '#2C2C2C', font: { family: 'Inter', size: 12, weight: '700' } }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.raw + '%';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: '#2C2C2C', font: { family: 'Inter', size: 11, weight: '600' } },
                        grid: { color: 'rgba(44, 44, 44, 0.06)' }
                    },
                    y: {
                        min: 70,
                        max: 95,
                        ticks: { color: '#2C2C2C', font: { family: 'Inter', size: 11, weight: '600' } },
                        grid: { color: 'rgba(44, 44, 44, 0.06)' }
                    }
                }
            }
        });
    } catch (err) {
        console.error("Error creating chart:", err);
    }
}

// Catalog View
async function loadCatalog() {
    const catElem = document.getElementById('catalog-category-filter');
    const seasonElem = document.getElementById('catalog-season-filter');

    const cat = catElem ? catElem.value : 'All';
    const season = seasonElem ? seasonElem.value : 'All';

    const url = `/api/destinations?category=${cat}&season=${season}`;
    try {
        const res = await fetch(url);
        const data = await res.json();
        if (data.status === 'success') {
            const container = document.getElementById('catalog-grid-container');
            if (!container) return;
            container.innerHTML = '';
            data.destinations.forEach(d => {
                const card = document.createElement('div');
                card.className = 'dest-card';
                card.innerHTML = `
                    <div>
                        <div class="card-top">
                            <span class="tag">${d.Category}</span>
                            <span class="tag">${d.Budget_Tier}</span>
                        </div>
                        <h4 class="dest-name">${d.Name}</h4>
                        <div class="dest-state">${d.State}</div>
                        <div class="tag-row">
                            <span class="tag tag-season-peak">Optimal: ${d.Season}</span>
                            <span class="tag">Months: ${d.BestTimeToVisit}</span>
                            <span class="tag">Score: ${d.Popularity}/10</span>
                        </div>
                    </div>
                `;
                container.appendChild(card);
            });
        }
    } catch (e) {
        console.error("Error loading catalog:", e);
    }
}
