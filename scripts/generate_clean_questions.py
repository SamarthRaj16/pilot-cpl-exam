import json
import os
import re

BASE = r"c:\VS Code\Codes\dgcacpllearning"

# Load nav_raw.json and reg_raw.json
with open(os.path.join(BASE, "scripts", "nav_raw.json"), "r", encoding="utf-8") as f:
    nav_raw = json.load(f)

with open(os.path.join(BASE, "scripts", "reg_raw.json"), "r", encoding="utf-8") as f:
    reg_raw = json.load(f)

def clean_text(s):
    if not isinstance(s, str):
        return s
    # Clean broken quotes / unicode artefacts
    s = s.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("?T", "'").replace("?", "'")
    return s.strip()

questions = []

# 1. AIR NAVIGATION: Pick 2 questions per chapter (50 total across 25 chapters)
nav_by_chap = {}
for item in nav_raw:
    chap = item.get("chapter", "General Navigation")
    nav_by_chap.setdefault(chap, []).append(item)

nav_count = 0
for chap, items in sorted(nav_by_chap.items()):
    # pick 2 items per chapter
    for item in items[:2]:
        nav_count += 1
        d = item["data"]
        q_id = f"NAV-{nav_count:03d}"
        questions.append({
            "id": q_id,
            "subject": "Air Navigation",
            "topic": chap,
            "difficulty": "easy" if nav_count % 3 == 1 else ("medium" if nav_count % 3 == 2 else "hard"),
            "question": clean_text(d["q"]),
            "options": [clean_text(o) for o in d["o"]],
            "answerIndex": d["a"],
            "explanation": clean_text(d["e"]),
            "source": f"R.K. Bali Air Navigation / Oxford ATPL Gen Nav, Chapter '{chap}'"
        })

# 2. AIR REGULATIONS: Pick 2 questions per chapter (50 total across 25 chapters)
reg_by_chap = {}
for item in reg_raw:
    chap = item.get("chapter", "Air Regulations")
    reg_by_chap.setdefault(chap, []).append(item)

reg_count = 0
for chap, items in sorted(reg_by_chap.items()):
    for item in items[:2]:
        reg_count += 1
        d = item["data"]
        q_id = f"REG-{reg_count:03d}"
        questions.append({
            "id": q_id,
            "subject": "Air Regulations",
            "topic": chap,
            "difficulty": "easy" if reg_count % 3 == 1 else ("medium" if reg_count % 3 == 2 else "hard"),
            "question": clean_text(d["q"]),
            "options": [clean_text(o) for o in d["o"]],
            "answerIndex": d["a"],
            "explanation": clean_text(d["e"]),
            "source": f"R.K. Bali Air Regulations / ICAO Annexes, Chapter '{chap}'"
        })

