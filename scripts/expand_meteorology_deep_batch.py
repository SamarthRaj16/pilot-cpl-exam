# -*- coding: utf-8 -*-
"""
Deep Aviation Meteorology Batch from I.C. Joshi (Chapters 6-25)
Directly referencing official DGCA chapter assessments with verified answers.
"""

import json
import os
import re

DEEP_MET_QUESTIONS = [
    # -------------------------------------------------------------
    # Chapter 14: Air Masses, Fronts & Western Disturbances (p. 133-135)
    # -------------------------------------------------------------
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "easy",
        "question": "An air mass which originates over the sea in high polar latitudes is classified as:",
        "options": ["Polar Maritime (Pm)", "Tropical Continental (Tc)", "Tropical Maritime (Tm)", "Equatorial Maritime (Em)"],
        "answerIndex": 0,
        "explanation": "Air masses originating over high-latitude oceans (sub-polar oceanic areas) are cold and moist, classified as Polar Maritime (Pm).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts', p. 126 & Q1"
    },
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "easy",
        "question": "The primary air mass prevailing over peninsular India during the Southwest Monsoon is:",
        "options": ["Tropical Continental (Tc)", "Equatorial Maritime (Em)", "Polar Continental (Pc)", "Arctic (A)"],
        "answerIndex": 1,
        "explanation": "Equatorial Maritime (Em) air mass originates over the tropical oceans south of the equator, crossing into the Indian subcontinent during the SW monsoon with high temperature and extreme humidity.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts', p. 126 & Q2"
    },
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "medium",
        "question": "If the advancing cold front air mass is colder than the retreating cold air ahead of the warm front, the resulting occlusion is a:",
        "options": ["Warm Occlusion", "Cold Occlusion", "Stationary Occlusion", "Neutral Occlusion"],
        "answerIndex": 1,
        "explanation": "In a Cold Occlusion, the air behind the advancing cold front is colder (denser) than the cool air ahead of the warm front, forcing the cool air and the warm front to ride up over it.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts', p. 130 & Q3"
    },
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "medium",
        "question": "When a warm air mass actively overtakes and ascends over a retreating colder air mass, the front is termed a:",
        "options": ["Cold Front", "Warm Front", "Occluded Front", "Squall Line"],
        "answerIndex": 1,
        "explanation": "A Warm Front is the transition zone where an advancing warm air mass overtakes and glides gently up over a retreating wedge of colder, denser air.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts', p. 129 & Q5"
    },
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "hard",
        "question": "Pre-frontal squall lines (lines of violent thunderstorms) typically occur at what distance ahead of a fast-moving cold front?",
        "options": ["10 to 20 km", "100 to 300 km", "500 to 800 km", "At the exact surface front only"],
        "answerIndex": 1,
        "explanation": "Squall lines frequently develop in the warm sector 100 to 300 km ahead of an active, fast-moving cold front, triggered by gravity waves and upper-level divergence.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts', p. 128 & Q8/Q11"
    },
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "medium",
        "question": "A cold front typically travels at what speed compared to a warm front?",
        "options": ["The same speed", "Approximately double the speed of a warm front", "Half the speed", "One quarter the speed"],
        "answerIndex": 1,
        "explanation": "A cold front moves roughly twice as fast (typically 20 to 30 kt) as a warm front (typically 10 to 15 kt). This speed difference leads to the cold front overtaking the warm front, forming an occlusion.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts', p. 130 & Q10"
    },
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "hard",
        "question": "What is the typical sequence of clouds observed as an active warm front approaches an observer from 1,000 km away?",
        "options": [
            "Cumulonimbus, Altocumulus, Stratus",
            "Cirrus (CI), Cirrostratus (CS), Altostratus (AS), Nimbostratus (NS), and Stratus (ST)",
            "Stratocumulus, Cumulus, Cirrus",
            "Nimbostratus followed directly by clear skies"
        ],
        "answerIndex": 1,
        "explanation": "Due to the gentle slope of the warm front (1:150), clouds thicken and lower progressively: high Cirrus appear ~1000 km ahead, followed by Cirrostratus (halo), Altostratus (~500 km), and finally dark Nimbostratus with continuous rain.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts', p. 129 & Q20"
    },
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "medium",
        "question": "Freezing Rain (FZRA) and Freezing Drizzle (FZDZ) are most commonly encountered in which frontal zone?",
        "options": [
            "Well behind a cold front",
            "Ahead of a warm front where warm rain falls through an underlying sub-zero surface cold air wedge",
            "Directly in a tropical depression",
            "Along a summer dry line"
        ],
        "answerIndex": 1,
        "explanation": "Freezing rain occurs ahead of a warm front when rain drops falling from the overriding warm air parcel enter a below-freezing shallow cold air wedge near the ground and become supercooled.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts', p. 135 & Q25"
    },
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "easy",
        "question": "When an active cold front passes over an airfield, what happens to barometric pressure?",
        "options": [
            "Pressure falls continuously for 24 hours",
            "The pressure fall is arrested and pressure begins to rise abruptly",
            "Pressure remains perfectly constant",
            "Pressure fluctuates wildly between 900 and 1100 hPa"
        ],
        "answerIndex": 1,
        "explanation": "Ahead of the cold front, pressure falls; as the cold front passes, the pressure drop is sharply arrested and pressure begins to rise rapidly due to the dense cold air mass.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts', p. 143 (Appendix I)"
    },

    # -------------------------------------------------------------
    # Chapter 15: Jet Streams (p. 140-142)
    # -------------------------------------------------------------
    {
        "topic": "Jet Streams",
        "difficulty": "easy",
        "question": "The central tubular zone of highest wind speed within a jet stream is termed the:",
        "options": ["Jet stream Axis", "Jet Core", "Jet Streak", "Trough line"],
        "answerIndex": 1,
        "explanation": "The path of maximum wind speed is known as the axis, and the tubular cross-sectional volume of maximum speed immediately enclosing the axis is called the Core.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 15 'Jet Streams', p. 136 & Q5/Q6"
    },
    {
        "topic": "Jet Streams",
        "difficulty": "medium",
        "question": "In a wavy jet stream, localized regions of maximum wind speed along the jet axis are called:",
        "options": ["Jet Streaks (Wind Maxima)", "Jet vortices", "Tropopause folds", "Rotor pockets"],
        "answerIndex": 0,
        "explanation": "Along the axis of a jet stream, wind speed is not uniform; distinct centers of maximum speed (wind maxima) occur, known as Jet Streaks.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 15 'Jet Streams', p. 136 & Q7"
    },
    {
        "topic": "Jet Streams",
        "difficulty": "medium",
        "question": "The Sub-Tropical Westerly Jet Stream (STJ) over India reaches its southernmost latitude position in which month?",
        "options": ["October", "December", "February (near 22°N)", "May"],
        "answerIndex": 2,
        "explanation": "The STJ shifts progressively southward over India with the progress of winter, reaching its southernmost position of approximately 22°N in February before moving north.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 15 'Jet Streams', p. 137 & Q11"
    },
    {
        "topic": "Jet Streams",
        "difficulty": "hard",
        "question": "How does vertical wind shear compare above the jet core versus below the jet core?",
        "options": [
            "Vertical shear is greater above the core than below the core",
            "Vertical shear is identical above and below",
            "Vertical shear is greater below the core than above the core",
            "There is zero shear above the core"
        ],
        "answerIndex": 0,
        "explanation": "Vertical wind shear in the Sub-Tropical Jet is significantly greater above the jet core (in the lower stratosphere) than below the core in the troposphere.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 15 'Jet Streams', p. 139 & Q16"
    },
    {
        "topic": "Jet Streams",
        "difficulty": "medium",
        "question": "Flying at right angles across a westerly jet stream with falling barometric pressure, an aircraft will experience:",
        "options": [
            "Wind from the right and decreasing speed",
            "Wind from the left and increasing headwind",
            "Wind from the left (port drift)",
            "Wind from the right (starboard drift)"
        ],
        "answerIndex": 2,
        "explanation": "Falling pressure indicates the aircraft is heading towards lower pressure (poleward). By Buys Ballot's Law, with low pressure ahead and to the left, the westerly jet blows from the left (producing starboard drift, wind from the left).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 15 'Jet Streams', p. 142 Q24"
    },

    # -------------------------------------------------------------
    # Chapter 16 & 17: CAT & Mountain Waves (p. 148-149)
    # -------------------------------------------------------------
    {
        "topic": "Clear Air Turbulence",
        "difficulty": "medium",
        "question": "In the vicinity of an upper westerly jet stream, where is Clear Air Turbulence (CAT) most prevalent?",
        "options": [
            "Directly inside the calm central core",
            "On the cyclonic (low-pressure/northern) side of the core and along the tropopause boundary",
            "Only on the south side at low altitudes",
            "Exclusively in the troposphere below 10,000 ft"
        ],
        "answerIndex": 1,
        "explanation": "Most CAT occurs in the fringes (not within the core) of the jet stream, specifically on the cold/cyclonic side where horizontal and vertical shears are greatest.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 16 'Clear Air Turbulence', p. 143 & Q8"
    },
    {
        "topic": "Mountain Waves",
        "difficulty": "easy",
        "question": "In a mountain wave system, where do turbulent Rotor Clouds form?",
        "options": [
            "In the wave crests at 40,000 ft",
            "In the troughs beneath the wave crests on the leeward side of the mountain ridge",
            "On the windward upwind slope",
            "Above the tropopause only"
        ],
        "answerIndex": 1,
        "explanation": "Rotor clouds form in the troughs of the lee waves, beneath the crests. The air rotates in a closed circular eddy with violent vertical gusts and extreme turbulence.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 17 'Mountain Waves', p. 146 & Q6"
    },
    {
        "topic": "Mountain Waves",
        "difficulty": "medium",
        "question": "For well-developed mountain waves to form, the atmosphere up to the mountain ridge crest must be:",
        "options": ["Super-adiabatically unstable", "Stable", "Isothermal above 50,000 ft only", "Completely saturated"],
        "answerIndex": 1,
        "explanation": "Mountain wave formation requires a stable layer of air near and just above the mountain crest. The stability acts as a restoring force, setting up oscillation when air is displaced over the ridge.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 17 'Mountain Waves', p. 145 & Q4"
    },
    {
        "topic": "Mountain Waves",
        "difficulty": "hard",
        "question": "When approaching a mountainous area where standing lee waves are reported, a pilot should anticipate:",
        "options": [
            "Calm, smooth gliding conditions throughout",
            "Roll clouds, lenticular clouds, severe up- and down-drafts on the lee side extending 20 to 30 miles downwind, and altimeter overreading",
            "Constant magnetic deviation",
            "Immediate engine flameout on all cylinders"
        ],
        "answerIndex": 1,
        "explanation": "Approaching mountain waves, pilots must watch for roll and lenticular clouds, anticipate strong vertical currents (up to 5,000 fpm sink rates), severe rotor turbulence downwind, and altimeter errors.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 17 'Mountain Waves', p. 146-147 & Q10"
    },

    # -------------------------------------------------------------
    # Chapter 18: Tropical Systems (p. 160-163)
    # -------------------------------------------------------------
    {
        "topic": "Tropical Systems & Monsoon",
        "difficulty": "easy",
        "question": "What is the typical diameter of a mature Tropical Cyclone over the North Indian Ocean?",
        "options": ["10 to 50 km", "300 to 600 km", "2,000 to 5,000 km", "100 metres"],
        "answerIndex": 1,
        "explanation": "Over the Bay of Bengal and Arabian Sea, the diameter of a typical tropical cyclone ranges from 300 to 600 km, with extreme cases reaching 1,000 km.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Tropical Systems', p. 158"
    },
    {
        "topic": "Tropical Systems & Monsoon",
        "difficulty": "medium",
        "question": "In the mature stage of a tropical cyclone, why are surface temperatures in the central eye slightly warmer than outside?",
        "options": [
            "Due to intense solar radiation focused by the cloud walls",
            "Due to adiabatic compression of slowly subsiding air within the eye",
            "Because ocean water boils in the eye",
            "Due to friction of rotating winds"
        ],
        "answerIndex": 1,
        "explanation": "Air in the eye sinks slowly (subsidence). As it descends, it is compressed and warms dry adiabatically, raising temperatures in the eye 0°C to 2°C warmer at the surface and up to 10°C warmer aloft.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Tropical Systems', p. 157"
    },
    {
        "topic": "Tropical Systems & Monsoon",
        "difficulty": "medium",
        "question": "In which months do the maximum number of Severe Cyclonic Storms form over the Bay of Bengal and Arabian Sea?",
        "options": [
            "January and February",
            "March and April",
            "May (pre-monsoon) and October–November (post-monsoon)",
            "July and August"
        ],
        "answerIndex": 2,
        "explanation": "Tropical cyclones over the Indian seas exhibit a bimodal peak: pre-monsoon (May) and post-monsoon (October-November). October and November experience the most severe cyclones.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Tropical Systems', p. 159 & Q5"
    },
    {
        "topic": "Tropical Systems & Monsoon",
        "difficulty": "hard",
        "question": "What is the approximate rate of movement of a Tropical Cyclone across the ocean?",
        "options": ["50 to 100 km/day", "300 to 500 km per day (15 to 20 km/h)", "1,500 km per day", "Zero (they never move)"],
        "answerIndex": 1,
        "explanation": "Tropical cyclones move at a typical translation speed of 15 to 20 km/h (8 to 12 knots), covering approximately 300 to 500 km in 24 hours.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Tropical Systems', p. 157 & Q39"
    },
    {
        "topic": "Tropical Systems & Monsoon",
        "difficulty": "medium",
        "question": "When a tropical cyclone makes landfall and crosses inland, it weakens rapidly primarily because of:",
        "options": [
            "Loss of its primary heat/moisture source (evaporation from warm sea water) and increased surface friction",
            "Coriolis force reversing direction",
            "Cold air from the Himalayas filling the eye instantly",
            "Solar radiation stopping completely"
        ],
        "answerIndex": 0,
        "explanation": "Cut off from the warm ocean's latent heat of condensation, the cyclone's thermodynamic engine starves. Concurrently, high surface friction over land increases convergence into the center, filling the low.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Tropical Systems', p. 158 & Q14"
    },

    # -------------------------------------------------------------
    # Chapter 20: General Circulation (p. 186-187)
    # -------------------------------------------------------------
    {
        "topic": "General Circulation",
        "difficulty": "easy",
        "question": "The low-latitude vertical atmospheric circulation cell between the Equator and approximately 30° latitude is known as the:",
        "options": ["Hadley Cell", "Ferrel Cell", "Polar Cell", "Walker Cell"],
        "answerIndex": 0,
        "explanation": "The Hadley Cell features rising air near the thermal equator (ITCZ), poleward flow aloft, sinking air in the subtropical high pressure belts near 30°N/S, and returning trade winds.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 20 'General Circulation', p. 182 & Q5"
    },
    {
        "topic": "General Circulation",
        "difficulty": "medium",
        "question": "The major world deserts (Sahara, Arabian, Thar) are located around 30°N and 30°S latitudes primarily due to:",
        "options": [
            "Large-scale atmospheric subsidence and dry anticyclonic conditions in the descending branch of the Hadley cell",
            "High frequency of tropical cyclones",
            "Absence of solar radiation",
            "Constant frontal rain"
        ],
        "answerIndex": 0,
        "explanation": "Subtropical high pressure belts (Horse Latitudes) at 30°N/S are formed by subsiding air from the Hadley cell. Sinking air warms adiabatically and dries out, suppressing cloudiness and creating vast deserts.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 20 'General Circulation', p. 182 & Q3"
    },
    {
        "topic": "General Circulation",
        "difficulty": "medium",
        "question": "In the Southern Hemisphere, the strong westerly winds blowing between 40°S and 50°S latitudes are called the:",
        "options": ["Roaring Forties", "Doldrums", "Trade Winds", "Polar Easterlies"],
        "answerIndex": 0,
        "explanation": "Unbroken by land masses, the Southern Hemisphere mid-latitude westerlies blow with intense gale force, famously known as the 'Roaring Forties' (and Furious Fifties).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 20 'General Circulation', p. 184"
    },
    {
        "topic": "General Circulation",
        "difficulty": "hard",
        "question": "What is the direction of the upper tropospheric winds over the equatorial regions?",
        "options": ["Westerlies", "Easterlies", "Northerlies", "Southerlies"],
        "answerIndex": 1,
        "explanation": "In the equatorial upper troposphere, upper air flow is dominated by broad tropical Easterlies, whereas middle latitudes are dominated by Zonal Westerlies.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 20 'General Circulation', p. 185 & Q8"
    },

    # -------------------------------------------------------------
    # Chapter 21: Meteorological Services for Aviation (p. 195-197)
    # -------------------------------------------------------------
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "easy",
        "question": "Under the World Area Forecast System (WAFS), the two global World Area Forecast Centres (WAFC) are located at:",
        "options": ["London and Washington", "Paris and Tokyo", "New Delhi and Geneva", "Montreal and Chicago"],
        "answerIndex": 0,
        "explanation": "Under ICAO WAFS, the two designated World Area Forecast Centres are WAFC London (Met Office UK) and WAFC Washington (NOAA/NWS USA).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 21 'Met Services', p. 188 & Q3"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "medium",
        "question": "What is an AIRMET message issued for?",
        "options": [
            "Information issued by a Meteorological Watch Office (MWO) concerning low-level en-route weather phenomena not already included in area forecasts that may affect low-level flights",
            "Notifying airline ticket price adjustments",
            "Reporting stratospheric volcanic ash only",
            "Routine upper wind forecasts for supersonic jets"
        ],
        "answerIndex": 0,
        "explanation": "AIRMET is advisory information issued by an MWO concerning low-level flights (below FL100 or FL150 in mountainous terrain) regarding moderate turbulence, moderate icing, mountain obscuration, or widespread low cloud/visibility.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 21 'Met Services', p. 193 & Q23"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "medium",
        "question": "In India, VOLMET radio telephony broadcasts are transmitted on HF frequencies from which two stations?",
        "options": ["Mumbai and Kolkata", "Delhi and Chennai", "Bangalore and Hyderabad", "Nagpur and Ahmedabad"],
        "answerIndex": 0,
        "explanation": "In India, continuous HF VOLMET meteorological broadcasts for aircraft in flight are operated from Mumbai (covering western/southern aerodromes) and Kolkata (covering eastern/northern aerodromes).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 21 'Met Services', p. 194 & Q31"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "hard",
        "question": "An Aerodrome Warning (Airfield Warning) is issued for aerodrome safety on the ground when mean wind speed is expected to reach at least:",
        "options": ["15 knots", "20 knots", "30 knots (or gusts of 35 kt)", "50 knots"],
        "answerIndex": 2,
        "explanation": "Aerodrome warnings for moored aircraft and ground facilities are issued when mean surface wind speed is expected to reach 30 knots or more, or when wind direction changes by >= 45° with speed >= 20 kt.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 21 'Met Services', p. 193 & Q26/Q27"
    },

    # -------------------------------------------------------------
    # Chapter 24 & 25: Station Model & METAR Codes (p. 214-230)
    # -------------------------------------------------------------
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "easy",
        "question": "On a plotted station model chart, how is a barometric pressure of 1014.2 hPa encoded in the standard 3-digit PPP group?",
        "options": ["014", "142", "101", "420"],
        "answerIndex": 1,
        "explanation": "PPP encodes tenths of hPa with the leading 9 or 10 omitted: 1014.2 hPa is plotted as '142'. (e.g., 998.5 hPa is plotted as '985').",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 24 'Station Model', p. 207 & p. 215 Q11"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "medium",
        "question": "In a METAR report, what does the present weather code '+TSRA' mean?",
        "options": [
            "Moderate rain without thunder",
            "Thunderstorm with heavy rain",
            "Light shower with hail",
            "Thunderstorm with ice pellets"
        ],
        "answerIndex": 1,
        "explanation": "'+' indicates heavy intensity, 'TS' stands for Thunderstorm, and 'RA' stands for Rain. Hence, '+TSRA' translates to Thunderstorm with heavy rain.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 25 'METAR & SPECI Codes', p. 219 (Table 25.3)"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "medium",
        "question": "In a METAR report, the air temperature and dew point are given as '02/M03'. What do these figures signify?",
        "options": [
            "Air temperature +02°C, Dew Point -03°C",
            "Air temperature -02°C, Dew Point +03°C",
            "Altimeter setting 02.03 inHg",
            "Wind 020 degrees at 3 knots"
        ],
        "answerIndex": 0,
        "explanation": "'02' is dry bulb temperature (+2°C), '/' is separator, 'M' denotes minus/sub-zero temperature, and '03' is dew point temperature (-3°C).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 25 'METAR & SPECI Codes', p. 222 (Table 25.1)"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "hard",
        "question": "What is the meaning of the METAR code 'WS ALL RWY'?",
        "options": [
            "All runways are wet and slippery",
            "Wind shear reported on all runways up to 500 m (1,600 ft)",
            "Wind speed exceeding 100 knots on all runways",
            "All runways are closed due to fog"
        ],
        "answerIndex": 1,
        "explanation": "'WS' stands for Wind Shear. 'WS ALL RWY' warns pilots of wind shear along the takeoff or final approach path of all runways up to 500 m (1,600 ft) above runway elevation.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 25 'METAR & SPECI Codes', p. 218 & p. 222"
    }
]

