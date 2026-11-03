"""
TourVibe AI - Dynamic Itinerary Generator & Smart Budget Decomposition Engine
Generates customized day-by-day travel roadmaps and financial expense allocations
tailored to user duration, companion group, category, and destination profile.
"""

# Destination-specific key milestones & curated landmarks for top hubs
DESTINATION_LANDMARKS = {
    "Hampi UNESCO Ruins": [
        ("Arrival & Sunset at Hemakuta Hill", "Check into heritage stay, sunset over monolithic boulder hills and Virupaksha Temple bazaar."),
        ("Sacred & Royal Enclosure Immersion", "Explore Vijaya Vittala Stone Chariot, musical pillars, Queen's Bath, and Hazara Rama Temple."),
        ("Across the Tungabhadra to Anegundi", "Ferry or coracle ride across river to monkey temple (Anjaneya Hill) and Sanapur Lake boulder cliffs."),
        ("Zenana Enclosure & Lotus Mahal", "Morning photography at Elephant Stables, underground Shiva shrine, and Tungabhadra riverbanks."),
        ("Craft Village & Departure Walk", "Souvenir shopping for local Lambani textiles and departure transit from Hospet.")
    ],
    "Taj Mahal & Agra Fort": [
        ("Agra Arrival & Sunset from Mehtab Bagh", "Arrive in Agra, evening sunset panorama of Taj Mahal from across the Yamuna River."),
        ("Taj Mahal Sunrise & Imperial Agra Fort", "Early dawn entry into Taj Mahal for golden hour photography, followed by exploring the Mughal palaces in Agra Fort."),
        ("Fatehpur Sikri Ghost Citadel", "Day excursion to the sandstone city of Emperor Akbar, Buland Darwaza, and Salim Chishti Dargah."),
        ("Mughal Heritage Walk & Street Dining", "Itmad-ud-Daulah (Baby Taj), Kinari Bazaar leather handicrafts, and tasting authentic Agra Petha."),
        ("Akbar's Tomb at Sikandra & Return", "Visit Sikandra mausoleum gardens and depart.")
    ],
    "Mysore Palace & Srirangapatna": [
        ("Mysore Welcome & Chamundi Hills", "Arrive in Mysore, drive up Chamundi Hill for city view, evening palace exterior illumination."),
        ("Royal Mysore Palace & Devaraja Market", "Tour the opulent Durbar halls of Mysore Palace, fragrant sandalwood shops, and vibrant Devaraja spice market."),
        ("Srirangapatna Historical Fort & Bird Sanctuary", "Explore Tipu Sultan's summer palace, river fortress, and boating at Ranganathittu Bird Sanctuary."),
        ("Brindavan Gardens & Musical Fountains", "Afternoon excursion to KRS Dam, illuminated musical fountain shows, and regional silk weaving centers."),
        ("Artisans Village & Sweet Tour", "Taste original Mysore Pak, visit Channapatna wooden toy artisans on the return highway.")
    ],
    "North Goa Beaches (Calangute, Anjuna, Baga)": [
        ("Coastal Arrival & Shack Sunset", "Check into beachside resort, evening sunset walk along Calangute and Baga shacks with fresh seafood."),
        ("Watersports at Anjuna & Fort Aguada", "Morning parasailing and jet-skiing at Baga, visit 17th-century Portuguese Aguada lighthouse fort."),
        ("Vagator Red Cliffs & Chapora Fort", "Panoramic views from 'Dil Chahta Hai' Chapora Fort, evening music and sunset at Ozran Beach."),
        ("Old Goa Cathedrals & Mandovi River Cruise", "Tour Basilica of Bom Jesus, Se Cathedral, followed by a sunset catamaran cruise along the Mandovi."),
        ("Flea Market Shopping & Departure", "Souvenir shopping at Anjuna flea market, cashews & feni tasting, and airport transfer.")
    ],
    "Gokarna (Om Beach & Kudle Beach)": [
        ("Gokarna Arrival & Kudle Beach Sunset", "Arrive in Gokarna, check into cliffside cottages, sunset relaxation and beachside cafes at Kudle."),
        ("Five-Beach Trek & Om Beach Water Adventures", "Scenic cliff trek linking Paradise, Half Moon, Om, and Kudle beaches. Boating and dolphin spotting at Om Beach."),
        ("Atmalinga Pilgrimage & Town Culture", "Morning darshan at Mahabaleshwar Temple, sacred Kotitirtha water tank, and traditional South Indian thali."),
        ("Yana Caves & Mirjan Fort Day Excursion", "Short scenic drive through dense Western Ghats to massive limestone Yana peaks and 16th-century Mirjan Fort."),
        ("Morning Beach Yoga & Leisure Return", "Calm morning walk along secluded Main Beach, shopping for brass artifacts, and departure.")
    ],
    "Coorg (Madikeri & Coffee Valleys)": [
        ("Arrival in the Scotland of India", "Check into coffee plantation estate, aroma walking tour, and evening sunset from Raja's Seat."),
        ("Abbey Falls & Madikeri Fortress", "Lush cascade of Abbey Falls amidst spice groves, followed by Madikeri Fort and Omkareshwara Temple."),
        ("Dubare Elephant Camp & Kaveri River", "Morning elephant bathing and river interaction at Dubare, followed by serene Golden Temple Tibetan Monastery in Bylakuppe."),
        ("Tadiandamol Peak or Talakaveri", "Drive to sacred birthplace of River Kaveri at Talakaveri or mild hiking on scenic plantation ridges."),
        ("Spice & Homemade Chocolate Shopping", "Pick up freshly roasted Coorg Arabica coffee, homemade dark chocolates, spices, and depart.")
    ],
    "Manali (Solang & Rohtang Valley)": [
        ("Alpine Arrival & Old Manali Vibe", "Check into pine-surrounded retreat, stroll through Old Manali wooden cafes and Tibetan monastery."),
        ("Hadimba Temple & Vashisht Thermal Baths", "Ancient cedarwood Hadimba Devi Temple, Manu Temple, and natural sulphur hot water springs at Vashisht."),
        ("Solang Valley Adventure & Paragliding", "Full day at Solang Valley for ropeway rides, zorbing, paragliding, and ATV quad trails."),
        ("High-Altitude Snow Excursion (Rohtang / Atal Tunnel)", "Drive through engineering marvel Atal Tunnel to Lahaul valley or high snow points on Rohtang Pass."),
        ("Mall Road Craft Stroll & Departure", "Shop for warm Kullu shawls and dry fruits on Mall Road before boarding return transit.")
    ],
    "Leh Ladakh Pangong Lake & Khardung La": [
        ("Leh Arrival & Mandatory Acclimatization", "Rest and acclimatize to high altitude (11,500 ft), gentle evening walk to Shanti Stupa for sunset over Zanskar range."),
        ("Leh Palace, Hall of Fame & Market", "Explore 17th-century Leh Royal Palace, Leh Main Bazaar apricot shops, and Tibetan handicrafts."),
        ("Highest Motorable Khardung La to Nubra Valley", "Drive across Khardung La pass (17,982 ft) to Diskit Monastery giant Buddha and Hunder sand dunes."),
        ("Double-Humped Camel Safari & Valley Drive", "Camel safari on Nubra dunes, scenic transit along Shyok River towards breathtaking Pangong Tso."),
        ("Pangong Lake Color Shifts & High Passes", "Marvel at changing blue shades of Pangong lake, drive back over Chang La pass (17,590 ft) to Leh for departure.")
    ],
    "Varanasi Kashi Vishwanath & Ganga Ghats": [
        ("Spiritual Arrival & Evening Ganga Aarti", "Arrive in the world's oldest living city, witness the grand, hypnotic evening Maha Aarti ceremony at Dashashwamedh Ghat."),
        ("Subah-e-Banaras Boat Ride & Kashi Vishwanath", "Dawn sunrise wooden boat ride along historical ghats, followed by darshan at the sacred Kashi Vishwanath Golden Temple corridor."),
        ("Sarnath Buddhist Heritage Day Excursion", "Visit deer park in Sarnath where Lord Buddha gave his first sermon, Dhamek Stupa, and the Ashoka Pillar museum."),
        ("Ancient Winding Alleys, Silk & Banarasi Delights", "Walk through mystical old city gallis, visit Banarasi silk weavers, and taste authentic Blue Lassi, kachoris, and Banarasi paan."),
        ("Assi Ghat Morning Yoga & Departure", "Peaceful morning flute and meditation session at Assi Ghat before departure.")
    ]
}