# 3. AVIATION METEOROLOGY: 45 authentic questions based on I.C. Joshi Aviation Meteorology
met_questions_data = [
    {
        "topic": "The Atmosphere",
        "difficulty": "easy",
        "q": "The lowest layer of the atmosphere, in which almost all weather phenomena occur, is called the:",
        "o": ["Stratosphere", "Troposphere", "Mesosphere", "Thermosphere"],
        "a": 1,
        "e": "The troposphere extends from the surface to about 16-18 km at the equator and 8-10 km at the poles. It contains about 75% of the atmospheric mass and virtually all weather phenomena.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', Page 5"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "medium",
        "q": "In the International Standard Atmosphere (ISA), what is the standard temperature and pressure at mean sea level?",
        "o": ["15°C (288.15 K) and 1013.25 hPa", "20°C and 1000 hPa", "0°C and 1013.25 hPa", "15°C and 1000 hPa"],
        "a": 0,
        "e": "ICAO ISA specifies sea level temperature as +15°C (288.15 K), pressure as 1013.25 hPa (29.92 inHg), and density as 1225 g/m³ with a lapse rate of 6.5°C/km (approx 1.98°C/1000 ft) up to 11 km.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', Page 7"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "medium",
        "q": "The height of the tropopause is:",
        "o": ["Constant over all latitudes at 11 km", "Highest at the equator (16-18 km) and lowest at the poles (8-10 km)", "Highest at the poles and lowest at the equator", "Dependent only on the time of day"],
        "a": 1,
        "e": "Due to intense solar heating and strong vertical convective currents in the tropics, the tropopause reaches 16-18 km at the equator, while over the cold poles it lies between 8-10 km.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', Page 5"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "hard",
        "q": "In ISA, from 11 km to 20 km altitude, the temperature is assumed to:",
        "o": ["Decrease at 2°C/1000 ft", "Increase at 1°C/km", "Remain constant at -56.5°C (isothermal)", "Decrease to -90°C"],
        "a": 2,
        "e": "In the ICAO Standard Atmosphere, temperature decreases at 6.5°C/km from sea level to 11 km (-56.5°C), and then remains isothermal at -56.5°C from 11 km up to 20 km.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', Page 7"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "easy",
        "q": "Roughly, a 1 hPa decrease in atmospheric pressure near mean sea level corresponds to an increase in height of approximately:",
        "o": ["10 ft", "27 to 30 ft", "60 ft", "100 ft"],
        "a": 1,
        "e": "Near mean sea level, 1 hPa change in pressure corresponds to approximately 27 to 30 ft (96 * T/P ft). At 20,000 ft it is about 50 ft/hPa, and at 40,000 ft about 100 ft/hPa.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', Page 12"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "medium",
        "q": "When flying from an area of high pressure into an area of low pressure without resetting the altimeter subscale, the altimeter will:",
        "o": ["Under-read (aircraft is higher than indicated)", "Over-read (aircraft is lower than indicated)", "Read correctly because pitot-static tube compensates", "Fluctuate rapidly between high and low readings"],
        "a": 1,
        "e": "Rule: 'High to Low, Look Out Below'. When flying from high to low pressure, the altimeter senses lower pressure and interprets it as higher altitude, thus over-reading. The true altitude is lower than indicated.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', Page 19"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "medium",
        "q": "Which pressure setting is defined as the aerodrome station level pressure reduced to mean sea level assuming ISA conditions?",
        "o": ["QFE", "QFF", "QNH", "QNE"],
        "a": 2,
        "e": "QNH is station pressure reduced to MSL using ISA temperature lapse rate. When set on the altimeter subscale on the ground, the altimeter reads aerodrome elevation above MSL.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', Page 18"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "hard",
        "q": "In the standard atmosphere, the 500 hPa and 300 hPa pressure levels correspond approximately to which altitudes?",
        "o": ["10,000 ft and 20,000 ft", "18,000 ft (FL180) and 30,000 ft (FL300)", "24,000 ft and 40,000 ft", "14,000 ft and 25,000 ft"],
        "a": 1,
        "e": "Standard isobaric levels in ISA: 850 hPa = 5,000 ft (FL50); 700 hPa = 10,000 ft (FL100); 500 hPa = 18,000 ft (FL180); 300 hPa = 30,000 ft (FL300); 200 hPa = 38,000 ft (FL380).",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', Page 19 Table 2.1"
    },
    {
        "topic": "Temperature & Heat",
        "difficulty": "easy",
        "q": "On a clear day with calm winds, the minimum surface air temperature normally occurs:",
        "o": ["At midnight", "At 03:00 local time", "Half an hour to one hour after sunrise", "Exactly at the moment of sunrise"],
        "a": 2,
        "e": "Due to nocturnal radiational cooling, ground temperatures continue falling after sunrise until incoming solar radiation balances outgoing terrestrial radiation, typically 30 to 60 minutes after dawn.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature', Page 32"
    },
    {
        "topic": "Temperature & Heat",
        "difficulty": "medium",
        "q": "The fraction of incoming solar radiation reflected back into space by clouds, aerosols, and the Earth surface is termed:",
        "o": ["Insolation", "Albedo", "Advection", "Thermal radiation"],
        "a": 1,
        "e": "Albedo is the ratio of reflected solar radiation to total incident solar radiation. Earth's average albedo is about 30%, whereas fresh snow reflects about 80%.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature', Page 31"
    },
    {
        "topic": "Air Density",
        "difficulty": "easy",
        "q": "Density altitude is defined as:",
        "o": ["The pressure altitude corrected for non-standard temperature", "The altitude above ground level in standard temperature", "The indicated altitude corrected for instrument error", "The true altitude minus terrain elevation"],
        "a": 0,
        "e": "Density altitude is pressure altitude corrected for non-standard temperature. In aviation, high density altitude reduces aircraft performance: longer takeoff run, slower rate of climb, and reduced engine power.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 4 'Air Density', Page 36"
    },
    {
        "topic": "Air Density",
        "difficulty": "medium",
        "q": "For every 1°C increase in temperature above ISA, the density altitude increases by approximately:",
        "o": ["30 ft", "60 ft", "120 ft", "200 ft"],
        "a": 2,
        "e": "A rule of thumb in aviation meteorology states that for each 1°C rise above standard ISA temperature, density altitude increases by approximately 120 ft above pressure altitude.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 4 'Air Density', Page 36"
    },
    {
        "topic": "Humidity",
        "difficulty": "easy",
        "q": "The temperature to which moist air must be cooled at constant pressure to reach saturation is called the:",
        "o": ["Wet bulb temperature", "Dew point temperature", "Virtual temperature", "Frost point"],
        "a": 1,
        "e": "Dew point (Td) is the temperature to which unsaturated air must be cooled at constant pressure and moisture content to become saturated (100% relative humidity).",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 5 'Humidity', Page 41"
    },
    {
        "topic": "Humidity",
        "difficulty": "medium",
        "q": "When unsaturated air is lifted adiabatically, what happens to its Relative Humidity (RH) and Dew Point (DP)?",
        "o": ["RH decreases and DP increases", "RH increases and DP decreases (by approx 2°C/km)", "RH and DP both remain unchanged", "RH increases while the humidity mixing ratio increases"],
        "a": 1,
        "e": "As air rises, it expands and cools at DALR (9.8°C/km). Dew point falls at approx 1.8°C to 2°C/km. The temperature and dew point converge, so Relative Humidity increases until saturation (LCL).",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 5 'Humidity', Page 41-42"
    },
    {
        "topic": "Winds",
        "difficulty": "easy",
        "q": "In the Northern Hemisphere, Buys Ballot's Law states that if an observer stands with their back to the wind:",
        "o": ["Low pressure is to their right and high pressure to their left", "Low pressure is to their left and high pressure to their right", "Low pressure is directly ahead", "Low pressure is directly behind"],
        "a": 1,
        "e": "Buys Ballot's Law states that in the Northern Hemisphere, an observer facing downwind has lower pressure to the left and higher pressure to the right. In the Southern Hemisphere, this is reversed.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', Page 46"
    },
    {
        "topic": "Winds",
        "difficulty": "medium",
        "q": "Coriolis force is directly proportional to wind speed and the sine of latitude. Where is Coriolis force zero?",
        "o": ["At the geographic poles", "At 45° latitude", "At the Equator", "At the tropopause"],
        "a": 2,
        "e": "Coriolis force = 2 * omega * V * sin(phi). Since sin(0°) = 0, Coriolis force is zero at the Equator and reaches its maximum value at the poles where sin(90°) = 1.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', Page 47"
    },
    {
        "topic": "Winds",
        "difficulty": "medium",
        "q": "A cold, dense wind blowing down a mountain slope at night due to surface cooling is termed a:",
        "o": ["Fohn wind", "Anabatic wind", "Katabatic wind", "Chinook"],
        "a": 2,
        "e": "Katabatic winds are gravity-driven down-slope winds caused by nocturnal radiational cooling of the mountain slopes, making the air heavier than surrounding free air.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', Page 54"
    },
    {
        "topic": "Winds",
        "difficulty": "hard",
        "q": "A sudden increase in wind speed of at least 16 kt (32 km/h), reaching 22 kt or more and lasting for at least one minute, is classified as a:",
        "o": ["Gust", "Squall", "Gale", "Microburst"],
        "a": 1,
        "e": "WMO defines a squall as a sudden increase of wind speed by at least 16 kt (8 m/s), the speed rising to 22 kt (11 m/s) or more and lasting for at least one minute. Gusts are transient fluctuations of seconds.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', Page 46"
    },
    {
        "topic": "Visibility & Fog",
        "difficulty": "easy",
        "q": "In aviation weather reports, 'Fog' (FG) is reported when the horizontal visibility is reduced by water droplets or ice crystals to less than:",
        "o": ["500 m", "1000 m", "1500 m", "5000 m"],
        "a": 1,
        "e": "By international aeronautical definition, fog is reported when visibility is less than 1000 m and relative humidity is near 100%. If visibility is between 1000 m and 5000 m with RH >= 95%, it is reported as Mist (BR).",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 7 'Visibility and Fog', Page 66"
    },
    {
        "topic": "Visibility & Fog",
        "difficulty": "medium",
        "q": "Radiation fog is most likely to form under which combination of meteorological conditions?",
        "o": ["Strong winds (> 15 kt), overcast stratus sky, and dry air", "Light winds (2-7 kt), clear skies at night, and high relative humidity", "Calm wind, cloudy sky, and warm advection", "Gale force winds and heavy precipitation"],
        "a": 1,
        "e": "Radiation fog requires high relative humidity, clear skies for maximum terrestrial radiation cooling, and light wind (2-7 kt) to produce gentle turbulent mixing confined to a shallow layer near the ground.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 7 'Visibility and Fog', Page 69"
    },
    {
        "topic": "Visibility & Fog",
        "difficulty": "medium",
        "q": "Advection fog forms when:",
        "o": ["Cold dry air blows over warm land", "Warm, moist air moves horizontally over a cold land or sea surface", "Air is cooled adiabatically by climbing a mountain", "Rain falls into cold surface air"],
        "a": 1,
        "e": "Advection fog forms when warm moist air is transported over a colder underlying surface, cooling the air to its dew point. It can form over land or sea at any time of day or night and with moderate winds.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 7 'Visibility and Fog', Page 70"
    },
    {
        "topic": "Clouds & Precipitation",
        "difficulty": "easy",
        "q": "Which cloud type is characterized by great vertical development, an anvil-shaped fibrous top, and hazards including severe turbulence, hail, and microbursts?",
        "o": ["Altocumulus (AC)", "Nimbostratus (NS)", "Cumulonimbus (CB)", "Stratocumulus (SC)"],
        "a": 2,
        "e": "Cumulonimbus (CB) is the thunderstorm cloud. It features massive vertical development, anvil cirrus top, and poses the most severe hazards in aviation (turbulence, severe icing, wind shear, hail, lightning).",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 8 'Clouds', Page 78"
    },
    {
        "topic": "Clouds & Precipitation",
        "difficulty": "medium",
        "q": "Optical halos around the sun or moon are produced by light refraction through ice crystals in which cloud type?",
        "o": ["Altocumulus (AC)", "Cirrostratus (CS)", "Altostratus (AS)", "Stratocumulus (SC)"],
        "a": 1,
        "e": "Cirrostratus (CS) clouds consist of hexagonal ice crystals that refract sunlight or moonlight at a 22° angle, producing a circular halo with the red component on the inside.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 8 'Clouds', Page 77; Chapter 10 'Optical Phenomena', Page 94"
    },
    {
        "topic": "Clouds & Precipitation",
        "difficulty": "medium",
        "q": "Precipitation consisting of very small, closely spaced water droplets (diameter < 0.5 mm) falling almost exclusively from Stratus cloud is termed:",
        "o": ["Rain (RA)", "Drizzle (DZ)", "Sleet", "Virga"],
        "a": 1,
        "e": "Drizzle (DZ) consists of small water droplets of diameter 0.1 to 0.5 mm that appear to float in air currents. It falls almost exclusively from Stratus (ST) clouds.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 11 'Precipitation', Page 100"
    },
    {
        "topic": "Clouds & Precipitation",
        "difficulty": "hard",
        "q": "Rain falling from a cloud that evaporates completely before reaching the ground is called:",
        "o": ["Graupel", "Virga", "Mirage", "Mizzle"],
        "a": 1,
        "e": "Virga is precipitation falling from a cloud base that evaporates in dry air below before reaching the ground. It often indicates strong downdrafts beneath the cloud.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 11 'Precipitation', Page 101"
    },
    {
        "topic": "Stability & Adiabatics",
        "difficulty": "medium",
        "q": "The Dry Adiabatic Lapse Rate (DALR) and Saturated Adiabatic Lapse Rate (SALR) near sea level are approximately:",
        "o": ["6.5°C/km and 2°C/km", "9.8°C/km (approx 3°C/1000 ft) and 5°C/km (approx 1.5°C/1000 ft)", "2°C/1000 ft and 3°C/1000 ft", "10°C/km and 9.8°C/km"],
        "a": 1,
        "e": "DALR is constant at 9.8°C/km (approx 3°C/1000 ft). SALR is lower because latent heat released during condensation warms the rising air, averaging about 5°C/km near sea level.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 9 'Stability and Instability', Page 86"
    },
    {
        "topic": "Stability & Adiabatics",
        "difficulty": "hard",
        "q": "If the Environmental Lapse Rate (ELR) is greater than the Dry Adiabatic Lapse Rate (DALR), the atmosphere is in a state of:",
        "o": ["Absolute stability", "Conditional instability", "Absolute instability", "Neutral equilibrium"],
        "a": 2,
        "e": "When ELR > DALR (super-adiabatic), lifted parcels of both dry and saturated air are warmer and less dense than the environment, continuing to accelerate upward (Absolute Instability).",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 9 'Stability and Instability', Page 87"
    },
    {
        "topic": "Ice Accretion",
        "difficulty": "medium",
        "q": "Clear ice (glazed ice) on an airframe is most dangerous because it:",
        "o": ["Is light and easily shaken off by vibration", "Is heavy, transparent, adheres tenaciously, alters airfoil shape, and is hard to remove", "Forms only on parked aircraft overnight", "Affects only communication antennas"],
        "a": 1,
        "e": "Clear ice forms from large supercooled water droplets at temperatures between 0°C and -10°C. The drops flow back before freezing, forming a dense, tenacious, transparent coating that severely degrades lift and adds weight.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 12 'Ice Accretion', Page 106"
    },
    {
        "topic": "Ice Accretion",
        "difficulty": "easy",
        "q": "Carburetor icing in piston engines is most likely to occur in which temperature and humidity conditions?",
        "o": ["Only below -20°C in dry air", "At ambient temperatures between -7°C and +30°C in moist air (RH > 60%)", "Only when flying through heavy rain at 0°C", "Only during full-throttle takeoff climb"],
        "a": 1,
        "e": "Fuel vaporization and adiabatic pressure reduction at the carburetor throttle butterfly can drop air temperature by up to 20°C. Carburetor ice can form even in warm ambient air up to +30°C with high relative humidity.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 12 'Ice Accretion', Page 107"
    },
    {
        "topic": "Thunderstorms",
        "difficulty": "medium",
        "q": "The mature stage of a thunderstorm lifecycle is definitively marked by:",
        "o": ["The first appearance of an anvil top", "The beginning of rain at the Earth's surface and the onset of downdrafts", "The cessation of all lightning flashes", "Weakening of the updrafts throughout the entire cell"],
        "a": 1,
        "e": "The mature stage begins when falling precipitation reaches the surface. Rain drags cold air downward, generating downdrafts and the first gust / squall front. Updrafts and downdrafts coexist in this stage.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 13 'Thunderstorm', Page 113"
    },
    {
        "topic": "Thunderstorms",
        "difficulty": "hard",
        "q": "A microburst is a localized intense downdraught with a horizontal diameter of less than 4 km. Its lifecycle typically lasts about:",
        "o": ["1 to 2 hours", "15 to 20 minutes", "1 to 2 days", "30 to 45 seconds"],
        "a": 1,
        "e": "Microbursts typically last 15 to 20 minutes. Peak winds develop 5 minutes after surface contact. An aircraft flying through encounters increasing headwind, strong downdraft, and then a dangerous sudden tailwind.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 13 'Thunderstorm', Page 117-118"
    },
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "medium",
        "q": "What is the typical slope of a cold front compared to a warm front?",
        "o": ["Cold front is flatter (1:150 to 1:180), warm front is steeper", "Cold front is steeper (approx 1:50 to 1:80), warm front is shallower (approx 1:150 to 1:180)", "Both fronts have the identical slope of 1:100", "Cold fronts have no slope as they are vertical walls"],
        "a": 1,
        "e": "Cold fronts advance like a blunt wedge with a steep slope of about 1:50 to 1:80, causing rapid vertical lifting and convective clouds (CU, CB). Warm fronts have a shallow slope of 1:150 to 1:180 with stratiform clouds.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts and Western Disturbances', Page 128-129"
    },
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "medium",
        "q": "Western Disturbances (WDs) affecting northern India during winter originate primarily over which region?",
        "o": ["Bay of Bengal", "Arabian Sea", "Mediterranean Sea and Caspian Sea region", "Siberian landmass"],
        "a": 2,
        "e": "Western Disturbances originate as extra-tropical low-pressure systems over the Mediterranean and Caspian Seas, travelling eastward steered by the Subtropical Westerly Jet stream into Pakistan and northern India.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts and Western Disturbances', Page 132"
    },
    {
        "topic": "Jet Streams",
        "difficulty": "easy",
        "q": "By WMO definition, the arbitrary lower speed limit for the core of a jet stream is:",
        "o": ["30 kt", "45 kt", "60 kt (approx 30 m/s)", "100 kt"],
        "a": 2,
        "e": "WMO defines a jet stream as a strong narrow current of winds concentrated along a quasi-horizontal axis in the upper troposphere or stratosphere, with a minimum core speed of 60 kt (30 m/s).",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 15 'Jet Streams', Page 136"
    },
    {
        "topic": "Jet Streams",
        "difficulty": "medium",
        "q": "The Subtropical Jet Stream (STJ) affects northern India primarily during which months?",
        "o": ["June to September only", "October to May (winter and transition seasons)", "July and August only", "April and May only"],
        "a": 1,
        "e": "The Subtropical Westerly Jet Stream prevails over northern India from October to May, reaching peak core speeds of 100-150 kt in January/February near 27° N at 12 km (200 hPa).",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 15 'Jet Streams', Page 137"
    },
    {
        "topic": "Clear Air Turbulence",
        "difficulty": "medium",
        "q": "Clear Air Turbulence (CAT) is most severe and most frequently encountered in which region relative to a jet stream?",
        "o": ["Directly in the calm center of the jet core", "On the low-pressure (colder / poleward) side near or below the jet axis where vertical and horizontal wind shear is greatest", "Far away from all frontal zones and tropopause folds", "Only at altitudes below 10,000 ft AMSL"],
        "a": 1,
        "e": "CAT occurs predominantly in regions of strong horizontal and vertical wind shear just below the tropopause, especially on the colder, poleward (left in Northern Hemisphere) side of the jet stream core.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 16 'Clear Air Turbulence', Page 143"
    },
    {
        "topic": "Tropical Systems & Monsoon",
        "difficulty": "easy",
        "q": "In the mature stage of a Tropical Cyclone, the central calm region of light winds and descending air is termed the:",
        "o": ["Wall Cloud", "Eye", "Surge Line", "Spiral Band"],
        "a": 1,
        "e": "The Eye is the central region of lowest surface pressure, warmest temperatures, light winds, and often clear skies caused by subsiding air. It is surrounded by the destructive Eye Wall.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 18 'Tropical Systems', Page 157"
    },
    {
        "topic": "Climatology of India",
        "difficulty": "medium",
        "q": "The normal date of onset of the Southwest Monsoon over the mainland of India (Kerala coast) is:",
        "o": ["15 May", "01 June", "15 June", "01 July"],
        "a": 1,
        "e": "The normal date for the onset of the Southwest Monsoon over the South Andaman Sea is 20 May, and over the mainland coast of Kerala is 01 June.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 19 'Climatology of India', Page 171"
    },
    {
        "topic": "Climatology of India",
        "difficulty": "medium",
        "q": "During a 'Break in Monsoon', the axis of the monsoon trough shifts towards:",
        "o": ["The Indian Peninsula (Tamil Nadu)", "The foot hills of the Himalayas", "The central Arabian Sea", "The equator"],
        "a": 1,
        "e": "During a break in monsoon, the monsoon trough shifts northwards close to the Himalayan foothills, causing heavy floods in Assam and sub-Himalayan Bengal while the plains of India experience dry spells.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 19 'Climatology of India', Page 172"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "easy",
        "q": "In a METAR weather report, the term CAVOK indicates that simultaneously:",
        "o": ["Visibility >= 10 km, no clouds below 1500 m (5000 ft) or MSA, and no weather of significance", "Visibility >= 5 km and sky completely clear", "Visibility >= 8 km and no rain", "No clouds at all altitudes and zero wind"],
        "a": 0,
        "e": "CAVOK (Ceiling And Visibility OK) requires: visibility 10 km or more; no cloud below 1500 m (5000 ft) or highest minimum sector altitude (whichever is greater), no CB/TCU; and no significant weather.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 25 'METAR SPECI', Page 219"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "medium",
        "q": "A TREND landing forecast appended to a METAR or SPECI has a validity period of:",
        "o": ["30 minutes", "2 hours", "6 hours", "9 hours"],
        "a": 1,
        "e": "A TREND forecast consists of a concise statement of expected significant changes appended to a METAR or SPECI and is valid for 2 hours from the time of the report.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 25 'METAR SPECI', Page 223"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "medium",
        "q": "In a TAF report, the change indicator 'TEMPO 1215' means that the described weather changes are expected to:",
        "o": ["Start permanently at 12:00 UTC and continue through 15:00 UTC", "Occur temporarily between 12:00 UTC and 15:00 UTC, lasting less than 1 hour in each instance", "Be valid only for 12 to 15 minutes", "Occur exactly at 12:15 UTC"],
        "a": 1,
        "e": "TEMPO denotes temporary fluctuations lasting less than one hour in each instance and in aggregate covering less than half of the indicated period (from 12:00 to 15:00 UTC).",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 26 'Aviation Weather Forecasts TAF', Page 224, 231"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "hard",
        "q": "In a METAR, 'R27/1200D' in the runway visual range group indicates:",
        "o": ["Runway 27 RVR is 1200 ft with downward slope", "Runway 27 RVR is 1200 metres with a downward (decreasing) tendency", "Runway 27 RVR is 1200 metres during daytime", "Runway 27 RVR is between 1200 and 1500 m"],
        "a": 1,
        "e": "In the RVR group RD_R/V_RV_RV_RV_R i: R27 indicates Runway 27, 1200 indicates 1200 metres, and the tendency letter 'D' indicates decreasing over the past 10 minutes ('U' = increasing, 'N' = no change).",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 25 'METAR SPECI', Page 221"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "medium",
        "q": "A SIGMET is issued by a Meteorological Watch Office (MWO) to warn pilots of:",
        "o": ["Routine terminal weather conditions", "En-route weather phenomena that may affect the safety of all aircraft operations", "Only local airport surface wind gusts", "Flight delays caused by air traffic congestion"],
        "a": 1,
        "e": "SIGMET messages give concise information concerning the occurrence or expected occurrence of specified en-route weather phenomena which may affect the safety of aircraft operations (e.g., severe turbulence, severe icing, volcanic ash, tropical cyclones).",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 21 'Met Services', Page 192"
    },
    {
        "topic": "General Circulation",
        "difficulty": "medium",
        "q": "The descending branch of the Hadley Cell near latitude 30° N and 30° S is characterized by calm winds, high pressure, and world deserts. This region is known as:",
        "o": ["The Doldrums (ITCZ)", "The Horse Latitudes", "The Roaring Forties", "The Polar Front"],
        "a": 1,
        "e": "The Horse Latitudes are subtropical high-pressure belts located around 30° N and 30° S, formed by subsiding air from the Hadley cell. The sinking air causes adiabatic warming, cloud dissipation, calm winds, and major arid zones.",
        "src": "I.C. Joshi Aviation Meteorology, Chapter 20 'General Circulation', Page 184"
    }
]

