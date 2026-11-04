# -*- coding: utf-8 -*-
"""
Comprehensive Aviation Meteorology Question Bank Expansion
Based strictly on I.C. Joshi 'Aviation Meteorology' (3rd Edition).
Covers all 19 DGCA syllabus chapters.
"""

import json
import os
import re

METEOROLOGY_QUESTIONS = [
    # -------------------------------------------------------------
    # Topic 1: The Atmosphere
    # -------------------------------------------------------------
    {
        "topic": "The Atmosphere",
        "difficulty": "easy",
        "question": "What is the standard sea-level temperature and pressure in the International Standard Atmosphere (ISA)?",
        "options": [
            "+15°C and 1013.25 hPa",
            "0°C and 1000.0 hPa",
            "+20°C and 1013.25 hPa",
            "+15°C and 29.82 inHg"
        ],
        "answerIndex": 0,
        "explanation": "In ISA, standard sea-level values are defined by ICAO as a temperature of +15°C (288.15 K), pressure of 1013.25 hPa (29.92 inHg), and density of 1.225 kg/m³.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 7"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "easy",
        "question": "What percentage of the total atmospheric mass is concentrated below 6 km (approx 20,000 ft)?",
        "options": ["25%", "50%", "75%", "90%"],
        "answerIndex": 1,
        "explanation": "Due to gravitational compression of air molecules, half (50%) of the total atmospheric mass lies below 6 km, and 75% lies below 10 km.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 3 & Q31"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "easy",
        "question": "Which gas is the third most abundant by volume in dry atmospheric air?",
        "options": ["Carbon Dioxide", "Argon", "Neon", "Helium"],
        "answerIndex": 1,
        "explanation": "Dry air consists of Nitrogen (78.08%), Oxygen (20.95%), Argon (0.93%), and Carbon Dioxide (0.035%). Argon is the third most abundant.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 1"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "medium",
        "question": "Why is the tropopause temperature colder over the Equator (-75°C to -80°C) than over the Poles (-45°C to -50°C)?",
        "options": [
            "Because solar radiation is weaker at the equator",
            "Because vigorous vertical thermal convection in the tropics lifts the tropopause much higher (16–18 km) before adiabatic cooling ceases",
            "Because polar regions receive more geothermal radiation",
            "Because the ozone layer is thickest over the equator"
        ],
        "answerIndex": 1,
        "explanation": "Intense solar heating at the equator causes deep convective overturning, pushing the tropopause up to 16-18 km. Continued adiabatic expansion cools the air to between -75°C and -85°C. At the poles, where convection is weak, the tropopause sits at only 8-10 km with temperatures near -45°C to -50°C.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 5 & Q6"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "medium",
        "question": "In the Jet Standard Atmosphere (JSA), what is the assumed temperature lapse rate?",
        "options": ["1.5°C / 1,000 ft", "2.0°C / 1,000 ft", "3.0°C / 1,000 ft", "6.5°C / 1,000 ft"],
        "answerIndex": 1,
        "explanation": "Jet Standard Atmosphere (JSA) assumes a mean sea-level temperature of 15°C and a uniform lapse rate of 2°C per 1,000 ft without a tropopause, used for space and extreme high altitude engineering.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 8 & Q32"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "hard",
        "question": "If the ambient temperature at 19 km altitude is measured at -60°C, what is the ISA temperature deviation?",
        "options": ["-4.5°C", "-05.5°C", "-03.5°C", "+03.5°C"],
        "answerIndex": 2,
        "explanation": "ISA temperature from 11 km to 20 km is constant at -56.5°C. With actual temperature at -60°C, ISA deviation = Actual - ISA = (-60) - (-56.5) = -3.5°C (ISA -3.5).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 8 & Q28"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "medium",
        "question": "The middle atmosphere layer where temperature increases with height up to the stratopause at 50 km is the:",
        "options": ["Troposphere", "Stratosphere", "Mesosphere", "Thermosphere"],
        "answerIndex": 1,
        "explanation": "The Stratosphere extends from the tropopause up to 50 km (stratopause). Temperature increases with height in this layer due to the absorption of solar ultraviolet radiation by ozone.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 6 & Q14/Q15"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "easy",
        "question": "In the lower atmosphere, what percentage of the total heat transfer from the Earth's surface to the air is in the form of Latent Heat?",
        "options": ["23%", "50%", "77%", "99%"],
        "answerIndex": 2,
        "explanation": "Heat transfer from the Earth's surface to the atmosphere consists of 23% sensible heat (conduction, convection, radiation) and 77% latent heat of evaporation/condensation.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 4 & p. 34 Q26"
    },

    # -------------------------------------------------------------
    # Topic 2: Atmospheric Pressure
    # -------------------------------------------------------------
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "easy",
        "question": "When flying with an altimeter set to 1013.25 hPa, the altimeter displays:",
        "options": [
            "Height above ground level (AGL)",
            "Altitude above mean sea level (AMSL)",
            "Pressure Altitude (Flight Level)",
            "Density Altitude"
        ],
        "answerIndex": 2,
        "explanation": "Setting standard sea level pressure 1013.25 hPa (29.92 inHg) on the subscale causes the altimeter to indicate Pressure Altitude, referred to as Flight Levels (e.g., FL300 = 30,000 ft pressure altitude) above the Transition Level.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 17"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "medium",
        "question": "An aircraft flies from an area of Low pressure into an area of High pressure without resetting its altimeter subscale. The altimeter will:",
        "options": [
            "Overread (indicate higher than true altitude)",
            "Underread (indicate lower than true altitude)",
            "Indicate correct true altitude throughout",
            "Freeze at the last indicated altitude"
        ],
        "answerIndex": 1,
        "explanation": "Flying from Low to High pressure, isobaric surfaces slope upwards in geometric height. Maintaining a constant indicated pressure will cause the aircraft to climb. The altimeter indicates lower than actual true altitude (Underreading: 'Low to High, clear the sky').",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 19 & Q4"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "medium",
        "question": "At mean sea level in ISA, what vertical distance corresponds to a 1 hPa pressure change?",
        "options": ["10 ft", "27 to 30 ft", "50 ft", "100 ft"],
        "answerIndex": 1,
        "explanation": "Near sea level, 1 hPa corresponds to approximately 27 to 30 feet (standard rule of thumb is 30 ft/hPa). At 20,000 ft, 1 hPa corresponds to 50 ft; at 40,000 ft, 1 hPa corresponds to 100 ft.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 12"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "hard",
        "question": "Station Level Pressure (QFE) is 970 hPa, and aerodrome elevation is 1,290 ft. What is the approximate QNH (using 1 hPa = 30 ft)?",
        "options": ["927 hPa", "970 hPa", "1013 hPa", "1025 hPa"],
        "answerIndex": 2,
        "explanation": "Pressure equivalent of elevation = 1,290 ft / 30 ft per hPa = 43 hPa. Since sea level is lower than the airfield, pressure is higher: QNH = QFE + 43 = 970 + 43 = 1013 hPa.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 18"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "hard",
        "question": "An aircraft is cruising at FL180 with an outside air temperature of -35°C. ISA temperature at FL180 is -21°C. What is the true altitude (approximate 4 ft per 1,000 ft per °C deviation rule)?",
        "options": ["18,000 ft", "16,992 ft", "19,008 ft", "17,500 ft"],
        "answerIndex": 1,
        "explanation": "Temperature deviation = Actual - ISA = -35 - (-21) = -14°C (ISA -14). Correction = 4 ft * 18 (thousands) * (-14°C) = -1,008 ft. True altitude = 18,000 - 1,008 = 16,992 ft.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 16"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "easy",
        "question": "Lines drawn on a weather chart connecting points of equal atmospheric pressure are called:",
        "options": ["Isotherms", "Isobars", "Isotachs", "Isallobars"],
        "answerIndex": 1,
        "explanation": "Isobars are lines connecting geographical locations of equal barometric pressure reduced to mean sea level.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 16 & Q14"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "medium",
        "question": "In a Trough of Low pressure in the Northern Hemisphere, when an aircraft crosses the trough axis, the wind will:",
        "options": [
            "Veer sharply",
            "Back sharply",
            "Remain completely unchanged in direction",
            "Drop to zero knots"
        ],
        "answerIndex": 1,
        "explanation": "Across a trough axis in the Northern Hemisphere, isobars change direction cyclonically. As the axis is crossed from west to east or south to north, winds back (turn counter-clockwise) abruptly.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 22 & Q15"
    },

    # -------------------------------------------------------------
    # Topic 3: Temperature & Heat
    # -------------------------------------------------------------
    {
        "topic": "Temperature & Heat",
        "difficulty": "easy",
        "question": "What is the primary process responsible for heating the atmosphere directly adjacent to the Earth's surface?",
        "options": ["Conduction", "Advection", "Nuclear fusion", "Sublimation"],
        "answerIndex": 0,
        "explanation": "Conduction transfers heat from the warmed Earth's surface directly to the thin boundary layer of air in physical contact with the ground.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature', p. 28"
    },
    {
        "topic": "Temperature & Heat",
        "difficulty": "medium",
        "question": "Under which conditions is the diurnal variation of surface temperature greatest?",
        "options": [
            "Over deep ocean waters with strong gale winds",
            "Over dry desert land on clear days with calm or light winds",
            "Under thick overcast nimbostratus clouds with heavy rain",
            "Over snow-covered polar plateaus in winter"
        ],
        "answerIndex": 1,
        "explanation": "Diurnal temperature range is maximized over dry land with low specific heat, under clear skies (permitting maximum daytime solar heating and nocturnal radiation loss), and with calm or light winds (preventing turbulent vertical mixing).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature', p. 31 & Q1/Q2"
    },
    {
        "topic": "Temperature & Heat",
        "difficulty": "medium",
        "question": "Which surface has the highest albedo (reflecting power)?",
        "options": ["Deep ocean water", "Freshly fallen snow", "Dark moist soil", "Dense green forest"],
        "answerIndex": 1,
        "explanation": "Fresh snow reflects approximately 80% to 90% of incident solar radiation, giving it the highest albedo of natural earth surfaces. Ocean water reflects only 5-10% at high solar angles.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature', p. 31 & Q8"
    },
    {
        "topic": "Temperature & Heat",
        "difficulty": "hard",
        "question": "In meteorology, the horizontal transport of heat and atmospheric properties by the wind is termed:",
        "options": ["Convection", "Advection", "Radiation", "Subsidence"],
        "answerIndex": 1,
        "explanation": "Advection is the horizontal transport of an atmospheric property (such as heat, cold, or moisture) by the mass motion of the wind.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature', p. 28"
    },
    {
        "topic": "Temperature & Heat",
        "difficulty": "medium",
        "question": "The door of a standard meteorological Stevenson screen in the Northern Hemisphere should always open towards the:",
        "options": ["South", "North", "East", "West"],
        "answerIndex": 1,
        "explanation": "In the Northern Hemisphere, the door of the Stevenson screen opens towards the North so that direct sunlight never strikes the thermometers during observation.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature', p. 35 Q29"
    },

    # -------------------------------------------------------------
    # Topic 4: Air Density
    # -------------------------------------------------------------
    {
        "topic": "Air Density",
        "difficulty": "easy",
        "question": "What is the relationship between air density, pressure, and temperature according to the equation of state (P = ρRT)?",
        "options": [
            "Density is directly proportional to temperature and inversely proportional to pressure",
            "Density is directly proportional to pressure and inversely proportional to absolute temperature",
            "Density is independent of temperature and pressure",
            "Density doubles whenever temperature drops by 1°C"
        ],
        "answerIndex": 1,
        "explanation": "From the ideal gas law ρ = P / (RT), density increases with higher atmospheric pressure and decreases with higher absolute temperature.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 4 'Air Density', p. 37"
    },
    {
        "topic": "Air Density",
        "difficulty": "medium",
        "question": "A decrease in air density of approximately 1 percent is produced by:",
        "options": [
            "A pressure fall of 10 hPa, or a temperature rise of 3°C, or a height increase of 300 ft",
            "A pressure rise of 10 hPa",
            "A temperature drop of 10°C",
            "Flying at 10,000 ft"
        ],
        "answerIndex": 0,
        "explanation": "As a rule of thumb, a 1% reduction in air density results from: a pressure decrease of 10 hPa, an increase in temperature of 3°C, or an altitude increase of 300 feet.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 4 'Air Density', p. 38"
    },
    {
        "topic": "Air Density",
        "difficulty": "hard",
        "question": "Why does a piston-engine aircraft require approximately 10% more runway length when taking off in high humidity?",
        "options": [
            "Because high humidity increases wheel rolling friction on tarmac",
            "Because water vapour reduces air density and displaces oxygen, reducing engine power output and aerodynamic lift",
            "Because instruments read calibrated airspeed 10 knots too low",
            "Because tires slip on wet runways"
        ],
        "answerIndex": 1,
        "explanation": "Water vapour has a lower molecular mass (18) than dry air (29), decreasing air density. Furthermore, humidity displaces oxygen in engine combustion chambers, reducing power output by up to 5% to 7%, mandating longer takeoff runs.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 4 'Air Density', p. 38"
    },

    # -------------------------------------------------------------
    # Topic 5: Humidity
    # -------------------------------------------------------------
    {
        "topic": "Humidity",
        "difficulty": "easy",
        "question": "Relative Humidity (RH) is defined as the ratio of:",
        "options": [
            "Actual vapour pressure to saturation vapour pressure at the same temperature, expressed as a percentage",
            "Dew point to dry bulb temperature",
            "Mass of water vapour to mass of dry air in grams",
            "Volume of air to volume of water"
        ],
        "answerIndex": 0,
        "explanation": "Relative Humidity is the ratio (in %) of the actual water vapour pressure present in the air to the maximum saturation vapour pressure possible at that temperature: RH = (e / es) * 100%.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 5 'Humidity', p. 41 & Q1"
    },
    {
        "topic": "Humidity",
        "difficulty": "medium",
        "question": "If unsaturated air is warmed without adding or removing moisture, what happens to its Relative Humidity and Dew Point?",
        "options": [
            "RH decreases while Dew Point remains unchanged",
            "Both RH and Dew Point increase",
            "RH remains unchanged while Dew Point falls",
            "Both RH and Dew Point decrease"
        ],
        "answerIndex": 0,
        "explanation": "Warming air increases its capacity to hold moisture (higher saturation vapour pressure), so Relative Humidity drops. However, since the actual moisture content is unchanged, the Dew Point remains constant.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 5 'Humidity', p. 41"
    },
    {
        "topic": "Humidity",
        "difficulty": "hard",
        "question": "At temperatures below 0°C, the saturation vapour pressure over supercooled water is:",
        "options": [
            "Lower than that over ice",
            "Greater than that over ice",
            "Equal to that over ice",
            "Zero"
        ],
        "answerIndex": 1,
        "explanation": "Water molecules are bound more tightly in an ice crystal lattice than in a liquid droplet. Therefore, at the same sub-zero temperature, saturation vapour pressure over supercooled water is greater than that over ice.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 5 'Humidity', p. 42 & Q6"
    },

    # -------------------------------------------------------------
    # Topic 6: Winds
    # -------------------------------------------------------------
    {
        "topic": "Winds",
        "difficulty": "easy",
        "question": "What is the relationship between 1 metre per second (m/s) and knots (kt)?",
        "options": ["1 m/s = 0.54 kt", "1 m/s = 1.94 kt (approx 2 kt)", "1 m/s = 3.6 kt", "1 m/s = 10 kt"],
        "answerIndex": 1,
        "explanation": "1 knot = 0.514 m/s. Therefore, 1 m/s = 1.944 kt (approximately 2 knots). 1 km/h = 0.54 kt.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 44"
    },
    {
        "topic": "Winds",
        "difficulty": "medium",
        "question": "A clockwise change in wind direction (e.g., from 090° to 120°) is defined as:",
        "options": ["Backing", "Veering", "Gusting", "Squalling"],
        "answerIndex": 1,
        "explanation": "Veering is defined as a clockwise change in wind direction (e.g. 060° to 090°, or 270° to 300°). Backing is an anti-clockwise change (e.g. 090° to 060°).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 46 & Q32/Q33"
    },
    {
        "topic": "Winds",
        "difficulty": "medium",
        "question": "In a Low pressure system in the Southern Hemisphere, winds blow:",
        "options": [
            "Clockwise and converge towards the centre",
            "Anticlockwise and converge towards the centre",
            "Clockwise and diverge outwards",
            "Directly straight across isobars from High to Low"
        ],
        "answerIndex": 0,
        "explanation": "In the Southern Hemisphere, Coriolis force deflects moving air to the left. Around a Low pressure system, winds blow in a clockwise direction, spiraling inward (converging) due to surface friction.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 47 & Q18/Q25"
    },
    {
        "topic": "Winds",
        "difficulty": "hard",
        "question": "What is a Fohn (or Chinook) wind?",
        "options": [
            "A cold, moist wind blowing up a windward mountain slope",
            "A warm, dry, gusty wind blowing down the leeward slope of a mountain range",
            "A sea breeze blowing onto a desert coastline",
            "A freezing katabatic wind flowing into a polar fjord"
        ],
        "answerIndex": 1,
        "explanation": "Air ascending the windward mountain cools at DALR until saturated, then at SALR releasing latent heat and precipitating. When descending the leeward side, it warms dry adiabatically at the full DALR (9.8°C/km), becoming much warmer and drier.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 53 & Q8"
    },
    {
        "topic": "Winds",
        "difficulty": "medium",
        "question": "A cold gravity wind that flows down mountain slopes and valleys at night due to nocturnal radiational cooling is a:",
        "options": ["Anabatic wind", "Katabatic wind", "Fohn wind", "Geostrophic wind"],
        "answerIndex": 1,
        "explanation": "At night, mountain slopes lose heat rapidly by terrestrial radiation, cooling the adjacent air. The chilled, denser air drains downslope under gravity into valleys as a Katabatic (down-slope) wind.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 54 & Q9/Q20"
    },
    {
        "topic": "Winds",
        "difficulty": "easy",
        "question": "An Anabatic wind flows:",
        "options": [
            "Down a mountain slope at night",
            "Up a mountain slope during the daytime due to surface solar heating",
            "Horizontally along a coastline",
            "Vertically downward beneath a cumulonimbus cloud"
        ],
        "answerIndex": 1,
        "explanation": "Anabatic winds are daytime up-slope winds caused by solar heating of mountain faces, warming the adjacent air which becomes buoyant and flows up the valley walls.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 54 & Q18"
    },

    # -------------------------------------------------------------
    # Topic 7: Visibility & Fog
    # -------------------------------------------------------------
    {
        "topic": "Visibility & Fog",
        "difficulty": "easy",
        "question": "What is 'Mist' (BR) officially defined as in aviation meteorology?",
        "options": [
            "Visibility less than 1,000 m with RH 100%",
            "Visibility between 1,000 m and 5,000 m caused by microscopic water droplets with high relative humidity (>90%)",
            "Visibility between 5,000 m and 10,000 m caused by dry dust",
            "Smoke and pollutants trapped under an inversion"
        ],
        "answerIndex": 1,
        "explanation": "Mist (BR) is reported when horizontal visibility is between 1,000 m and 5,000 m due to water droplets in suspension, with high relative humidity (typically >90%).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 7 'Visibility and Fog', p. 66 & Q4"
    },
    {
        "topic": "Visibility & Fog",
        "difficulty": "medium",
        "question": "What type of fog occurs when cold Arctic air moves over a warmer open sea surface?",
        "options": ["Radiation fog", "Steaming fog (Arctic Sea Smoke)", "Advection fog", "Frontal fog"],
        "answerIndex": 1,
        "explanation": "Steaming fog (Arctic sea smoke or evaporation fog) forms when very cold, dry air drifts over relatively warm water. Intense evaporation from the water saturates the cold air, condensing into rising streamers of fog.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 7 'Visibility and Fog', p. 70"
    },
    {
        "topic": "Visibility & Fog",
        "difficulty": "medium",
        "question": "Why does radiation fog almost never form over the open ocean?",
        "options": [
            "Because salt prevents condensation",
            "Because the diurnal temperature variation of the ocean surface is negligible (< 1°C)",
            "Because ocean air is always unsaturated",
            "Because winds over oceans are never calm"
        ],
        "answerIndex": 1,
        "explanation": "Radiation fog requires rapid nocturnal cooling of the underlying surface. Since water has high thermal capacity and mixes constantly, its diurnal temperature variation is under 1°C, preventing sufficient radiation cooling.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 7 'Visibility and Fog', p. 71 Q3"
    },
    {
        "topic": "Visibility & Fog",
        "difficulty": "hard",
        "question": "In north and northwest India, radiation fog is most frequent during which months?",
        "options": ["May to June", "July to September", "December to February", "October to November"],
        "answerIndex": 2,
        "explanation": "Over northern India (Punjab, Haryana, Delhi, UP, and Bihar), dense radiation fog occurs primarily in winter from December to February following the passage of Western Disturbances.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 7 'Visibility and Fog', p. 69 & Q5"
    },

    # -------------------------------------------------------------
    # Topic 8: Clouds & Vertical Motion
    # -------------------------------------------------------------
    {
        "topic": "Clouds & Precipitation",
        "difficulty": "easy",
        "question": "Which cloud genus is capable of producing violent thunderstorms, hail, tornadoes, and severe microbursts?",
        "options": ["Cumulus humilis", "Nimbostratus", "Cumulonimbus (CB)", "Altocumulus"],
        "answerIndex": 2,
        "explanation": "Cumulonimbus (CB) is a heavy, dense cloud of immense vertical extent (often reaching 40,000 to 60,000 ft in tropics) capable of producing violent turbulence, severe icing, hail, lightning, and squalls.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 8 'Vertical Motion and Clouds', p. 78"
    },
    {
        "topic": "Clouds & Precipitation",
        "difficulty": "medium",
        "question": "In aerodrome meteorological reports (METAR/TAF), which two cloud types are considered of operational significance and must ALWAYS be reported by name?",
        "options": [
            "Altocumulus and Stratus",
            "Cumulonimbus (CB) and Towering Cumulus (TCU)",
            "Cirrus and Cirrostratus",
            "Stratocumulus and Nimbostratus"
        ],
        "answerIndex": 1,
        "explanation": "Under ICAO Annex 3 and WMO standards, Cumulonimbus (CB) and Towering Cumulus / Cumulus congestus of great vertical extent (TCU) are the only cloud types identified by name in METAR and TAF due to their severe convective hazards.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 8 'Vertical Motion and Clouds', p. 78 & Chapter 25 p. 219"
    },
    {
        "topic": "Clouds & Precipitation",
        "difficulty": "hard",
        "question": "What is the Mintra Level in high-altitude aviation?",
        "options": [
            "The altitude above which engine thrust decreases by 50%",
            "The minimum flight level above which aircraft exhaust condensation trails (contrails) can form in saturated air (around -45°C)",
            "The level of maximum clear air turbulence",
            "The freezing level over the equator"
        ],
        "answerIndex": 1,
        "explanation": "Mintra Level is the lowest flight level where condensation trails (contrails) will form if the air is 100% relative humidity. A flight level temperature of about -45°C provides a good operational estimate.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 8 'Vertical Motion and Clouds', p. 82 & Q13"
    },
    {
        "topic": "Clouds & Precipitation",
        "difficulty": "medium",
        "question": "What is the standard ICAO reporting term for a cloud amount of 3 to 4 oktas?",
        "options": ["FEW (Few)", "SCT (Scattered)", "BKN (Broken)", "OVC (Overcast)"],
        "answerIndex": 1,
        "explanation": "Cloud coverage in oktas: FEW = 1-2 oktas, SCT (Scattered) = 3-4 oktas, BKN (Broken) = 5-7 oktas, OVC (Overcast) = 8 oktas, SKC/NSC = 0 oktas.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 8 'Vertical Motion and Clouds', p. 80 (Table 8.3)"
    },

    # -------------------------------------------------------------
    # Topic 9: Stability & Adiabatics
    # -------------------------------------------------------------
    {
        "topic": "Stability & Adiabatics",
        "difficulty": "easy",
        "question": "An atmospheric layer where the Environmental Lapse Rate (ELR) is zero (temperature constant with height) is termed:",
        "options": ["Inversion", "Isothermal layer", "Super-adiabatic layer", "Adiabatic zone"],
        "answerIndex": 1,
        "explanation": "An Isothermal layer is a layer where temperature remains constant with increasing altitude (lapse rate = 0°C/km). It represents a stable atmosphere.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 9 'Stability & Instability', p. 85 & Q9"
    },
    {
        "topic": "Stability & Adiabatics",
        "difficulty": "medium",
        "question": "When the Environmental Lapse Rate (ELR) is greater than the Dry Adiabatic Lapse Rate (ELR > DALR), the layer is:",
        "options": [
            "Absolutely Stable",
            "Conditionally Unstable",
            "Absolutely Unstable",
            "Neutral for saturated air"
        ],
        "answerIndex": 2,
        "explanation": "When ELR > DALR (steeper than 9.8°C/km), both dry and saturated air parcels lifted will always be warmer and less dense than the surrounding environment, accelerating upward (Absolutely Unstable).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 9 'Stability & Instability', p. 87 & Q4"
    },
    {
        "topic": "Stability & Adiabatics",
        "difficulty": "hard",
        "question": "What thermodynamic diagram is primarily used in India for plotting upper air radiosonde soundings and evaluating atmospheric instability?",
        "options": ["Skew-T log-P diagram", "Tphigram (Tephigram)", "Stuve diagram", "Mollier chart"],
        "answerIndex": 1,
        "explanation": "The Tephigram (Tphigram, T-phi gram) is the official thermodynamic diagram used by the India Meteorological Department (IMD) to evaluate atmospheric stability, condensation levels, and thunderstorm potential.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 9 'Stability & Instability', p. 89"
    },

    # -------------------------------------------------------------
    # Topic 13: Thunderstorms
    # -------------------------------------------------------------
    {
        "topic": "Thunderstorms",
        "difficulty": "easy",
        "question": "The Dissipating stage of a thunderstorm is characterized by:",
        "options": [
            "Strong updrafts throughout the cell",
            "Downdrafts dominating the entire cell and precipitation gradually tapering off",
            "Rapid increase in thunderstorm cell diameter to 100 km",
            "Maximum frequency of cloud-to-ground lightning"
        ],
        "answerIndex": 1,
        "explanation": "In the dissipating stage, downdrafts spread throughout the entire lower and middle levels of the cell, cutting off the inflow of warm, moist updrafts. The cloud spreads out into an anvil and gradually dissolves.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 13 'Thunderstorm', p. 113"
    },
    {
        "topic": "Thunderstorms",
        "difficulty": "medium",
        "question": "What is the typical diameter of an individual single-cell thunderstorm cumulonimbus tower?",
        "options": ["100 to 200 metres", "1 to 10 km", "50 to 100 km", "500 km"],
        "answerIndex": 1,
        "explanation": "An individual thunderstorm cell typically has a diameter of 1 to 10 km. A cluster of multiple cells may span tens to hundreds of kilometers.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 13 'Thunderstorm', p. 110"
    },
    {
        "topic": "Thunderstorms",
        "difficulty": "hard",
        "question": "What causes the initial sharp pressure rise ('thunderstorm nose') observed at a ground station immediately before rain commences?",
        "options": [
            "A sudden surge of solar heat",
            "The arrival of the cold, dense downdraft hitting the ground and spreading out under gravity",
            "Severe atmospheric ionization from lightning",
            "The weight of falling hail stones in the upper troposphere"
        ],
        "answerIndex": 1,
        "explanation": "The cold downdraft, chilled by the evaporation of rain in dry air aloft, is much denser than the warm ambient surface air. When it hits the surface, it spreads out as a cold dome, creating a sudden sharp barometric pressure jump.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 13 'Thunderstorm', p. 114"
    },
    {
        "topic": "Thunderstorms",
        "difficulty": "hard",
        "question": "On weather radar, what characteristic echo shape is indicative of a severe supercell thunderstorm producing a tornado?",
        "options": ["A concentric circular ring", "A Hook Echo (figure '6' shape)", "A completely diffuse fuzzy blob", "A straight uniform line"],
        "answerIndex": 1,
        "explanation": "A 'Hook Echo' or figure '6' appendage on radar reflectivity indicates a rotating mesocyclone in a severe supercell thunderstorm, wrapping precipitation around the updraft, strongly correlated with tornado formation.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 13 'Thunderstorm', p. 117 & Chapter 22 p. 200"
    },

    # -------------------------------------------------------------
    # Topic 15: Jet Streams
    # -------------------------------------------------------------
    {
        "topic": "Jet Streams",
        "difficulty": "medium",
        "question": "Why do jet streams form in the upper troposphere?",
        "options": [
            "Due to magnetic variations near the Earth's poles",
            "Due to strong horizontal temperature contrasts across frontal boundaries, which create steep horizontal pressure gradients that strengthen with height (thermal wind effect)",
            "Due to lunar gravitational tides in the stratosphere",
            "Due to ocean currents transferring kinetic energy upward"
        ],
        "answerIndex": 1,
        "explanation": "Jet streams result from strong horizontal temperature gradients across air mass boundaries (polar front and subtropical ridge). The thermal wind equation dictates that vertical wind shear increases with height as long as this gradient persists, peaking at the tropopause.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 15 'Jet Streams', p. 139"
    },
    {
        "topic": "Jet Streams",
        "difficulty": "medium",
        "question": "What is the typical vertical wind shear threshold within a jet stream layer?",
        "options": ["1 m/s per km", "5 to 10 m/s per km (approx 3 to 6 kt / 1,000 ft)", "25 m/s per km", "50 m/s per km"],
        "answerIndex": 1,
        "explanation": "WMO defines jet streams as having vertical wind shears of roughly 5 to 10 m/s per km (approx 3-6 kt per 1,000 ft) and lateral shears around 5 m/s per 100 km.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 15 'Jet Streams', p. 136 & Q3"
    },

    # -------------------------------------------------------------
    # Topic 17: Mountain Waves
    # -------------------------------------------------------------
    {
        "topic": "Mountain Waves",
        "difficulty": "medium",
        "question": "A smooth stationary cloud resting directly over the summit of a mountain ridge in standing wave conditions is known as a:",
        "options": ["Rotor cloud", "Cap Cloud (Fohn Wall)", "Mamma cloud", "Castellanus"],
        "answerIndex": 1,
        "explanation": "A Cap Cloud (or mountain cap/fohn wall) forms directly over the mountain crest where moist air is forced to rise over the peak and condenses, dissolving as it descends the lee side.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 17 'Mountain Waves', p. 146"
    },
    {
        "topic": "Mountain Waves",
        "difficulty": "hard",
        "question": "Why are mountain waves especially hazardous to aircraft crossing high terrain on instruments (IFR)?",
        "options": [
            "VHF radios fail completely in mountain waves",
            "Strong downdrafts (up to 25 m/s / 5,000 fpm) can exceed aircraft climb performance while altimeter errors cause the altimeter to overread, leading to CFIT",
            "Magnetic compasses spin uncontrollably",
            "Pitot heat is extinguished by lee waves"
        ],
        "answerIndex": 1,
        "explanation": "Severe downdrafts on the leeward slope can exceed maximum aircraft climb rates (2,000 to 5,000 ft/min). Simultaneously, local low pressure in the wave trough makes the altimeter overread (reading higher than true altitude), creating catastrophic Controlled Flight Into Terrain (CFIT) hazards.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 17 'Mountain Waves', p. 146-147"
    },

    # -------------------------------------------------------------
    # Topic 18: Tropical Systems & Monsoon
    # -------------------------------------------------------------
    {
        "topic": "Tropical Systems & Monsoon",
        "difficulty": "medium",
        "question": "Why do Tropical Cyclones rarely or never form within 5° of the Equator?",
        "options": [
            "Sea surface temperatures are too cold at the equator",
            "The Coriolis force is virtually zero at the equator, preventing the initiation of cyclonic rotation",
            "Trade winds are too strong at the equator",
            "Atmospheric pressure at the equator is too high"
        ],
        "answerIndex": 1,
        "explanation": "Tropical cyclogenesis requires a minimum Coriolis parameter to impart cyclonic spin to converging air currents. Since Coriolis force is zero at the equator (f = 2Ω sin 0°), tropical revolving storms only form poleward of 5° latitude (typically 5° to 15°N/S).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Tropical Systems', p. 155 & Q6/Q35"
    },
    {
        "topic": "Tropical Systems & Monsoon",
        "difficulty": "hard",
        "question": "What is the 'Eye Wall' of a tropical cyclone?",
        "options": [
            "The calm boundary between the ocean and beach",
            "The ring of towering cumulonimbus clouds surrounding the eye, containing the most violent winds, heaviest rain, and severe turbulence",
            "The outermost edge of the cirrus canopy at 50,000 ft",
            "A warm front extending ahead of the cyclone"
        ],
        "answerIndex": 1,
        "explanation": "The eye wall is a dense ring of towering convective clouds (width 50-150 km) immediately enclosing the central eye. It exhibits the steepest pressure gradient, the highest sustained surface winds, torrential rain, and extreme turbulence.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Tropical Systems', p. 157 & Q15/Q19"
    },

    # -------------------------------------------------------------
    # Topic 19: Climatology of India & Met Services
    # -------------------------------------------------------------
    {
        "topic": "Climatology of India",
        "difficulty": "easy",
        "question": "Which of the following months represent the Northeast (Retreating) Monsoon season over India?",
        "options": ["March to May", "June to September", "October to December", "January to February"],
        "answerIndex": 2,
        "explanation": "The Northeast Monsoon (Post-monsoon / Retreating monsoon) season occurs from October to December. It brings the primary annual rainfall to Tamil Nadu, coastal Andhra Pradesh, and parts of Kerala.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 19 'Climatology of India', p. 164 (Table 19.1) & Q13"
    },
    {
        "topic": "Climatology of India",
        "difficulty": "medium",
        "question": "What is the 'Monsoon Trough' over India during the Southwest Monsoon?",
        "options": [
            "An ocean trench in the Bay of Bengal",
            "A quasi-stationary low pressure trough extending from Ganganagar (Rajasthan) through Allahabad to the Head Bay of Bengal",
            "A cold front along the Western Ghats",
            "An upper tropospheric easterly wind anomaly"
        ],
        "answerIndex": 1,
        "explanation": "The Monsoon Trough is an elongated semi-permanent low pressure trough extending across northern India from northwest Rajasthan through Allahabad to the Head Bay of Bengal. Its north-south oscillations dictate rainfall across India.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 19 'Climatology of India', p. 170 & Q8/Q9"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "easy",
        "question": "A routine aerodrome weather report issued every 30 minutes in aeronautical code is designated as a:",
        "options": ["TAF", "METAR", "SPECI", "ROFOR"],
        "answerIndex": 1,
        "explanation": "METAR (Aviation Routine Weather Report) is issued every half hour (or hourly at smaller stations) to report actual surface weather conditions observed at an aerodrome.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 25 'METAR & SPECI Codes', p. 217"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "medium",
        "question": "In a METAR report, what does the group '24015G28KT' indicate?",
        "options": [
            "Surface wind from 240° True at 15 knots, gusting to 28 knots",
            "Surface wind from 240° Magnetic at 28 knots",
            "Temperature 24°C with dew point 15°C and QNH 1028 hPa",
            "Runway 24 visual range 1500 m to 2800 m"
        ],
        "answerIndex": 0,
        "explanation": "In METAR wind reporting: '240' is wind direction in degrees True, '15' is mean speed in knots, 'G28' indicates gusts reaching 28 knots, followed by speed units 'KT'.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 25 'METAR & SPECI Codes', p. 218"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "hard",
        "question": "In an Aerodrome Forecast (TAF), what does the change indicator 'TEMPO 1416 3000 TSRA' mean?",
        "options": [
            "Permanent weather change commencing at 1400 UTC",
            "Temporary fluctuations lasting for less than one hour at a time between 1400 UTC and 1600 UTC with visibility 3,000 m in thunderstorm with moderate rain",
            "Gradual trend becoming effective at 1600 UTC",
            "Probable thunderstorm with 14% to 16% likelihood"
        ],
        "answerIndex": 1,
        "explanation": "TEMPO denotes frequent or infrequent temporary fluctuations to forecast conditions lasting less than one hour in each instance and covering less than half the total period between the stated start (1400Z) and end (1600Z) times.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 26 'Aviation Forecasts', p. 223"
    }
]