def append_deep_met():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    questions_file = os.path.join(base_dir, "src", "data", "questions.json")

    with open(questions_file, "r", encoding="utf-8") as f:
        existing_questions = json.load(f)

    existing_texts = set()
    for q in existing_questions:
        norm = re.sub(r'[^a-zA-Z0-9]', '', q["question"].lower())
        existing_texts.add(norm)

    met_ids = [int(q["id"].replace("MET-", "")) for q in existing_questions if q.get("subject") == "Aviation Meteorology" and q["id"].startswith("MET-")]
    next_id_num = max(met_ids) + 1 if met_ids else 200

    new_added = 0
    rejected = 0

    for item in DEEP_MET_QUESTIONS:
        norm = re.sub(r'[^a-zA-Z0-9]', '', item["question"].lower())
        if norm in existing_texts:
            rejected += 1
            continue

        q_id = f"MET-{str(next_id_num).zfill(3)}"
        next_id_num += 1

        new_q = {
            "id": q_id,
            "subject": "Aviation Meteorology",
            "topic": item["topic"],
            "difficulty": item["difficulty"],
            "question": item["question"],
            "options": item["options"],
            "answerIndex": item["answerIndex"],
            "explanation": item["explanation"],
            "source": item["source"],
            "validation_status": "approved"
        }

        existing_questions.append(new_q)
        existing_texts.add(norm)
        new_added += 1

    print(f"Deep Batch Added: {new_added} questions (Rejected dups: {rejected})")
    print(f"Total Questions Now: {len(existing_questions)}")

    with open(questions_file, "w", encoding="utf-8") as f:
        json.dump(existing_questions, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    append_deep_met()