# Category-based fallback templates for other destinations
CATEGORY_TEMPLATES = {
    "Cultural": [
        ("Arrival, Heritage Welcome & Orientation", "Settle into accommodation, evening walk through heritage quarters, orientation with local architectural traditions."),
        ("Signature UNESCO / Historical Site Tour", "Full-day guided exploration of core palaces, fortresses, and state archaeological museums."),
        ("Artisan Communities & Folk Traditions", "Visit local handicraft clusters, traditional textile looms, and evening classical folk music/dance show."),
        ("Regional Day Excursion & Ancient Environs", "Short road trip to nearby historical ruins, ancient stepwells, or secondary fortress bastions."),
        ("Culinary & Cultural Market Discovery", "Savor heritage recipes at historic eateries, shop for authentic brass and terracotta crafts."),
        ("Lesser-Known Bastions & Photography", "Early morning golden-hour photography of monument domes, peaceful museum galleries."),
        ("Farewell Leisure & Departure Walk", "Leisure morning walk in municipal gardens, packing regional souvenirs, and departure transit.")
    ],
    "Leisure": [
        ("Coastal Arrival & Sunset Promenade", "Check into beach resort, relax after travel, evening barefoot sunset walk along the shoreline."),
        ("Beachside Watersports & Coastal Forts", "Parasailing, banana boat rides, and exploring coastal headland viewpoints with sea breeze."),
        ("Island Hopping / Lagoon Boat Cruise", "Boating through scenic backwaters or island ferries with snorkeling and marine life spotting."),
        ("Cliffside Dining & Twilight Relaxation", "Relaxing seaside cafe hopping, enjoying fresh local culinary delicacies and live ambient music."),
        ("Wellness & Coastal Village Walk", "Ayurvedic massage, yoga on the beach, and interacting with local fishermen hamlets."),
        ("Secluded Secret Beach Exploration", "Day excursion to tranquil, uncrowded cove beaches away from tourist hubs."),
        ("Souvenir Shopping & Relaxed Departure", "Shopping for seashells, tropical apparel, and local cashew/spice treats before heading home.")
    ],
    "Nature": [
        ("Mountain Arrival & Valley Sunset", "Check into hill cottage, sip locally grown tea/coffee, and catch panoramic valley sunset view."),
        ("Waterfalls & Botanical Garden Trails", "Visit cascading mountain waterfalls, orchid nurseries, and dense pine / cedar ridge viewpoints."),
        ("Wildlife Sanctuary or Tea Estate Tour", "Morning wildlife safari or guided walking trail through mist-covered tea and spice plantations."),
        ("High Peak Hiking & Adventure Viewpoint", "Moderate scenic hike to the highest ridge in the region for uninterrupted 360-degree mountain vistas."),
        ("Indigenous Village & River Exploration", "Visit remote river valleys, living bamboo groves, or serene mountain lakes."),
        ("Bird Watching & Forest Canopy Walk", "Early morning forest trail with binoculars for endemic bird species and floral flora."),
        ("Local Herbals & Fresh Roast Shopping", "Purchase authentic hill honey, pure essential oils, organic green tea, and depart.")
    ],
    "Adventure": [
        ("Base Camp Arrival & Gear Check", "Arrive at adventure hub, briefing with certified guides, equipment check, and altitude acclimatization."),
        ("High-Octane Activity Day (Rafting / Paragliding)", "Morning river rafting through Class III+ rapids or tandem paragliding flight over deep valleys."),
        ("Signature Trek / High Mountain Pass", "Full-day alpine ridge trek through scenic rhododendron forests or rugged rocky gorges."),
        ("Camping Under the Stars & Bonfire", "Wilderness overnight camp or outdoor rock-climbing and bouldering session with camp meals."),
        ("Canyon Exploration or Quad Safari", "Explore hidden water canyons, off-road 4x4 trails, or mountain biking across rough terrain."),
        ("Suspension Bridges & Secret Cascades", "Trek to remote suspension bridges and natural plunge pools for wilderness swimming."),
        ("Victory Celebration & Departure", "Collect adventure certification / action photos, celebrate trip memories, and board return transit.")
    ],
    "Religious": [
        ("Pilgrimage Arrival & Temple Town Orientation", "Arrive at holy dham, check into peaceful dharmashala/hotel, evening river ghat aarti or temple parikrama."),
        ("Principal Shrine Mahadarshan & Abhishekham", "Early morning auspicious temple darshan, special archana rituals, and receiving divine mahaprasad."),
        ("Sacred Water Bodies & Secondary Shrines", "Holy dip in sacred sarovar/river, followed by visits to historic mathas, ashrams, and Vedic centers."),
        ("Spiritual Discourse & Ashram Meditation", "Attend calming Satsang discourse, meditation session, or visit associated saint samadhi shrines."),
        ("Philanthropic Annadana & Holy Town Walk", "Participate in temple community kitchen (langar/annadana) and explore devotional bookstalls."),
        ("Hilltop Temple Ascent or Parikrama", "Scenic hill stairway climb or circumambulation trail around the sacred mountain/temple complex."),
        ("Sacred Keepsakes & Graceful Departure", "Procure consecrated temple prasadam, sacred rudraksha, brass pooja lamps, and depart in peace.")
    ]
}