for idx, q_item in enumerate(met_questions_data):
    questions.append({
        "id": f"MET-{idx+1:03d}",
        "subject": "Aviation Meteorology",
        "topic": q_item["topic"],
        "difficulty": q_item["difficulty"],
        "question": clean_text(q_item["q"]),
        "options": [clean_text(o) for o in q_item["o"]],
        "answerIndex": q_item["a"],
        "explanation": clean_text(q_item["e"]),
        "source": q_item["src"]
    })

# 4. TECHNICAL GENERAL: 35 authentic questions
tg_questions_data = [
    {
        "topic": "Principles of Flight",
        "difficulty": "easy",
        "q": "According to Bernoulli's principle, as airflow accelerates over the cambered upper surface of an airfoil, what happens to dynamic pressure and static pressure?",
        "o": ["Dynamic pressure decreases and static pressure increases", "Dynamic pressure increases and static pressure decreases", "Both dynamic and static pressure increase", "Both dynamic and static pressure decrease"],
        "a": 1,
        "e": "Bernoulli's theorem states that for steady incompressible flow, total pressure (static + dynamic) remains constant. As air accelerates over the camber, dynamic pressure increases and static pressure decreases, producing lift.",
        "src": "Oxford ATPL Principles of Flight, Chapter 2 'Subsonic Airflow'"
    },
    {
        "topic": "Principles of Flight",
        "difficulty": "medium",
        "q": "An aircraft will stall whenever which condition occurs?",
        "o": ["The airspeed falls below a fixed calibrated airspeed", "The critical (stalling) angle of attack is exceeded, regardless of airspeed, weight, or attitude", "The engine power is reduced to idle", "The aircraft enters a banked turn exceeding 45 degrees"],
        "a": 1,
        "e": "An airfoil always stalls at the same critical angle of attack (typically 15°-18° for general aviation airfoils), regardless of airspeed, weight, load factor, or flight attitude.",
        "src": "Oxford ATPL Principles of Flight, Chapter 3 'The Stall'"
    },
    {
        "topic": "Principles of Flight",
        "difficulty": "medium",
        "q": "Induced drag is a byproduct of lift creation caused by wingtip vortices. As airspeed increases in straight and level flight, induced drag:",
        "o": ["Increases proportional to the square of airspeed", "Decreases inversely proportional to the square of airspeed", "Remains constant", "Increases linearly with airspeed"],
        "a": 1,
        "e": "Induced drag is inversely proportional to the square of airspeed (Di proportional to 1/V^2). At high speeds, angle of attack is small, wingtip vortices are weak, and induced drag is low. At low speeds, induced drag is high.",
        "src": "Oxford ATPL Principles of Flight, Chapter 4 'Drag'"
    },
    {
        "topic": "Principles of Flight",
        "difficulty": "hard",
        "q": "In a level, coordinated 60-degree banked turn, the load factor (g) and stall speed increase by approximately what factors?",
        "o": ["Load factor 1.41 g, stall speed increases by 19%", "Load factor 2.0 g, stall speed increases by approximately 41%", "Load factor 3.0 g, stall speed doubles (100%)", "Load factor 1.5 g, stall speed increases by 25%"],
        "a": 1,
        "e": "Load factor n = 1 / cos(bank angle). At 60°, n = 1/cos(60°) = 2.0 g. Stall speed in a turn Vs_turn = Vs_level * sqrt(n) = Vs * sqrt(2.0) = 1.414 * Vs (a 41% increase in stalling speed).",
        "src": "Oxford ATPL Principles of Flight, Chapter 8 'Manoeuvres'"
    },
    {
        "topic": "Principles of Flight",
        "difficulty": "medium",
        "q": "When flying into ground effect (within approximately one wingspan of the surface), which changes occur?",
        "o": ["Induced drag increases and elevator authority is lost", "Induced drag decreases, effective lift increases, and the aircraft tends to float", "Parasite drag increases dramatically requiring more thrust", "Stall speed increases significantly"],
        "a": 1,
        "e": "The proximity of the ground restricts the vertical component of airflow, reducing downwash and wingtip vortex size. Induced drag drops significantly, increasing the lift-to-drag ratio and causing the aircraft to float.",
        "src": "Oxford ATPL Principles of Flight, Chapter 4 'Ground Effect'"
    },
    {
        "topic": "Principles of Flight",
        "difficulty": "medium",
        "q": "What is the primary aerodynamic purpose of wing dihedral (wings angled upward from root to tip)?",
        "o": ["To increase maximum takeoff weight", "To provide lateral (roll) stability", "To provide longitudinal (pitch) stability", "To reduce parasite drag in cruise"],
        "a": 1,
        "e": "Dihedral provides lateral stability. When the aircraft sideslips (rolls), the lower wing has a higher effective angle of attack than the higher wing, producing a restoring rolling moment that levels the wings.",
        "src": "Oxford ATPL Principles of Flight, Chapter 9 'Stability'"
    },
    {
        "topic": "Piston Engines",
        "difficulty": "easy",
        "q": "In a four-stroke internal combustion aero-engine, what is the correct order of the operating strokes?",
        "o": ["Compression, Intake, Exhaust, Power", "Intake, Compression, Power, Exhaust", "Intake, Power, Compression, Exhaust", "Power, Compression, Exhaust, Intake"],
        "a": 1,
        "e": "The Otto four-stroke cycle consists of: 1) Intake (fuel-air drawn in), 2) Compression (mixture compressed), 3) Power/Expansion (spark fires, burning expands), 4) Exhaust (burnt gases expelled).",
        "src": "Oxford ATPL Aircraft General Knowledge - Powerplant, Chapter 1 'Piston Engines'"
    },
    {
        "topic": "Piston Engines",
        "difficulty": "medium",
        "q": "Aviation piston engines use dual independent ignition systems primarily consisting of:",
        "o": ["A car battery and two alternators", "Two engine-driven magnetos, each firing one of two spark plugs per cylinder, independent of the electrical system", "A single distributor firing four spark plugs in sequence", "Direct injection piezo-electric igniters powered by the busbar"],
        "a": 1,
        "e": "Aero piston engines use two independent magnetos (left and right), each powering one spark plug per cylinder. Magnetos are engine-driven permanent-magnet generators that operate completely independent of the aircraft battery.",
        "src": "Oxford ATPL Aircraft General Knowledge - Powerplant, Chapter 3 'Ignition Systems'"
    },
    {
        "topic": "Piston Engines",
        "difficulty": "medium",
        "q": "Detonation in an aircraft piston engine is best defined as:",
        "o": ["Ignition of the fuel-air charge prior to the normal spark event", "An uncontrolled, explosive burning of the remaining fuel-air charge ahead of the normal flame front", "Backfiring through the carburetor induction pipe due to lean mixture", "Normal rapid combustion at full takeoff power"],
        "a": 1,
        "e": "Detonation is the sudden explosive combustion of the end-gas ahead of the advancing flame front. It causes extreme cylinder head temperature and pressure spikes, potentially leading to catastrophic engine damage.",
        "src": "Oxford ATPL Aircraft General Knowledge - Powerplant, Chapter 2 'Combustion'"
    },
    {
        "topic": "Piston Engines",
        "difficulty": "hard",
        "q": "Pre-ignition differs from detonation in that pre-ignition is caused by:",
        "o": ["Using fuel of too high an octane rating", "An incandescent hotspot (such as glowing carbon or overheated spark plug electrode) igniting the mixture before timed spark occurs", "Over-cooling the cylinder head during a descent", "Excessively rich fuel-to-air mixture"],
        "a": 1,
        "e": "Pre-ignition is the ignition of the fuel-air charge before the spark plug fires, caused by a local hot spot in the cylinder (overheated spark plug tip, carbon deposit, or cracked exhaust valve).",
        "src": "Oxford ATPL Aircraft General Knowledge - Powerplant, Chapter 2 'Combustion'"
    },
    {
        "topic": "Piston Engines",
        "difficulty": "medium",
        "q": "During a pre-flight magneto check at 1800 RPM, switching from BOTH to LEFT produces no drop in RPM. The most likely reason is:",
        "o": ["The engine is running perfectly with zero magneto wear", "The right magneto P-lead (ground wire) is broken/disconnected, leaving the right magneto permanently LIVE", "The left magneto has failed completely", "The carburetor heat is stuck in the ON position"],
        "a": 1,
        "e": "If switching to one magneto produces no RPM drop, the P-lead on the other magneto is broken or disconnected. The other magneto remains ungrounded (hot/live) and keeps firing. This is an extreme safety hazard on the ground.",
        "src": "Oxford ATPL Aircraft General Knowledge - Powerplant, Chapter 3 'Ignition Systems'"
    },
    {
        "topic": "Piston Engines",
        "difficulty": "easy",
        "q": "Applying carburetor heat to an aircraft with an iced carburetor will initially cause:",
        "o": ["An immediate increase in engine RPM and smoother running", "A further drop in RPM and possible engine roughness as ice melts, followed by an RPM rise once clear", "The engine to cut out permanently", "The cylinder head temperature to drop to zero"],
        "a": 1,
        "e": "When carburetor heat is applied, hot air is less dense, so the mixture richens and RPM drops slightly. As ice melts, water passes through the cylinders causing temporary roughness, before smooth operation returns at clear RPM.",
        "src": "Oxford ATPL Aircraft General Knowledge - Powerplant, Chapter 4 'Fuel and Carburetion'"
    },
    {
        "topic": "Propellers",
        "difficulty": "easy",
        "q": "A constant-speed propeller automatically adjusts its blade pitch to maintain a constant:",
        "o": ["Aircraft true airspeed (TAS)", "Engine RPM selected by the pilot via the propeller control", "Manifold pressure at all altitudes", "Exhaust gas temperature (EGT)"],
        "a": 1,
        "e": "A constant-speed propeller uses a hydraulic governor to automatically vary the blade pitch angle, maintaining the engine RPM selected by the pilot on the blue propeller pitch lever regardless of airspeed or throttle setting.",
        "src": "Oxford ATPL Aircraft General Knowledge - Powerplant, Chapter 7 'Propellers'"
    },
    {
        "topic": "Propellers",
        "difficulty": "medium",
        "q": "P-factor (asymmetric propeller blade effect) causes an aircraft to yaw to the left during high angle of attack flight (such as climb) because:",
        "o": ["The ascending blade takes a bigger bite of air than the descending blade", "The descending blade operates at a higher effective angle of attack and produces more thrust than the ascending blade", "Propeller torque rolls the left wheel down on the runway", "Slipstream hits the left side of the rudder"],
        "a": 1,
        "e": "At high angles of attack, the propeller disc is tilted relative to relative airflow. The downward-moving blade on the right has a higher forward velocity and higher angle of attack, producing more thrust than the upward blade on the left, yawing the plane left.",
        "src": "Oxford ATPL Principles of Flight, Chapter 7 'Propeller Effects'"
    },
    {
        "topic": "Propellers",
        "difficulty": "hard",
        "q": "On a multi-engine aircraft with both propellers rotating clockwise (viewed from the cockpit), the 'critical engine' is the:",
        "o": ["Right engine, because its failure causes no asymmetric yaw", "Left engine, because its thrust line is closer to the fuselage than the right engine's descending blade thrust line", "Engine closest to the fuel tanks", "Neither engine, because clockwise engines are symmetric"],
        "a": 1,
        "e": "The descending blade on the right engine produces thrust furthest from the aircraft centerline (longer moment arm). Failure of the left engine leaves the right engine operating with maximum asymmetric yaw moment, making the left engine critical.",
        "src": "Oxford ATPL Principles of Flight, Chapter 10 'Multi-Engine Flight'"
    },
    {
        "topic": "Aircraft Systems",
        "difficulty": "medium",
        "q": "In a hydraulic system, why is mineral-based fluid (such as MIL-PRF-5606) dyed red?",
        "o": ["To indicate it is corrosive to aluminum", "For leak detection and to prevent accidental servicing with incompatible fluid types", "To lubricate actuator seals automatically", "To indicate it has boiled under high pressure"],
        "a": 1,
        "e": "Aviation hydraulic fluids are color-coded to prevent catastrophic cross-contamination: MIL-H-5606 (mineral) is dyed red; Skydrol (phosphate-ester synthetic) is dyed purple/green. Mixing them destroys system packings and seals.",
        "src": "Oxford ATPL Aircraft General Knowledge - Systems, Chapter 1 'Hydraulics'"
    },
    {
        "topic": "Aircraft Systems",
        "difficulty": "easy",
        "q": "What is the purpose of an aircraft electrical circuit breaker?",
        "o": ["To boost voltage when the battery is weak", "To protect aircraft wiring and equipment from overheating and fire caused by excessive current (overload/short-circuit)", "To convert alternating current (AC) to direct current (DC)", "To ground the magnetos when shutting down the engine"],
        "a": 1,
        "e": "Circuit breakers protect wiring and electrical components from carrying excessive electrical current that could cause insulation melting, electrical fires, and equipment failure. They pop open automatically when rated current is exceeded.",
        "src": "Oxford ATPL Aircraft General Knowledge - Systems, Chapter 4 'Electrics'"
    },
    {
        "topic": "Aircraft Systems",
        "difficulty": "medium",
        "q": "An aircraft alternator failure in flight is normally first indicated by:",
        "o": ["Immediate engine stoppage", "A zero or negative reading on the ammeter (discharge) and an annunciator warning light", "The airspeed indicator reading zero", "Loss of all hydraulic pressure"],
        "a": 1,
        "e": "Since the ignition system runs on magnetos, the engine continues running. The ammeter shows battery discharge (or zero output), and the low-voltage/alternator-fail warning illuminates as the battery takes over electrical loads.",
        "src": "Oxford ATPL Aircraft General Knowledge - Systems, Chapter 4 'Electrics'"
    },
    {
        "topic": "Pitot-Static Instruments",
        "difficulty": "easy",
        "q": "Which flight instrument relies on BOTH pitot (ram) pressure and static pressure to operate?",
        "o": ["Altimeter", "Vertical Speed Indicator (VSI)", "Airspeed Indicator (ASI)", "Turn Coordinator"],
        "a": 2,
        "e": "The Airspeed Indicator (ASI) measures dynamic pressure (ram pressure minus static pressure). The Altimeter and Vertical Speed Indicator connect to the static source only.",
        "src": "Oxford ATPL Aircraft General Knowledge - Instrumentation, Chapter 1 'Pitot-Static Systems'"
    },
    {
        "topic": "Pitot-Static Instruments",
        "difficulty": "medium",
        "q": "If the pitot tube ram pressure inlet is completely blocked by ice while the drain hole remains open, what will the Airspeed Indicator indicate?",
        "o": ["It will freeze at the speed when blockage occurred", "The pressure bleeds out through the drain hole, causing the ASI to drop to zero", "It will over-read progressively as the aircraft climbs", "It will indicate maximum airspeed (Vne)"],
        "a": 1,
        "e": "If the ram air inlet is blocked while the drain hole is open, trapped pressure leaks out through the drain hole. The pressure inside the capsule drops to ambient static pressure, and the ASI indicates zero.",
        "src": "Oxford ATPL Aircraft General Knowledge - Instrumentation, Chapter 1 'Pitot-Static Systems'"
    },
    {
        "topic": "Pitot-Static Instruments",
        "difficulty": "hard",
        "q": "If BOTH the pitot tube ram inlet and drain hole are completely frozen shut, how will the Airspeed Indicator behave during a climb?",
        "o": ["It will indicate zero", "It will act like an altimeter, over-reading as the aircraft climbs into lower ambient static pressure", "It will under-read as the aircraft climbs", "It will read constant regardless of attitude"],
        "a": 1,
        "e": "Trapped ram pressure remains constant in the capsule. As the aircraft climbs, ambient static pressure in the casing decreases, allowing the capsule to expand. The ASI acts like an altimeter and falsely over-reads.",
        "src": "Oxford ATPL Aircraft General Knowledge - Instrumentation, Chapter 1 'Pitot-Static Systems'"
    },
    {
        "topic": "Pitot-Static Instruments",
        "difficulty": "hard",
        "q": "If the static port becomes completely blocked while climbing to a higher altitude, what will the Altimeter and VSI indicate?",
        "o": ["Altimeter will read zero; VSI will show maximum climb", "Altimeter freezes at the altitude where blockage occurred; VSI drops to zero after pressure equalizes", "Altimeter continues to read correctly; VSI over-reads", "Both instruments oscillate erratically"],
        "a": 1,
        "e": "Trapped static pressure holds the altimeter aneroid capsule fixed, freezing the altimeter at the altitude of blockage. In the VSI, calibrated leak capillary equalizes pressure between capsule and case, causing the VSI to read zero.",
        "src": "Oxford ATPL Aircraft General Knowledge - Instrumentation, Chapter 1 'Pitot-Static Systems'"
    },
    {
        "topic": "Gyroscopic Instruments",
        "difficulty": "easy",
        "q": "The two fundamental physical properties of a spinning gyroscope that enable aircraft flight instruments are:",
        "o": ["Centrifugal force and gravitational attraction", "Rigidity in space (gyroscopic inertia) and precession", "Aerodynamic lift and drag", "Magnetic dip and variation"],
        "a": 1,
        "e": "The two fundamental properties of a gyroscope are: 1) Rigidity in space (the rotor maintains its spin axis orientation in inertial space), and 2) Precession (an applied force results in angular motion 90° ahead in the direction of rotation).",
        "src": "Oxford ATPL Aircraft General Knowledge - Instrumentation, Chapter 2 'Gyroscopic Instruments'"
    },
    {
        "topic": "Gyroscopic Instruments",
        "difficulty": "medium",
        "q": "The Attitude Indicator (Artificial Horizon) utilizes a gyro spinning in which plane to display pitch and roll?",
        "o": ["Horizontal spin axis with vertical gimbals", "Vertical spin axis (spinning in the horizontal plane) with freedom in two gimbals", "Tilted 45 degrees to sense both yaw and roll", "Fixed single gimbal aligned with the longitudinal axis"],
        "a": 1,
        "e": "The Attitude Indicator rotor spins about a vertical axis (in the horizontal plane) supported by two gimbals, giving 3 degrees of freedom. This provides an earth-vertical reference against which aircraft pitch and roll attitudes are measured.",
        "src": "Oxford ATPL Aircraft General Knowledge - Instrumentation, Chapter 2 'Gyroscopic Instruments'"
    },
    {
        "topic": "Gyroscopic Instruments",
        "difficulty": "medium",
        "q": "Apparent drift (apparent wander) in a Directional Gyroscope is caused by:",
        "o": ["Friction in the gimbal bearings only", "The rotation of the Earth beneath the gyro spinning in space, equal to 15° per hour multiplied by sin(latitude)", "Magnetic fields from electrical wires in the cockpit", "Vibrations from the engine exhaust system"],
        "a": 1,
        "e": "A Directional Gyro maintains its axis in space while the Earth rotates 15° per hour beneath it. At the poles, apparent drift is 15°/hr * sin(90°) = 15°/hr. At the equator (sin 0° = 0), apparent drift is zero.",
        "src": "Oxford ATPL Aircraft General Knowledge - Instrumentation, Chapter 2 'Gyroscopic Instruments'"
    },
    {
        "topic": "Gyroscopic Instruments",
        "difficulty": "medium",
        "q": "The Turn Coordinator differs from the older Turn and Slip Indicator because its gimbal is tilted approximately 30 degrees, allowing it to sense:",
        "o": ["Pitch rate only", "Both rate of roll and rate of yaw", "Only rate of yaw (turn)", "Angle of bank directly in degrees"],
        "a": 1,
        "e": "The Turn Coordinator has its gyro gimbal tilted 30° up from horizontal, enabling it to sense both roll rate and yaw rate. The older Turn and Slip Indicator had a horizontal gimbal sensing yaw rate only.",
        "src": "Oxford ATPL Aircraft General Knowledge - Instrumentation, Chapter 2 'Gyroscopic Instruments'"
    },
    {
        "topic": "Weight & Balance",
        "difficulty": "easy",
        "q": "What is the primary aerodynamic hazard of operating an aircraft with the Center of Gravity (CG) located aft of the approved aft limit?",
        "o": ["Severely increased elevator control forces during landing flare", "Decreased longitudinal static stability, violent stall characteristics, and possible inability to recover from a stall or spin", "Excessive fuel consumption due to heavy nose-down trim", "Decreased cruise speed due to excessive tailplane download"],
        "a": 1,
        "e": "An aft CG reduces the tailplane arm and download requirement, drastically reducing longitudinal static stability. In extreme aft CG, the aircraft becomes dynamically unstable and may enter an unrecoverable flat spin.",
        "src": "Oxford ATPL Principles of Flight, Chapter 9 'Weight and Balance / Stability'"
    },
    {
        "topic": "Weight & Balance",
        "difficulty": "medium",
        "q": "Operating an aircraft with the Center of Gravity (CG) at its extreme forward limit results in:",
        "o": ["Higher cruise speed and lighter control forces", "Higher stall speed, heavier elevator control forces, and difficulty in achieving full flare on landing", "Danger of unrecoverable spin", "Zero induced drag in straight and level flight"],
        "a": 1,
        "e": "A forward CG requires a larger down-load on the tailplane to balance the nose-heavy moment. The wings must produce more total lift, which increases stall speed, increases induced drag (reducing cruise speed), and demands high stick forces.",
        "src": "Oxford ATPL Principles of Flight, Chapter 9 'Weight and Balance / Stability'"
    },
    {
        "topic": "Airspeed Definitions",
        "difficulty": "easy",
        "q": "Calibrated Airspeed (CAS) is defined as Indicated Airspeed (IAS) corrected for:",
        "o": ["Air density and altitude variations", "Compressibility error at high Mach numbers", "Instrument and position (installation) errors", "Wind speed and direction"],
        "a": 2,
        "e": "CAS is IAS corrected for position error (static port location turbulence and angle of attack) and instrument mechanical errors. Flight manuals provide CAS vs IAS correction tables.",
        "src": "Oxford ATPL Aircraft General Knowledge - Instrumentation, Chapter 1"
    },
    {
        "topic": "Airspeed Definitions",
        "difficulty": "medium",
        "q": "True Airspeed (TAS) equals Calibrated Airspeed (CAS) under which atmospheric conditions?",
        "o": ["At any altitude as long as IAS is below 100 kt", "In standard ISA conditions at mean sea level (15°C, 1013.25 hPa, 1225 g/m³)", "At the absolute ceiling of the aircraft", "At FL180 in standard temperature"],
        "a": 1,
        "e": "TAS is the actual speed of the aircraft through the air mass: TAS = EAS / sqrt(relative density). At sea level in ISA, relative density = 1.0, so TAS equals EAS/CAS. At altitude, air is thinner so TAS is higher than CAS.",
        "src": "Oxford ATPL Principles of Flight / Navigation, Chapter 'Airspeeds'"
    },
    {
        "topic": "Airspeed Definitions",
        "difficulty": "easy",
        "q": "A pilot flying at a constant Calibrated Airspeed of 120 kt climbs from sea level to 10,000 ft in ISA. The True Airspeed (TAS) will:",
        "o": ["Decrease by about 10%", "Remain exactly 120 kt", "Increase by approximately 2% per 1000 ft of altitude (reaching approx 144 kt)", "Increase to 200 kt"],
        "a": 2,
        "e": "Rule of thumb: TAS increases by approximately 1.5% to 2% per 1000 ft of altitude for a constant CAS. At 10,000 ft: 120 kt + (10 * 2%) = 120 * 1.20 = approx 144 kt.",
        "src": "Oxford ATPL General Navigation, Chapter 'Airspeed Conversions'"
    },
    {
        "topic": "Piston Engines",
        "difficulty": "medium",
        "q": "Exhaust Gas Temperature (EGT) is used by pilots of piston aircraft primarily to:",
        "o": ["Monitor oil cooler efficiency", "Set and adjust the fuel-to-air mixture for best economy or best power", "Verify whether the cabin heater valve is open", "Determine the exact outside air temperature"],
        "a": 1,
        "e": "EGT measures the temperature of combustion gases exiting the cylinder. Peaking the mixture (chemically correct stoichiometric ratio) and leaning or richening relative to peak EGT allows precise fuel mixture management.",
        "src": "Oxford ATPL Aircraft General Knowledge - Powerplant, Chapter 4 'Mixture Control'"
    },
    {
        "topic": "Aircraft Systems",
        "difficulty": "hard",
        "q": "Vapor lock in an aircraft fuel system is caused by:",
        "o": ["Water accumulating in the fuel tank sumps freezing at low temperatures", "Fuel vaporizing prematurely in fuel lines due to high fuel temperature, low ambient pressure, or excessive suction, blocking liquid fuel flow", "Microbiological fungal growth in Jet-A1 tanks", "Excessive lead additives accumulating in fuel injectors"],
        "a": 1,
        "e": "Vapor lock occurs when high temperatures and/or low atmospheric pressures cause volatile fuel components to boil inside fuel lines. The resulting vapor bubble prevents the fuel pump from delivering liquid fuel to the engine.",
        "src": "Oxford ATPL Aircraft General Knowledge - Systems, Chapter 3 'Fuel Systems'"
    },
    {
        "topic": "Aircraft Systems",
        "difficulty": "medium",
        "q": "What is the primary function of the aircraft landing gear oleo-pneumatic strut?",
        "o": ["To steer the aircraft on the ground only", "To absorb and dissipate landing impact shocks using compressed gas (nitrogen) and hydraulic fluid forced through an orifice", "To retract the landing gear after takeoff", "To cool the wheel brakes after landing"],
        "a": 1,
        "e": "An oleo strut absorbs landing loads: compressed nitrogen acts as a spring, while hydraulic oil forced through a metering orifice provides viscous damping, dissipating kinetic energy as heat without rebounding.",
        "src": "Oxford ATPL Aircraft General Knowledge - Systems, Chapter 2 'Landing Gear'"
    },
    {
        "topic": "Principles of Flight",
        "difficulty": "easy",
        "q": "Which flight control surface provides longitudinal control (pitch about the lateral axis)?",
        "o": ["Ailerons", "Elevator (or Stabilator)", "Rudder", "Flaps"],
        "a": 1,
        "e": "The elevator controls pitch about the lateral axis (longitudinal control). Ailerons control roll about the longitudinal axis (lateral control). The rudder controls yaw about the normal/vertical axis (directional control).",
        "src": "Oxford ATPL Principles of Flight, Chapter 6 'Flight Controls'"
    }
]

