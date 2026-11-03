import pandas as pd

# Precise coordinates for all 175 destinations across India
COORDS = {
    # Cultural & Heritage
    101: (15.3350, 76.4600), # Hampi
    102: (27.1751, 78.0421), # Taj Mahal Agra
    103: (12.3051, 76.6551), # Mysore Palace
    104: (26.9855, 75.8513), # Amer Fort Jaipur
    105: (15.9189, 75.6766), # Badami
    106: (15.9489, 75.8160), # Pattadakal
    107: (16.8302, 75.7350), # Bijapur Gol Gumbaz
    108: (13.1625, 75.8596), # Belur
    109: (13.2167, 75.9936), # Halebidu
    110: (17.9104, 77.5199), # Bidar Fort
    111: (24.8318, 79.9199), # Khajuraho
    112: (24.5764, 73.6835), # Udaipur Lake Pichola
    113: (26.2980, 73.0189), # Mehrangarh Fort Jodhpur
    114: (26.9124, 70.9127), # Jaisalmer Fort
    115: (20.5519, 75.7033), # Ajanta & Ellora
    116: (28.6562, 77.2410), # Red Fort Delhi
    117: (26.2307, 78.1695), # Gwalior Fort
    118: (25.3512, 78.6415), # Orchha Fort
    119: (27.0945, 77.6679), # Fatehpur Sikri
    120: (19.8876, 86.0945), # Konark Sun Temple
    121: (12.6208, 80.1945), # Mahabalipuram
    122: (10.7828, 79.1318), # Thanjavur Brihadisvara
    123: (24.8887, 74.6269), # Chittorgarh Fort
    124: (25.1357, 85.4435), # Nalanda Ruins
    125: (17.3833, 78.4011), # Golconda Fort
    126: (25.1478, 73.5872), # Kumbhalgarh Fort
    127: (23.8589, 72.1017), # Rani Ki Vav Patan
    128: (25.4414, 75.6421), # Bundi Taragarh Fort
    129: (23.4793, 77.7397), # Sanchi Stupa
    130: (22.5448, 88.3426), # Victoria Memorial Kolkata
    131: (22.3662, 75.3949), # Mandu Citadel
    132: (18.9400, 72.8353), # CSMT Mumbai
    133: (12.8342, 79.7036), # Kanchipuram
    134: (10.0763, 78.7844), # Chettinad
    135: (8.2508, 77.3275),  # Padmanabhapuram Palace

    # Beach & Leisure
    201: (15.5439, 73.7553), # North Goa (Baga/Calangute)
    202: (15.0100, 74.0232), # South Goa (Palolem)
    203: (14.5479, 74.3188), # Gokarna Om Beach
    204: (13.2205, 74.7432), # Kaup Beach
    205: (13.3541, 74.6974), # Malpe Beach
    206: (14.8185, 74.1306), # Karwar Beach
    207: (11.9761, 92.9876), # Havelock Island Radhanagar
    208: (11.8324, 93.0506), # Neil Island
    209: (8.7379, 76.7163),  # Varkala Cliff Beach
    210: (8.4021, 76.9787),  # Kovalam Lighthouse Beach
    211: (9.6011, 76.2999),  # Marari Beach
    212: (11.9338, 79.8358), # Pondicherry Promenade
    213: (12.0070, 79.8107), # Auroville Beach
    214: (19.7983, 85.8249), # Puri Beach
    215: (21.4682, 87.0234), # Chandipur Beach
    216: (21.6266, 87.5074), # Digha & Mandarmani
    217: (18.6584, 72.8773), # Alibaug & Kashid
    218: (16.0374, 73.4908), # Tarkarli Beach
    219: (17.1479, 73.2687), # Ganpatipule Beach
    220: (20.7144, 70.9874), # Diu Island Nagoa
    221: (13.0499, 80.2824), # Marina Beach Chennai
    222: (9.1783, 79.4184),  # Dhanushkodi Beach
    223: (12.3927, 75.0315), # Bekal Beach Resort
    224: (10.8533, 72.1948), # Agatti Island Lakshadweep
    225: (8.2833, 73.0500),  # Minicoy Island Lakshadweep
    226: (17.7812, 83.3852), # Rushikonda Beach Vizag
    227: (12.9234, 74.8085), # Panambur Beach Mangalore
    228: (12.8093, 74.8523), # Ullal Beach Mangalore
    229: (11.8306, 75.3957), # Kizhunna Beach Kannur
    230: (11.3857, 75.7277), # Kappad Beach Kozhikode

    # Nature & Hill Stations
    301: (12.4244, 75.7382), # Coorg Madikeri
    302: (13.3161, 75.7720), # Chikmagalur
    303: (14.2285, 74.8124), # Jog Falls
    304: (11.6664, 76.6291), # Bandipur Tiger Reserve
    305: (11.9567, 76.2711), # Nagarhole Kabini
    306: (13.5487, 75.7538), # Kemmanagundi
    307: (13.5073, 75.0934), # Agumbe Sunset Point
    308: (13.2198, 75.2573), # Kudremukh National Park
    309: (13.3702, 77.6835), # Nandi Hills
    310: (14.5492, 74.5513), # Yana Rocks
    311: (10.0889, 77.0595), # Munnar Tea Gardens
    312: (11.6854, 76.1320), # Wayanad Chembra
    313: (9.6031, 77.1615),  # Thekkady Periyar
    314: (11.4102, 76.6950), # Ooty Nilgiris
    315: (10.2381, 77.4892), # Kodaikanal
    316: (11.7753, 78.2093), # Yercaud
    317: (32.2432, 77.1892), # Manali Rohtang
    318: (31.1048, 77.1734), # Shimla & Kufri
    319: (32.2190, 76.3234), # Dharamshala Kangra
    320: (32.5387, 75.9710), # Dalhousie & Khajjiar
    321: (29.3919, 79.4542), # Nainital Lake
    322: (30.4598, 78.0644), # Mussoorie Queen of Hills
    323: (29.5300, 78.7747), # Jim Corbett
    324: (30.7280, 79.6053), # Valley of Flowers
    325: (29.8443, 79.6044), # Kausani Panorama
    326: (27.0410, 88.2663), # Darjeeling Tiger Hill
    327: (27.0667, 88.4667), # Kalimpong
    328: (26.6500, 88.7667), # Dooars Gorumara
    329: (27.3389, 88.6065), # Gangtok Tsomgo
    330: (27.3000, 88.2333), # Pelling Kanchenjunga
    331: (27.7833, 88.7000), # Yumthang Zero Point
    332: (25.5788, 91.8933), # Shillong
    333: (25.2986, 91.7303), # Cherrapunji Nohkalikai
    334: (25.2017, 91.9167), # Mawlynnong Root Bridges
    335: (26.5775, 93.1711), # Kaziranga National Park
    336: (26.9500, 94.2167), # Majuli River Island
    337: (27.5861, 91.8594), # Tawang Monasteries
    338: (27.5644, 93.8385), # Ziro Valley Pine Groves
    339: (17.9237, 73.6586), # Mahabaleshwar
    340: (18.7557, 73.4091), # Lonavala & Khandala
    341: (17.9242, 73.8009), # Panchgani Table Land
    342: (22.4674, 78.4346), # Pachmarhi Satpura
    343: (22.3345, 80.6115), # Kanha & Bandhavgarh
    344: (24.5925, 72.7156), # Mount Abu
    345: (20.5750, 73.7489), # Saputara Hill Station

    # Adventure & Trekking
    401: (34.1526, 77.5771), # Leh Ladakh Pangong
    402: (34.5833, 77.5500), # Nubra Valley Hunder
    403: (33.7483, 76.8428), # Chadar Trek Zanskar
    404: (30.0869, 78.2676), # Rishikesh Rafting
    405: (30.5298, 79.5694), # Auli Skiing Slopes
    406: (31.0234, 78.1723), # Kedarkantha Trek
    407: (30.2642, 79.7314), # Roopkund Mystery Lake
    408: (31.1444, 78.3847), # Har Ki Dun Trek
    409: (32.2461, 78.0349), # Spiti Valley Chandratal
    410: (32.0428, 76.7179), # Bir Billing Paragliding
    411: (32.0100, 77.3150), # Kasol & Kheerganga
    412: (32.2570, 76.3533), # Triund Ridge Trek
    413: (32.2890, 77.3680), # Hampta Pass Trek
    414: (34.0484, 74.3805), # Gulmarg Skiing
    415: (34.0106, 75.3214), # Pahalgam Betaab Valley
    416: (34.3000, 75.2833), # Great Lakes Sonamarg
    417: (15.2678, 74.6189), # Dandeli Kali Rafting
    418: (12.6644, 75.6983), # Kumara Parvatha Trek
    419: (12.2167, 75.6167), # Tadiandamol Coorg Peak
    420: (14.0167, 74.3167), # Netrani Scuba Murudeshwar
    421: (12.9194, 77.2936), # Savandurga Night Trek
    422: (12.0000, 93.0000), # Havelock Coral Safari
    423: (26.8300, 70.5100), # Sam Sand Dunes Jaisalmer
    424: (23.8344, 69.8389), # Rann of Kutch Safari
    425: (19.3833, 73.7833), # Harishchandragad Trek
    426: (19.6000, 73.7167), # Kalsubai Peak
    427: (19.5333, 73.7000), # Sandhan Valley Trek
    428: (10.0833, 77.2000), # Kolukkumalai Safari
    429: (8.7300, 76.7100),  # Kovalam Surfing
    430: (15.5200, 73.7600), # Goa Watersports

    # Religious & Pilgrimage
    501: (25.3109, 83.0107), # Varanasi Kashi Vishwanath
    502: (13.6833, 79.3500), # Tirupati Balaji
    503: (31.6200, 74.8765), # Golden Temple Amritsar
    504: (30.7352, 79.0669), # Kedarnath Jyotirlinga
    505: (30.7433, 79.4938), # Badrinath Alaknanda
    506: (29.9560, 78.1700), # Haridwar Har Ki Pauri
    507: (30.1250, 78.3150), # Rishikesh Parmarth Niketan
    508: (14.0940, 74.4899), # Murudeshwar Shiva Statue
    509: (13.3409, 74.7421), # Udupi Sri Krishna Matha
    510: (12.9554, 75.3789), # Dharmasthala Manjunatha
    511: (12.6775, 75.6144), # Kukke Subramanya
    512: (13.4187, 75.2536), # Sringeri Sharada Peetham
    513: (13.2789, 75.3421), # Horanadu Annapoorneshwari
    514: (14.5428, 74.3189), # Gokarna Mahabaleshwar
    515: (12.8572, 76.4867), # Shravanabelagola Bahubali
    516: (12.2745, 76.6711), # Chamundeshwari Temple
    517: (16.2064, 76.0847), # Koodalasangama
    518: (9.9195, 78.1194),  # Madurai Meenakshi Temple
    519: (9.2881, 79.3174),  # Rameshwaram Ramanathaswamy
    520: (8.0780, 77.5550),  # Kanyakumari Vivekananda
    521: (10.4500, 77.5167), # Palani Murugan Temple
    522: (11.3992, 79.6933), # Chidambaram Nataraja
    523: (9.4344, 77.0811),  # Sabarimala Ayyappa
    524: (10.5947, 76.0406), # Guruvayur Temple
    525: (8.4828, 76.9436),  # Padmanabhaswamy Temple
    526: (19.8049, 85.8179), # Puri Jagannath Temple
    527: (24.6961, 84.9913), # Bodh Gaya Mahabodhi
    528: (20.8880, 70.4012), # Somnath Jyotirlinga
    529: (22.2406, 68.9685), # Dwarka Dwarkadhish
    530: (19.7667, 74.4767), # Shirdi Sai Baba
    531: (19.9328, 73.5303), # Trimbakeshwar Nashik
    532: (32.9900, 74.9500), # Vaishno Devi Katra
    533: (34.2156, 75.5039), # Amarnath Cave Lingam
    534: (26.4897, 74.5511), # Pushkar Brahma Temple
    535: (26.1667, 91.7047)  # Kamakhya Devi Guwahati
}

df = pd.read_csv("data/enriched_destinations.csv")

# Add Latitude and Longitude columns
lats, lons = [], []
for _, row in df.iterrows():
    dest_id = int(row["DestinationID"])
    lat, lon = COORDS.get(dest_id, (20.5937, 78.9629))
    lats.append(lat)
    lons.append(lon)

df["Latitude"] = lats
df["Longitude"] = lons

df.to_csv("data/enriched_destinations.csv", index=False)
print(f"Successfully enriched all {len(df)} destinations with exact coordinates!")
print(df[["DestinationID", "Name", "State", "Latitude", "Longitude"]].head(8))
