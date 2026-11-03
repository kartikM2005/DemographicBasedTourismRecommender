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

    updateBudgetDisplay();
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
    } else if (tabName === 'recommender' && leafletMap) {
        setTimeout(() => leafletMap.invalidateSize(), 150);
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
        setBudgetValue(12000);
        setActiveBtn('group-type-selector', 'Friends');
        setActiveBtn('season-selector', 'Winter');
        setSlider('input-duration', 'duration-display', 5, ' days');
    } else if (type === 'family_summer') {
        setSlider('input-age', 'age-display', 42, ' years');
        setRadio('gender', 'Female');
        setBudgetValue(45000);
        setActiveBtn('group-type-selector', 'Family');
        setActiveBtn('season-selector', 'Summer');
        setSlider('input-duration', 'duration-display', 7, ' days');
    } else if (type === 'senior_pilgrimage') {
        setSlider('input-age', 'age-display', 65, ' years');
        setRadio('gender', 'Male');
        setBudgetValue(15000);
        setActiveBtn('group-type-selector', 'Couple');
        setActiveBtn('season-selector', 'Winter');
        setSlider('input-duration', 'duration-display', 10, ' days');
    } else if (type === 'solo_adventure') {
        setSlider('input-age', 'age-display', 26, ' years');
        setRadio('gender', 'Other');
        setBudgetValue(25000);
        setActiveBtn('group-type-selector', 'Solo');
        setActiveBtn('season-selector', 'Monsoon');
        setSlider('input-duration', 'duration-display', 4, ' days');
    }
}

function setBudgetValue(val) {
    const input = document.getElementById('input-budget');
    if (input) {
        input.value = val;
        updateBudgetDisplay();
    }
}