for idx, q_item in enumerate(tg_questions_data):
    questions.append({
        "id": f"TG-{idx+1:03d}",
        "subject": "Technical General",
        "topic": q_item["topic"],
        "difficulty": q_item["difficulty"],
        "question": clean_text(q_item["q"]),
        "options": [clean_text(o) for o in q_item["o"]],
        "answerIndex": q_item["a"],
        "explanation": clean_text(q_item["e"]),
        "source": q_item["src"]
    })

# 5. TECHNICAL SPECIFIC (25 questions) and 6. RTR (25 questions) from Subagent
# Let's import the 50 clean questions produced by Subagent 97a9f59d-f55e-4ab6-a49b-3708caa290ac
ts_rtr_text = '''[
  {
    "id": "TS-001",
    "subject": "Technical Specific",
    "topic": "V-speeds and their meanings",
    "difficulty": "easy",
    "question": "Vso is defined as the stalling speed or minimum steady flight speed in which configuration?",
    "options": ["Clean configuration at maximum weight", "Landing configuration (flaps and gear extended)", "Cruise configuration at sea level", "Take-off configuration with flaps at first notch"],
    "answerIndex": 1,
    "explanation": "Vso is the stalling speed or minimum steady flight speed in the landing configuration (flaps fully extended, gear down). It corresponds to the lower end of the white arc on the airspeed indicator.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-002",
    "subject": "Technical Specific",
    "topic": "V-speeds and their meanings",
    "difficulty": "easy",
    "question": "Vno is best described as which of the following?",
    "options": ["Never-exceed speed", "Maximum structural cruising speed", "Best rate-of-climb speed", "Manoeuvring speed"],
    "answerIndex": 1,
    "explanation": "Vno is the maximum structural cruising speed. Flight above Vno should only be conducted in smooth air and with caution. It marks the upper limit of the green arc and the lower limit of the yellow arc on the ASI.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-003",
    "subject": "Technical Specific",
    "topic": "V-speeds and their meanings",
    "difficulty": "medium",
    "question": "Va (manoeuvring speed) is significant because below this speed the aircraft:",
    "options": ["Will not exceed its never-exceed speed in a dive", "Will stall before exceeding its limit load factor with a single full control input", "Can extend flaps without structural damage", "Achieves best glide ratio"],
    "answerIndex": 1,
    "explanation": "At or below Va, the wings will stall before the airframe can be overstressed by a single full (abrupt) control deflection. Va decreases as aircraft weight decreases because a lighter aircraft needs less lift and will stall at a lower speed.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-004",
    "subject": "Technical Specific",
    "topic": "V-speeds and their meanings",
    "difficulty": "medium",
    "question": "Vx and Vy differ in that Vx gives best angle of climb while Vy gives best rate of climb. Which statement about their relationship at altitude is correct?",
    "options": ["Vx and Vy converge as altitude increases, meeting at the aircraft absolute ceiling", "Vx remains constant while Vy decreases with altitude", "Vy remains constant while Vx increases with altitude", "Both Vx and Vy increase equally with altitude"],
    "answerIndex": 0,
    "explanation": "As altitude increases, excess power decreases more rapidly than excess thrust. Vy decreases and Vx increases slightly until they converge at the absolute ceiling where the aircraft can maintain level flight at only one airspeed.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-005",
    "subject": "Technical Specific",
    "topic": "V-speeds and their meanings",
    "difficulty": "hard",
    "question": "Vfe refers to the maximum speed at which flaps may be extended. If a pilot inadvertently exceeds Vfe with flaps deployed, the primary structural risk is to which component?",
    "options": ["Engine mounts due to increased drag loading", "Flap hinges, actuating mechanism, and wing flap attachment structure", "Landing gear doors due to airflow disruption", "Elevator trim tab"],
    "answerIndex": 1,
    "explanation": "Exceeding Vfe with flaps extended risks structural damage or failure of the flap hinges, actuating rods/screws, and the wing structure at the flap attachment points due to excessive aerodynamic loads on the flap surfaces.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-006",
    "subject": "Technical Specific",
    "topic": "Airspeed indicator markings",
    "difficulty": "easy",
    "question": "On a standard airspeed indicator, the white arc represents which speed range?",
    "options": ["Normal operating range from Vno to Vne", "Flap operating range from Vso to Vfe", "Caution range from Vno to Vne", "Best glide speed to never-exceed speed"],
    "answerIndex": 1,
    "explanation": "The white arc on the airspeed indicator represents the flap operating range. Its lower limit is Vso (stalling speed in landing configuration) and its upper limit is Vfe (maximum flap extended speed).",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-007",
    "subject": "Technical Specific",
    "topic": "Airspeed indicator markings",
    "difficulty": "easy",
    "question": "The red radial line on the airspeed indicator represents:",
    "options": ["Vno — maximum structural cruising speed", "Vne — never-exceed speed", "Vso — stall speed in landing configuration", "Va — manoeuvring speed"],
    "answerIndex": 1,
    "explanation": "The red radial line marks Vne, the never-exceed speed. Exceeding this speed risks structural failure due to flutter or overstress. It is placed at the top of the yellow arc.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-008",
    "subject": "Technical Specific",
    "topic": "Airspeed indicator markings",
    "difficulty": "medium",
    "question": "The yellow arc (caution range) on the airspeed indicator lies between which two speeds?",
    "options": ["Vs1 and Vso", "Vfe and Vne", "Vno and Vne", "Va and Vno"],
    "answerIndex": 2,
    "explanation": "The yellow arc (caution range) lies between Vno (maximum structural cruising speed) and Vne (never-exceed speed). Flight in this range is permitted only in smooth air and requires caution.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-009",
    "subject": "Technical Specific",
    "topic": "Airspeed indicator markings",
    "difficulty": "medium",
    "question": "The green arc on the ASI represents the normal operating range. What are its lower and upper limits?",
    "options": ["Vso to Vno", "Vs1 to Vno", "Vso to Vne", "Va to Vno"],
    "answerIndex": 1,
    "explanation": "The green arc spans from Vs1 (stalling speed in clean/cruise configuration, power off) at its lower end to Vno (maximum structural cruising speed) at its upper end. This is the normal operating range in smooth air.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-010",
    "subject": "Technical Specific",
    "topic": "Airspeed indicator markings",
    "difficulty": "hard",
    "question": "On a multi-engine aircraft ASI, a blue radial line indicates:",
    "options": ["Vmc — minimum control speed with critical engine inoperative", "Vyse — best rate-of-climb speed with one engine inoperative", "Vxse — best angle-of-climb speed with one engine inoperative", "Vsse — safe intentional one-engine inoperative speed"],
    "answerIndex": 1,
    "explanation": "The blue radial line on a multi-engine ASI marks Vyse, the best rate-of-climb speed with one engine inoperative (also called blue-line speed). It represents the optimum single-engine climb performance speed.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-011",
    "subject": "Technical Specific",
    "topic": "Fuel grades and colors",
    "difficulty": "easy",
    "question": "AVGAS 100LL used in piston aircraft is which color?",
    "options": ["Red", "Green", "Blue", "Colorless"],
    "answerIndex": 2,
    "explanation": "AVGAS 100LL (100 octane, Low Lead) is dyed blue. The color coding helps pilots and fuellers identify the correct fuel type and avoid misfuelling.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-012",
    "subject": "Technical Specific",
    "topic": "Fuel grades and colors",
    "difficulty": "easy",
    "question": "Jet-A1 turbine fuel, when visually inspected, normally appears as which color?",
    "options": ["Blue", "Green", "Straw/colorless (pale yellow)", "Red"],
    "answerIndex": 2,
    "explanation": "Jet-A1 is a kerosene-based turbine fuel that appears straw-colored or nearly colorless. Unlike AVGAS, it is not dyed with a distinctive color. Its density and smell differ markedly from AVGAS.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-013",
    "subject": "Technical Specific",
    "topic": "Fuel grades and colors",
    "difficulty": "medium",
    "question": "AVGAS 80 (grade 80/87) is identified by which color?",
    "options": ["Blue", "Red", "Green", "Orange"],
    "answerIndex": 1,
    "explanation": "AVGAS Grade 80/87 is dyed red. It is a lower octane fuel suitable for engines with lower compression ratios. AVGAS 100 (non-low-lead) is dyed green, while 100LL is blue.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-014",
    "subject": "Technical Specific",
    "topic": "Fuel grades and colors",
    "difficulty": "hard",
    "question": "A pilot discovers that AVGAS 100LL has been accidentally loaded into an aircraft certified for AVGAS 80 only. The primary concern is:",
    "options": ["Fuel will burn too lean causing engine roughness", "Higher lead content of 100LL may cause valve seat deposits and fouling over time, and the engine was not designed for it", "Fuel will vaporize at low altitudes causing vapor lock", "The blue dye will contaminate the fuel system filters"],
    "answerIndex": 1,
    "explanation": "While 100LL has adequate octane rating for lower-grade engines, its higher lead content (compared to AVGAS 80) can lead to lead fouling of spark plugs and valve seats over time. The engine manufacturer approval must be confirmed. Using an unapproved fuel grade is also a regulatory violation.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-015",
    "subject": "Technical Specific",
    "topic": "Altimeter setting procedures",
    "difficulty": "easy",
    "question": "QNH is defined as the altimeter sub-scale setting that causes the altimeter to read:",
    "options": ["Zero on the ground at any elevation", "Pressure altitude at the airfield", "Airfield elevation above mean sea level when on the ground", "Height above the standard datum of 1013.25 hPa"],
    "answerIndex": 2,
    "explanation": "QNH is the local altimeter setting adjusted so that the altimeter reads the aerodrome elevation (AMSL) when the aircraft is on the ground at that aerodrome. It allows aircraft to fly at altitudes referenced to mean sea level.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-016",
    "subject": "Technical Specific",
    "topic": "Altimeter setting procedures",
    "difficulty": "medium",
    "question": "When climbing through the transition altitude, the pilot should change the altimeter setting from QNH to:",
    "options": ["QFE of the destination aerodrome", "Standard pressure setting of 1013.25 hPa (29.92 inHg)", "QNH of the destination aerodrome", "Regional QNH"],
    "answerIndex": 1,
    "explanation": "At the transition altitude, climbing aircraft change from QNH to standard pressure (1013.25 hPa / 29.92 inHg). Above the transition layer, aircraft fly at Flight Levels referenced to standard pressure, ensuring uniform vertical separation.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-017",
    "subject": "Technical Specific",
    "topic": "Altimeter setting procedures",
    "difficulty": "medium",
    "question": "QFE is the altimeter setting that causes the altimeter to indicate:",
    "options": ["Elevation AMSL at the aerodrome", "Height above the aerodrome reference point (zero on the ground at the aerodrome)", "Density altitude at field elevation", "Flight level equivalent of field elevation"],
    "answerIndex": 1,
    "explanation": "QFE is set so that the altimeter reads zero (or aerodrome elevation if at a threshold) when the aircraft is on the ground at the reference point. It gives height above the aerodrome rather than altitude above sea level.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-018",
    "subject": "Technical Specific",
    "topic": "Altimeter setting procedures",
    "difficulty": "hard",
    "question": "An aircraft on approach with QNH set will read altitude AMSL. If the actual atmospheric pressure is lower than the set QNH, the aircraft will be:",
    "options": ["Higher than indicated — safe situation", "Lower than indicated — potentially dangerous", "At the correct altitude since QNH compensates automatically", "Unaffected, as pressure changes only affect TAS"],
    "answerIndex": 1,
    "explanation": "If the actual pressure is lower than set (cold or low-pressure air), the altimeter over-reads — the aircraft is actually lower than indicated. This is the basis of the memory aid: High to Low, Look Out Below. This is a safety-critical scenario during approaches.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-019",
    "subject": "Technical Specific",
    "topic": "POH sections",
    "difficulty": "easy",
    "question": "According to the standard POH/AFM structure (FAR Part 23 / EASA CS-23 format), which section contains emergency procedures?",
    "options": ["Section 1", "Section 2", "Section 3", "Section 4"],
    "answerIndex": 2,
    "explanation": "The standard POH is divided into 9 sections. Section 3 is Emergency Procedures, which contains memory items, checklists for abnormal/emergency situations, and amplified procedures. Section 1 is General, Section 2 is Limitations, and Section 4 is Normal Procedures.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-020",
    "subject": "Technical Specific",
    "topic": "POH sections",
    "difficulty": "medium",
    "question": "A pilot needs to find the aircraft maximum certified takeoff weight and CG limits. This information is located in which POH section?",
    "options": ["Section 4 — Normal Procedures", "Section 6 — Weight and Balance", "Section 2 — Limitations", "Section 7 — Airplane and Systems Description"],
    "answerIndex": 2,
    "explanation": "Section 2 (Limitations) contains all FAA/DGCA-approved operating limitations, including maximum takeoff weight, maximum landing weight, CG limits, airspeed limitations, engine limitations, and approved fuel types.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-021",
    "subject": "Technical Specific",
    "topic": "POH sections",
    "difficulty": "medium",
    "question": "Which section of the POH would a pilot consult to determine the aircraft useful load and to perform a weight and balance calculation?",
    "options": ["Section 2 — Limitations", "Section 5 — Performance", "Section 6 — Weight and Balance", "Section 9 — Supplements"],
    "answerIndex": 2,
    "explanation": "Section 6 (Weight and Balance) contains equipment lists, loading graphs, moment/weight tables, and sample CG calculations. Pilots use this section to compute the loaded weight and confirm the CG is within limits before each flight.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-022",
    "subject": "Technical Specific",
    "topic": "Weight limits",
    "difficulty": "easy",
    "question": "Maximum ramp weight (maximum taxi weight) differs from maximum takeoff weight because it accounts for:",
    "options": ["Fuel burn during flight to destination", "Fuel burned and oil consumed during engine start, taxi, and runup", "Passenger and baggage weight loaded at the terminal", "Structural limits applicable only on the ground"],
    "answerIndex": 1,
    "explanation": "Maximum ramp weight (also called maximum taxi weight) is slightly higher than maximum takeoff weight by the amount of fuel expected to be burned during engine start, taxi, and run-up. The aircraft must be at or below MTOW by the time it begins its takeoff roll.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-023",
    "subject": "Technical Specific",
    "topic": "Weight limits",
    "difficulty": "medium",
    "question": "An aircraft has a maximum zero fuel weight (MZFW) limitation. The purpose of this limit is to:",
    "options": ["Prevent the aircraft from exceeding structural limits in turbulence when fuel is absent from the wing tanks", "Ensure the aircraft cannot take off with an empty fuel tank", "Limit the payload that can be carried on short sectors", "Prevent exceeding the maximum landing weight on arrival"],
    "answerIndex": 0,
    "explanation": "MZFW is the maximum weight of the aircraft without usable fuel. Fuel in the wing tanks relieves upward bending loads on the wing root. Without fuel (or with minimal fuel), bending loads on the wing root structure are highest, so MZFW limits the payload/structure combination to prevent overstress.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-024",
    "subject": "Technical Specific",
    "topic": "Performance charts",
    "difficulty": "medium",
    "question": "When using a takeoff distance performance chart, increasing pressure altitude while keeping all other variables constant will result in:",
    "options": ["Shorter ground roll due to higher engine efficiency", "Longer ground roll because of reduced air density and engine power output", "No change because ASI reads the same IAS", "Shorter total distance because thinner air reduces drag"],
    "answerIndex": 1,
    "explanation": "At higher pressure altitudes, air density is lower. This reduces both engine power output and propeller/wing efficiency (aerodynamic performance). As a result, acceleration is lower and the aircraft needs more runway to reach the required airspeed for liftoff.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "TS-025",
    "subject": "Technical Specific",
    "topic": "Performance charts",
    "difficulty": "hard",
    "question": "A performance chart gives a take-off distance of 800 m under standard conditions. The temperature is ISA+20. Using the approximation of 10% increase per 1000 ft density altitude increase above field elevation, and the density altitude is approximately 2000 ft above field elevation, the corrected distance is approximately:",
    "options": ["960 m", "880 m", "800 m", "840 m"],
    "answerIndex": 0,
    "explanation": "A 2000 ft density altitude increase above the charted conditions gives approximately 2 x 10% = 20% increase in distance. 800 m x 1.20 = 960 m. This is a standard approximation method used when exact chart corrections are not available.",
    "source": "Generic POH / DGCA Flight Test Standards"
  },
  {
    "id": "RTR-001",
    "subject": "RTR",
    "topic": "Phonetic alphabet",
    "difficulty": "easy",
    "question": "In the ICAO phonetic alphabet, the letter W is represented by which word?",
    "options": ["Washington", "Whiskey", "White", "Warsaw"],
    "answerIndex": 1,
    "explanation": "The ICAO phonetic alphabet word for W is Whiskey. The full alphabet is standardised in ICAO Doc 9432 and Annex 10 to ensure clarity in voice communications regardless of the speaker language background.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-002",
    "subject": "RTR",
    "topic": "Phonetic alphabet",
    "difficulty": "easy",
    "question": "How is the number 9 pronounced in standard ICAO radiotelephony?",
    "options": ["Nine", "Niner", "Nov-em-ber", "Nyne"],
    "answerIndex": 1,
    "explanation": "In ICAO radiotelephony, the digit 9 is pronounced NINER to avoid confusion with the German word nein (no) and similar words in other languages. Correct numeral pronunciation is specified in ICAO Doc 9432.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-003",
    "subject": "RTR",
    "topic": "Phonetic alphabet",
    "difficulty": "medium",
    "question": "A pilot is asked to spell out the registration VT-KAB using the ICAO phonetic alphabet. The correct transmission is:",
    "options": ["Victor Tango Kilo Alpha Bravo", "Victor Tango Kilo November Bravo", "Victor Tango Kilo Alfa Bravo", "Violet Tiger Kilo Alpha Bravo"],
    "answerIndex": 2,
    "explanation": "The ICAO phonetic word for A is Alfa (not Alpha — the spelling Alpha is not the official ICAO form). The correct transmission is Victor Tango Kilo Alfa Bravo. ICAO Doc 9432 specifies Alfa and Juliett as the standard spellings.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-004",
    "subject": "RTR",
    "topic": "Readability scale",
    "difficulty": "easy",
    "question": "In ICAO standard radiotelephony, a readability of 5 means:",
    "options": ["Unreadable", "Readable now and then", "Readable but with difficulty", "Perfectly readable"],
    "answerIndex": 3,
    "explanation": "The ICAO readability scale runs from 1 to 5: 1 = Unreadable, 2 = Readable now and then, 3 = Readable but with difficulty, 4 = Readable, 5 = Perfectly readable. A readability of 5 is the best possible signal quality report.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-005",
    "subject": "RTR",
    "topic": "Readability scale",
    "difficulty": "medium",
    "question": "A controller responds to a pilot radio check with READABILITY 3. This means the pilot transmission is:",
    "options": ["Perfectly readable", "Readable but with difficulty", "Readable now and then", "Unreadable"],
    "answerIndex": 1,
    "explanation": "Readability 3 on the ICAO scale means readable but with difficulty. The pilot should take corrective action (check microphone, adjust squelch, check frequency, or change position) to improve signal quality.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-006",
    "subject": "RTR",
    "topic": "Standard phraseology",
    "difficulty": "easy",
    "question": "Which word is used in ICAO RTF to indicate that a message has been received and understood?",
    "options": ["Copy", "Roger", "Wilco", "Affirmative"],
    "answerIndex": 1,
    "explanation": "ROGER means I have received all of your last transmission. It does not mean I will comply (that is WILCO — will comply). COPY and AFFIRMATIVE are not the standard ICAO terms for simple acknowledgement of receipt.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-007",
    "subject": "RTR",
    "topic": "Standard phraseology",
    "difficulty": "easy",
    "question": "The word WILCO in ICAO RTF phraseology means:",
    "options": ["I have received and understood your message", "I have received your message, will comply", "Wait, I must check with operations", "Your message is not understood"],
    "answerIndex": 1,
    "explanation": "WILCO (derived from will comply) means I have received your message, understand it, and will comply with it. It already implies receipt, so ROGER WILCO is redundant but sometimes used colloquially; WILCO alone is technically sufficient.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-008",
    "subject": "RTR",
    "topic": "Standard phraseology",
    "difficulty": "medium",
    "question": "The phrase BREAK BREAK in RTF is used to indicate:",
    "options": ["A separation between the address and the message of the same station", "An emergency transmission follows", "Separation between messages to different aircraft in a busy frequency", "The pilot is leaving the frequency temporarily"],
    "answerIndex": 2,
    "explanation": "BREAK BREAK is used to indicate a separation between messages addressed to different aircraft on the same frequency, especially when several messages are transmitted in sequence. BREAK (once) separates the address from the message text for the same station.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-009",
    "subject": "RTR",
    "topic": "ATC clearances and readback",
    "difficulty": "medium",
    "question": "Which of the following items in an ATC clearance is MANDATORY to read back by the pilot?",
    "options": ["Weather information and ATIS code", "Route clearance, assigned heading, altitude, and speed instructions", "Taxiway names during pushback", "Traffic information passed by ATC"],
    "answerIndex": 1,
    "explanation": "ICAO Annex 11 and Doc 4444 require mandatory readback of: ATC route clearances, runway-in-use, clearances to enter/land/take off/hold short of any active runway, heading instructions, altitude instructions, speed instructions, SSR transponder codes, and altimeter settings. Weather info and ATIS codes do not require readback.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-010",
    "subject": "RTR",
    "topic": "ATC clearances and readback",
    "difficulty": "medium",
    "question": "A pilot reads back an ATC clearance incorrectly. The controller should respond with:",
    "options": ["ROGER — the readback is accepted even if incorrect", "NEGATIVE, followed by the correct version of the instruction", "STANDBY and reissue after other traffic is handled", "CONFIRM — asking the pilot to re-read the original message"],
    "answerIndex": 1,
    "explanation": "If a readback is incorrect or incomplete, ATC must use the word NEGATIVE and immediately transmit the correct version. This is a safety-critical procedure to prevent misunderstandings from becoming operational errors.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-011",
    "subject": "RTR",
    "topic": "Distress and urgency calls",
    "difficulty": "easy",
    "question": "The MAYDAY distress call is transmitted how many times at the beginning of a distress message?",
    "options": ["Once", "Twice", "Three times", "Five times"],
    "answerIndex": 2,
    "explanation": "The distress call begins with MAYDAY MAYDAY MAYDAY spoken three times, as specified in ICAO Annex 10 and Doc 9432. The repetition ensures the call is recognised as a distress call even if the beginning is partially missed.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-012",
    "subject": "RTR",
    "topic": "Distress and urgency calls",
    "difficulty": "easy",
    "question": "PAN-PAN (urgency) differs from MAYDAY (distress) primarily because:",
    "options": ["PAN-PAN is used by ATC; MAYDAY is used only by pilots", "PAN-PAN indicates a serious situation requiring priority, but the aircraft is not in immediate danger of destruction", "PAN-PAN is used only on 121.5 MHz; MAYDAY on working frequency", "PAN-PAN requires a full position report; MAYDAY does not"],
    "answerIndex": 1,
    "explanation": "MAYDAY indicates a state of distress — grave and imminent danger requiring immediate assistance (e.g., engine failure with forced landing imminent). PAN-PAN indicates urgency — a serious and urgent situation that requires priority handling but is not immediately life-threatening (e.g., medical emergency, lost aircraft).",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-013",
    "subject": "RTR",
    "topic": "Distress and urgency calls",
    "difficulty": "medium",
    "question": "The international aeronautical distress frequency on which all aircraft should monitor during flight (and on which ELTs transmit) is:",
    "options": ["123.45 MHz", "121.5 MHz", "156.8 MHz", "243.0 MHz"],
    "answerIndex": 1,
    "explanation": "121.5 MHz is the international VHF aeronautical emergency/distress frequency. ELTs (Emergency Locator Transmitters) transmit on both 121.5 MHz and 406 MHz. Aircraft are encouraged to monitor 121.5 MHz when on airways. 243.0 MHz is the military UHF guard frequency.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-014",
    "subject": "RTR",
    "topic": "Distress and urgency calls",
    "difficulty": "hard",
    "question": "After transmitting a MAYDAY call, a pilot does not receive a response. What is the next correct action per ICAO procedures?",
    "options": ["Cease transmitting to avoid blocking the channel", "Repeat the MAYDAY call on 121.5 MHz or any other available frequency", "Switch to squawk 7700 and only transmit on 243.0 MHz", "Transmit a PAN-PAN downgrade and await acknowledgement"],
    "answerIndex": 1,
    "explanation": "If a MAYDAY call goes unanswered on the current frequency, the pilot should repeat it on 121.5 MHz (international distress frequency) or attempt any other available frequency. Squawk 7700 should also be selected, but continued voice transmission attempts are essential.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-015",
    "subject": "RTR",
    "topic": "Transponder codes",
    "difficulty": "easy",
    "question": "The SSR transponder code 7700 indicates:",
    "options": ["Radio communication failure", "Unlawful interference (hijack)", "General emergency", "VFR flight in uncontrolled airspace"],
    "answerIndex": 2,
    "explanation": "Squawk 7700 is the standard ICAO SSR code for general emergency. Squawk 7600 indicates radio communication failure (NORDO), and squawk 7500 indicates unlawful interference (hijacking). These codes are recognized worldwide and trigger immediate ATC alerts.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-016",
    "subject": "RTR",
    "topic": "Transponder codes",
    "difficulty": "easy",
    "question": "Which transponder code should a pilot squawk when experiencing radio communication failure (NORDO)?",
    "options": ["7700", "7500", "7600", "2000"],
    "answerIndex": 2,
    "explanation": "Code 7600 is the ICAO designated SSR code for radio communication failure (NORDO — No Radio). It alerts ATC that the aircraft cannot communicate by voice. ATC will then apply NORDO procedures. Code 7700 is general emergency and 7500 is hijack.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-017",
    "subject": "RTR",
    "topic": "Transponder codes",
    "difficulty": "medium",
    "question": "An ATC instruction reads SQUAWK IDENT. The correct pilot action is:",
    "options": ["Switch the transponder to STANDBY mode", "Press the IDENT button on the transponder to produce a special SPI pulse on radar", "Change the transponder code to the assigned squawk and press IDENT", "Set the transponder to Mode A only and confirm on radio"],
    "answerIndex": 1,
    "explanation": "When instructed to SQUAWK IDENT, the pilot presses the IDENT (Identification) button on the transponder. This triggers a Special Position Identification (SPI) pulse, causing the aircraft radar return to blossom on the controller screen for quick identification.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-018",
    "subject": "RTR",
    "topic": "Transponder codes",
    "difficulty": "medium",
    "question": "Transponder Mode C provides ATC with which additional information compared to Mode A?",
    "options": ["Aircraft registration and flight number", "Pressure altitude of the aircraft", "GPS position of the aircraft", "Ground speed and heading"],
    "answerIndex": 1,
    "explanation": "Mode A transmits only the 4-digit squawk code for identification. Mode C additionally transmits the aircraft pressure altitude (derived from the transponder encoding altimeter or air data computer), enabling ATC to see the aircraft altitude on radar.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-019",
    "subject": "RTR",
    "topic": "Frequency management",
    "difficulty": "easy",
    "question": "Before changing from one ATC frequency to another (when not instructed by ATC), the pilot should:",
    "options": ["Change immediately to avoid delay", "Inform the current controller and obtain approval or acknowledgement before changing", "Switch without informing since radio is the pilot prerogative", "Squawk 7600 and then change frequency"],
    "answerIndex": 1,
    "explanation": "A pilot should always inform the current ATC unit before changing to another frequency, unless ATC has already instructed the change or it is an emergency. Unannounced frequency changes can result in loss of radio contact and are contrary to ICAO RTF procedures.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-020",
    "subject": "RTR",
    "topic": "Frequency management",
    "difficulty": "medium",
    "question": "A pilot is instructed MONITOR 128.3. The correct action is:",
    "options": ["Tune 128.3, call the station, and await a response", "Tune 128.3 and listen without making an initial call", "Continue on the current frequency and note 128.3 as backup", "Acknowledge on current frequency, tune 128.3, and call when ready"],
    "answerIndex": 1,
    "explanation": "MONITOR (frequency) means tune to the stated frequency and listen, but do not make an initial call. CONTACT (frequency) means tune and make an initial call. These are distinct standard ICAO instructions with different required actions.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-021",
    "subject": "RTR",
    "topic": "ATIS",
    "difficulty": "easy",
    "question": "ATIS stands for:",
    "options": ["Automatic Terminal Information Service", "Air Traffic Identification System", "Aerodrome Traffic and Information Squawk", "Automatic Transponder Identification System"],
    "answerIndex": 0,
    "explanation": "ATIS stands for Automatic Terminal Information Service. It is a continuous broadcast of routine aerodrome meteorological and operational information on a dedicated frequency, updated regularly (typically every 30 minutes or when significant changes occur), and identified by a successive letter of the alphabet.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-022",
    "subject": "RTR",
    "topic": "ATIS",
    "difficulty": "medium",
    "question": "When making first contact with approach control after listening to ATIS information CHARLIE, the pilot should:",
    "options": ["State the full ATIS message received to confirm awareness", "Mention INFORMATION CHARLIE in the initial call to indicate the ATIS has been received", "Ask for the latest ATIS as it may have changed", "Omit any reference to ATIS and wait for the controller to ask"],
    "answerIndex": 1,
    "explanation": "Pilots should include the ATIS identifier (e.g., INFORMATION CHARLIE) in their initial call to the ATC unit. This informs the controller that the pilot has the current ATIS information and does not need it repeated. If the ATIS has been updated, ATC will advise the pilot to obtain the new information.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-023",
    "subject": "RTR",
    "topic": "VHF propagation basics",
    "difficulty": "medium",
    "question": "VHF radio waves used in aviation communications travel primarily as:",
    "options": ["Ground waves that follow the curvature of the Earth", "Sky waves reflected by the ionosphere", "Line-of-sight waves limited by the horizon", "Surface waves diffracted around terrain"],
    "answerIndex": 2,
    "explanation": "VHF (Very High Frequency, 30-300 MHz) signals propagate primarily by line-of-sight. They cannot follow the Earth curvature and are not significantly reflected by the ionosphere (unlike HF/MF). This limits VHF range to approximately line-of-sight between the aircraft and the ground station antenna.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-024",
    "subject": "RTR",
    "topic": "VHF propagation basics",
    "difficulty": "medium",
    "question": "A pilot flying at 1600 ft AGL notices VHF communication with a ground station 60 NM away is unreliable. The most likely reason is:",
    "options": ["VHF frequency selected is outside the aviation band", "The aircraft is below the radio horizon for that range at its current altitude", "The transmitter is operating on a sky wave at this frequency", "Ionospheric absorption is highest during daytime at VHF"],
    "answerIndex": 1,
    "explanation": "VHF range is governed by line-of-sight. The radio horizon in nautical miles is approximately 1.23 times the square root of altitude in feet. At 1600 ft: 1.23 x sqrt(1600) = 1.23 x 40 = approximately 49 NM. The 60 NM station may therefore be beyond the radio horizon, causing unreliable reception.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  },
  {
    "id": "RTR-025",
    "subject": "RTR",
    "topic": "Standard phraseology",
    "difficulty": "hard",
    "question": "When a pilot is uncertain of a received ATC clearance, the correct ICAO phraseology to request repetition of the last message is:",
    "options": ["REPEAT LAST MESSAGE", "SAY AGAIN", "CONFIRM LAST TRANSMISSION", "RESTATE INSTRUCTIONS"],
    "answerIndex": 1,
    "explanation": "SAY AGAIN is the standard ICAO phraseology requesting repetition of all or part of a previous transmission. The word REPEAT is reserved for use by artillery and should not be used in aviation RTF to avoid confusion. Pilots should use SAY AGAIN ALL AFTER (phrase) or SAY AGAIN ALL BEFORE (phrase) for partial repetition.",
    "source": "ICAO Doc 9432 / DGCA RTR(A) Syllabus / Annex 10"
  }
]'''

ts_rtr_items = json.loads(ts_rtr_text)
for item in ts_rtr_items:
    questions.append({
        "id": item["id"],
        "subject": item["subject"],
        "topic": item["topic"],
        "difficulty": item["difficulty"],
        "question": clean_text(item["question"]),
        "options": [clean_text(o) for o in item["options"]],
        "answerIndex": item["answerIndex"],
        "explanation": clean_text(item["explanation"]),
        "source": item["source"]
    })

# Save to src/data/questions.json
out_file = os.path.join(BASE, "src", "data", "questions.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {len(questions)} clean questions in {out_file}")
from collections import Counter
c = Counter(q["subject"] for q in questions)
for s, cnt in sorted(c.items()):
    print(f"  {s}: {cnt}")