def generate_itinerary(dest_name, state, category, duration=5, group_type="Friends", spending=25000.0, budget_tier="Moderate"):
    """
    Synthesizes a day-by-day tailored itinerary and financial breakdown.
    """
    days_count = max(2, min(duration, 10))  # Normalize between 2 and 10 days
    
    # 1. Select activities list (Specific landmarks if known, otherwise category template)
    matched_plan = None
    for key, plan in DESTINATION_LANDMARKS.items():
        if key.lower() in dest_name.lower() or dest_name.lower() in key.lower():
            matched_plan = plan
            break
            
    if not matched_plan:
        matched_plan = CATEGORY_TEMPLATES.get(category, CATEGORY_TEMPLATES["Cultural"])

    # Build the days
    daily_schedule = []
    for d in range(1, days_count + 1):
        idx = min(d - 1, len(matched_plan) - 1)
        # If user duration exceeds plan length, wrap around or extend
        if d == days_count and d > 2:
            title = "Souvenir Stroll & Fond Farewell"
            desc = f"Morning relaxed brunch, packing regional crafts and memories of {dest_name}, hotel check-out and journey back."
        else:
            title, desc = matched_plan[idx]
            
        daily_schedule.append({
            "day": d,
            "title": f"Day {d}: {title}",
            "description": desc
        })

    # 2. Financial Budget Decomposition
    # Normalize spending amount realistically
    total_budget = float(spending)
    if total_budget < 3000.0:
        total_budget = 15000.0  # Safe default in INR

    accommodation_cost = round(total_budget * 0.40)
    per_night = round(accommodation_cost / max(1, days_count - 1))
    
    transport_cost = round(total_budget * 0.25)
    food_cost = round(total_budget * 0.20)
    activities_cost = round(total_budget * 0.15)
    daily_spend = round(total_budget / days_count)

    tier = budget_tier.capitalize()
    if "Luxury" in tier or total_budget >= 40000.0:
        feasibility_badge = "🟢 LUXURY & RESORT COMFORT"
        feasibility_status = "Ample budget for 4/5-star stays, private cab transfers, and premium guided activities."
    elif "Budget" in tier or total_budget <= 15000.0:
        feasibility_badge = "🟢 HIGH-VALUE BUDGET FIT"
        feasibility_status = "Optimal for hostels, homestays, public/shared transit, and local street gastronomy."
    else:
        feasibility_badge = "🟢 COMFORTABLE MODERATE FIT"
        feasibility_status = "Ideal balance of boutique boutique stays, comfortable private/rental cabs, and cafe dining."

    budget_breakdown = {
        "total_budget": total_budget,
        "daily_average": daily_spend,
        "per_night_stay": per_night,
        "accommodation": {
            "amount": accommodation_cost,
            "percentage": 40,
            "label": "Hotels & Stays"
        },
        "transport": {
            "amount": transport_cost,
            "percentage": 25,
            "label": "Transit & Local Cabs"
        },
        "food": {
            "amount": food_cost,
            "percentage": 20,
            "label": "Dining & Local Food"
        },
        "activities": {
            "amount": activities_cost,
            "percentage": 15,
            "label": "Sightseeing & Passes"
        },
        "feasibility_badge": feasibility_badge,
        "feasibility_status": feasibility_status
    }

    return {
        "days_count": days_count,
        "group_type": group_type,
        "schedule": daily_schedule,
        "budget_breakdown": budget_breakdown
    }

if __name__ == "__main__":
    # Test generator
    test_res = generate_itinerary(
        dest_name="Manali (Solang & Rohtang Valley)",
        state="Himachal Pradesh",
        category="Nature",
        duration=5,
        group_type="Friends",
        spending=20000.0,
        budget_tier="Moderate"
    )
    print(f"Generated {test_res['days_count']}-Day Itinerary for {test_res['group_type']}:")
    for s in test_res["schedule"]:
        print(f"  {s['title']}: {s['description']}")
    print("\nBudget Breakdown:")
    print(f"  Total: Rs. {test_res['budget_breakdown']['total_budget']}")
    print(f"  Stay: Rs. {test_res['budget_breakdown']['accommodation']['amount']}")
    print(f"  Transport: Rs. {test_res['budget_breakdown']['transport']['amount']}")
    print(f"  Food: Rs. {test_res['budget_breakdown']['food']['amount']}")
    print(f"  Activities: Rs. {test_res['budget_breakdown']['activities']['amount']}")
    print(f"  Status: {test_res['budget_breakdown']['feasibility_badge'].encode('ascii', errors='replace').decode('ascii')}")