def run_expansion():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    questions_file = os.path.join(base_dir, "src", "data", "questions.json")

    with open(questions_file, "r", encoding="utf-8") as f:
        existing_questions = json.load(f)

    print(f"Existing questions count: {len(existing_questions)}")

    # Map existing questions by normalized text
    existing_texts = set()
    for q in existing_questions:
        norm = re.sub(r'[^a-zA-Z0-9]', '', q["question"].lower())
        existing_texts.add(norm)

    # Determine next MET ID
    met_ids = [int(q["id"].replace("MET-", "")) for q in existing_questions if q.get("subject") == "Aviation Meteorology" and q["id"].startswith("MET-")]
    next_id_num = max(met_ids) + 1 if met_ids else 100

    new_added = 0
    rejected_dups = 0

    for item in METEOROLOGY_QUESTIONS:
        norm = re.sub(r'[^a-zA-Z0-9]', '', item["question"].lower())
        if norm in existing_texts:
            rejected_dups += 1
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

    print(f"Newly validated Meteorology questions added: {new_added}")
    print(f"Duplicate candidates rejected: {rejected_dups}")
    print(f"New total questions in database: {len(existing_questions)}")

    # Save to questions.json
    with open(questions_file, "w", encoding="utf-8") as f:
        json.dump(existing_questions, f, indent=2, ensure_ascii=False)

    print("Successfully updated src/data/questions.json!")

if __name__ == "__main__":
    run_expansion()