function updateBudgetDisplay() {
    const input = document.getElementById('input-budget');
    const display = document.getElementById('budget-tier-display');
    const pills = document.querySelectorAll('.btn-budget-pill');
    if (!input) return;

    const val = parseFloat(input.value) || 0;
    let tier = 'Moderate Tier';
    if (val <= 12000) tier = 'Budget Tier';
    else if (val <= 35000) tier = 'Moderate Tier';
    else if (val <= 70000) tier = 'Premium Tier';
    else tier = 'Luxury Tier';

    if (display) {
        display.innerText = `${tier} (₹${val.toLocaleString()})`;
    }

    pills.forEach(p => {
        const match = p.getAttribute('onclick') ? p.getAttribute('onclick').match(/\d+/) : null;
        if (match) {
            const pillVal = parseInt(match[0]);
            if (Math.abs(pillVal - val) < 500) p.classList.add('active');
            else p.classList.remove('active');
        }
    });
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
    const durationElem = document.getElementById('input-duration');
    const budgetElem = document.getElementById('input-budget');

    const age = ageElem ? parseInt(ageElem.value) : 25;
    const gender = genderElem ? genderElem.value : 'Male';
    const group = getSelectedVal('group-type-selector') || 'Friends';
    const season = getSelectedVal('season-selector') || 'Winter';
    const duration = durationElem ? parseInt(durationElem.value) : 6;
    const spending = budgetElem ? (parseFloat(budgetElem.value) || 25000.0) : 25000.0;

    // Dynamically derive Income Tier from real numerical budget in INR
    let income = 'Medium';
    if (spending <= 12000) income = 'Low';
    else if (spending >= 45000) income = 'High';

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
            initOrUpdateIndiaMap(currentRecommendations);
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

        const itinerary = dest.Itinerary || {
            days_count: 5,
            schedule: [
                { day: 1, title: "Day 1: Arrival & Orientation", description: "Arrive at destination, check into hotel, and evening local exploration." },
                { day: 2, title: "Day 2: Landmark & Cultural Tour", description: "Visit prime heritage monuments and cultural centers." },
                { day: 3, title: "Day 3: Outdoor & Scenic Excursion", description: "Explore scenic natural viewpoints and local culinary hotspots." },
                { day: 4, title: "Day 4: Leisure & Local Craft Stroll", description: "Market visits and souvenir craft shopping." },
                { day: 5, title: "Day 5: Farewell & Departure", description: "Morning breakfast, packing memories, and check-out." }
            ],
            budget_breakdown: {
                total_budget: 20000,
                daily_average: 4000,
                per_night_stay: 2000,
                accommodation: { amount: 8000, percentage: 40, label: "Hotels & Stays" },
                transport: { amount: 5000, percentage: 25, label: "Transit & Cabs" },
                food: { amount: 4000, percentage: 20, label: "Dining & Food" },
                activities: { amount: 3000, percentage: 15, label: "Sightseeing" },
                feasibility_badge: "🟢 COMFORTABLE BUDGET FIT",
                feasibility_status: "Ideal balance of stays and touring."
            }
        };

        const budget = itinerary.budget_breakdown || {
            total_budget: 20000,
            per_night_stay: 2000,
            accommodation: { amount: 8000, percentage: 40 },
            transport: { amount: 5000, percentage: 25 },
            food: { amount: 4000, percentage: 20 },
            activities: { amount: 3000, percentage: 15 },
            feasibility_badge: "🟢 COMFORTABLE BUDGET FIT",
            feasibility_status: "Ideal balance of stays and touring."
        };

        let timelineHtml = '';
        if (itinerary.schedule && itinerary.schedule.length > 0) {
            timelineHtml = itinerary.schedule.map(step => `
                <div class="timeline-step">
                    <div class="timeline-step-title">${step.title}</div>
                    <div class="timeline-step-desc">${step.description}</div>
                </div>
            `).join('');
        }

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

                <!-- Custom Itinerary & Smart Budget Toggle Button -->
                <button class="btn-itinerary-toggle" onclick="toggleItinerary(this)">
                    <span>📅 ${itinerary.days_count}-Day Custom Itinerary & Budget</span>
                    <span class="toggle-icon">▼</span>
                </button>

                <!-- Itinerary & Budget Collapsible Drawer -->
                <div class="itinerary-drawer">
                    <!-- Budget Section -->
                    <div class="budget-box">
                        <div class="itinerary-section-title">
                            <span>💰 Smart Budget Split (₹${budget.total_budget.toLocaleString()})</span>
                        </div>
                        <div class="budget-badge-pill">${budget.feasibility_badge}</div>
                        <div style="font-size: 0.72rem; color: #64748B; margin-bottom: 6px;">${budget.feasibility_status}</div>
                        <div class="budget-alloc-grid">
                            <div class="budget-alloc-card">
                                <div class="budget-alloc-label"><span>🏨 Stays (${budget.accommodation.percentage}%)</span></div>
                                <div class="budget-alloc-amount">₹${budget.accommodation.amount.toLocaleString()}</div>
                                <div style="font-size: 0.65rem; color: #94A3B8;">~₹${budget.per_night_stay.toLocaleString()}/night</div>
                            </div>
                            <div class="budget-alloc-card">
                                <div class="budget-alloc-label"><span>🚗 Transit (${budget.transport.percentage}%)</span></div>
                                <div class="budget-alloc-amount">₹${budget.transport.amount.toLocaleString()}</div>
                            </div>
                            <div class="budget-alloc-card">
                                <div class="budget-alloc-label"><span>🍽️ Dining (${budget.food.percentage}%)</span></div>
                                <div class="budget-alloc-amount">₹${budget.food.amount.toLocaleString()}</div>
                            </div>
                            <div class="budget-alloc-card">
                                <div class="budget-alloc-label"><span>🎟️ Passes (${budget.activities.percentage}%)</span></div>
                                <div class="budget-alloc-amount">₹${budget.activities.amount.toLocaleString()}</div>
                            </div>
                        </div>
                    </div>

                    <!-- Day-by-Day Timeline Section -->
                    <div style="margin-top: 10px;">
                        <div class="itinerary-section-title">
                            <span>📅 Day-by-Day Schedule</span>
                        </div>
                        <div class="timeline-list">
                            ${timelineHtml}
                        </div>
                    </div>
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

// Toggle Itinerary & Budget Collapsible Drawer
function toggleItinerary(btn) {
    if (!btn) return;
    const drawer = btn.nextElementSibling;
    if (!drawer) return;
    const isOpen = drawer.classList.contains('open');
    if (isOpen) {
        drawer.classList.remove('open');
        btn.classList.remove('active');
    } else {
        drawer.classList.add('open');
        btn.classList.add('active');
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
        initOrUpdateIndiaMap(currentRecommendations);
    } else if (filterType === 'Karnataka') {
        const filtered = currentRecommendations.filter(d => d.State.toLowerCase().includes('karnataka'));
        renderRecommendationCards(filtered);
        initOrUpdateIndiaMap(filtered);
    } else if (filterType === 'Peak') {
        const filtered = currentRecommendations.filter(d => d.Seasonal_Status && d.Seasonal_Status.includes('Optimal'));
        renderRecommendationCards(filtered);
        initOrUpdateIndiaMap(filtered);
    }
}

// Real Interactive India Geospatial Map Logic (Leaflet.js)
let leafletMap = null;
let mapMarkersGroup = null;

function initOrUpdateIndiaMap(dests) {
    const mapCard = document.getElementById('india-map-card');
    if (!mapCard) return;

    if (typeof L === 'undefined') {
        console.warn("Leaflet library not loaded, skipping map render");
        return;
    }

    if (!dests || dests.length === 0) {
        mapCard.style.display = 'none';
        return;
    }

    try {
        mapCard.style.display = 'block';

        if (!leafletMap) {
            // Real Center of India coordinates: [22.5, 82.0], Zoom 5
            leafletMap = L.map('indiaMap', {
                scrollWheelZoom: false,
                attributionControl: true
            }).setView([22.5, 82.0], 5);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}.png', {
                maxZoom: 18,
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(leafletMap);

            mapMarkersGroup = L.featureGroup().addTo(leafletMap);
        }

        mapMarkersGroup.clearLayers();

        const colorMap = {
            'Leisure': '#0284c7',
            'Nature': '#059669',
            'Adventure': '#d97706',
            'Cultural': '#7c3aed',
            'Religious': '#e11d48'
        };

        const iconMap = {
            'Leisure': '🏖️',
            'Nature': '🌲',
            'Adventure': '🧗',
            'Cultural': '🏛️',
            'Religious': '🛕'
        };

        dests.forEach(d => {
            const lat = parseFloat(d.Latitude);
            const lon = parseFloat(d.Longitude);
            if (isNaN(lat) || isNaN(lon)) return;

            const color = colorMap[d.Category] || '#612D53';
            const icon = iconMap[d.Category] || '📍';
            const weather = d.Live_Ground_Condition || {};

            const customHtml = `<div class="custom-pin-marker" style="background-color: ${color};" title="${d.Name}">${icon}</div>`;
            const customIcon = L.divIcon({
                className: 'custom-leaflet-marker',
                html: customHtml,
                iconSize: [32, 32],
                iconAnchor: [16, 16],
                popupAnchor: [0, -16]
            });

            const popupHtml = `
                <div class="map-popup-card">
                    <div class="map-popup-title">${d.Name}</div>
                    <div class="map-popup-meta">${d.State} • <strong>${d.Category}</strong></div>
                    <div class="map-popup-temp">${weather.icon || '🌤️'} ${weather.temperature || 25}°C • ${weather.condition || 'Clear'}</div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 4px;">
                        <span class="map-popup-match">${d.Match_Percentage}% Match</span>
                        <span style="font-size: 0.72rem; color: #64748B;">₹${(d.Itinerary?.budget_breakdown?.total_budget || 25000).toLocaleString()}</span>
                    </div>
                </div>
            `;

            const marker = L.marker([lat, lon], { icon: customIcon }).bindPopup(popupHtml);
            mapMarkersGroup.addLayer(marker);
        });

        if (mapMarkersGroup.getLayers().length > 0) {
            leafletMap.fitBounds(mapMarkersGroup.getBounds().pad(0.18));
        }

        setTimeout(() => {
            if (leafletMap) leafletMap.invalidateSize();
        }, 150);
    } catch (e) {
        console.error("Map initialization notice:", e);
    }
}

function resetMapView() {
    if (leafletMap && mapMarkersGroup && mapMarkersGroup.getLayers().length > 0) {
        leafletMap.fitBounds(mapMarkersGroup.getBounds().pad(0.18));
    } else if (leafletMap) {
        leafletMap.setView([22.5, 82.0], 5);
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
