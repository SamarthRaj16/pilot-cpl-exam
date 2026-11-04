# -*- coding: utf-8 -*-
"""
DGCA CPL Aviation Meteorology Question Generator & Validator
Based on I.C. Joshi 'Aviation Meteorology' (3rd Edition) & DGCA CPL Syllabus.
"""

import json
import os
import re

# Comprehensive Bank of Verified Meteorology Questions from I.C. Joshi
METEOROLOGY_EXPANSION_BANK = [
    # -------------------------------------------------------------
    # Topic 1: The Atmosphere
    # -------------------------------------------------------------
    {
        "topic": "The Atmosphere",
        "difficulty": "easy",
        "question": "What percentage of the atmospheric mass is contained below approximately 10 km (FL330)?",
        "options": ["50%", "75%", "90%", "99%"],
        "answerIndex": 1,
        "explanation": "Due to gravitational compression, half (50%) of the total atmospheric mass is concentrated below 6 km (approx 18,000 ft), and three-quarters (75%) is contained below 10 km (approx 33,000 ft).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 3"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "easy",
        "question": "By volume, what is the approximate proportion of Nitrogen to Oxygen in dry atmospheric air?",
        "options": ["1 : 4", "4 : 1", "3 : 1", "1 : 3"],
        "answerIndex": 1,
        "explanation": "Dry air consists of approximately 78.08% Nitrogen and 20.95% Oxygen by volume, giving a volumetric ratio of approximately 4:1 (78% : 21%). By weight, the ratio is approximately 3:1.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 2"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "medium",
        "question": "The atmospheric layer up to approximately 80 km where the relative composition of major gases remains uniform is called the:",
        "options": ["Heterosphere", "Homosphere", "Stratosphere", "Ionosphere"],
        "answerIndex": 1,
        "explanation": "The Homosphere extends from the earth's surface up to about 80 km altitude. Due to turbulent mixing and convective processes, the proportion of dry atmospheric gases remains practically constant. Above 80 km lies the Heterosphere.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 2"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "medium",
        "question": "At what altitude is the maximum concentration of atmospheric Ozone (O3) located?",
        "options": ["5 to 10 km", "10 to 15 km", "20 to 25 km", "45 to 50 km"],
        "answerIndex": 2,
        "explanation": "Atmospheric ozone is found between 10 and 50 km in the stratosphere, but its peak concentration occurs between 20 and 25 km where solar ultraviolet radiation strongly dissociates molecular oxygen.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 3 & Q22"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "medium",
        "question": "Above what altitude is supplementary breathing oxygen required for flight crew due to the rapid decrease in oxygen partial pressure?",
        "options": ["5,000 ft", "8,000 ft", "10,000 ft", "15,000 ft"],
        "answerIndex": 2,
        "explanation": "Under standard aviation regulations and physiology, supplementary oxygen is required when flying above 10,000 ft AMSL in unpressurized aircraft because the reduced partial pressure of oxygen induces hypoxia.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 2 & Q23"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "hard",
        "question": "In the standard International Standard Atmosphere (ISA), what is the temperature at an altitude of 17 km?",
        "options": ["-56.5°C", "-65.5°C", "-35.5°C", "-45.0°C"],
        "answerIndex": 0,
        "explanation": "In ISA, temperature decreases uniformly up to 11 km (36,090 ft) at 6.5°C/km to -56.5°C. From 11 km to 20 km (approx 65,000 ft), the stratosphere is isothermal at -56.5°C.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 7 & Q17"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "hard",
        "question": "If the ambient temperature at 2,000 m altitude is measured at +05°C, what is the ISA temperature deviation?",
        "options": ["-05°C", "-02°C", "+03°C", "+08°C"],
        "answerIndex": 2,
        "explanation": "ISA sea-level temperature is +15°C. At 2,000 m (2 km), ISA temperature is 15 - (2 * 6.5) = +02°C. With actual temperature of +05°C, ISA deviation = Actual - ISA = 5 - 2 = +03°C (ISA +3).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 8 & Q26"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "medium",
        "question": "The layer of the atmosphere where temperature stops falling with height and the lapse rate decreases to 2°C/km or less is the:",
        "options": ["Mesopause", "Stratopause", "Tropopause", "Ionopause"],
        "answerIndex": 2,
        "explanation": "The Tropopause marks the boundary between the troposphere and stratosphere. According to WMO, it is defined as the level where the lapse rate drops to 2°C/km or less and does not exceed this for at least 2 km.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 5"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "easy",
        "question": "The word 'tropos' from which Troposphere is derived means:",
        "options": ["Stratified", "Turning or mixing", "Warm layer", "Upper sphere"],
        "answerIndex": 1,
        "explanation": "'Tropos' is a Greek word meaning turning, overturning or mixing, reflecting the active vertical convective and turbulent mixing characteristic of weather in this layer.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 5 & Q8"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "hard",
        "question": "Rare mother-of-pearl (Nacreous) clouds form in which atmospheric layer?",
        "options": ["Mesosphere", "Upper Stratosphere", "Lower Troposphere", "Thermosphere"],
        "answerIndex": 1,
        "explanation": "Nacreous clouds (Mother-of-Pearl clouds) are formed in the upper stratosphere between 20 and 30 km altitude, usually in polar winter regions, composed of supercooled water droplets or ice crystals.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 6 & Q16/Q29"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "hard",
        "question": "Noctilucent clouds are observed in which region of the upper atmosphere?",
        "options": ["Troposphere", "Mesosphere", "Stratosphere", "Thermosphere"],
        "answerIndex": 1,
        "explanation": "Noctilucent (night-shining) clouds are the highest clouds in Earth's atmosphere, occurring in the Mesosphere at altitudes around 80 to 85 km in high latitudes during summer.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 6 & Q25"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "medium",
        "question": "The coldest atmospheric temperatures (approximately -90°C) occur at the:",
        "options": ["Tropopause over the poles", "Mesopause", "Stratopause", "Thermopause"],
        "answerIndex": 1,
        "explanation": "The lowest temperatures in the Earth's atmosphere occur at the Mesopause (around 80 to 85 km), where temperatures plummet to approximately -90°C (-130°F) before rising in the thermosphere.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 6"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "medium",
        "question": "What is the primary mechanism by which the troposphere is heated from below?",
        "options": [
            "Direct absorption of solar short-wave radiation by clean air",
            "Terrestrial radiation, conduction, and latent heat release from the Earth's surface",
            "Frictional dissipation of planetary jet streams",
            "Cosmic ray ionization in the ionosphere"
        ],
        "answerIndex": 1,
        "explanation": "The troposphere is virtually transparent to incoming solar shortwave radiation (only ~19% absorbed). The surface absorbs solar radiation, heats up, and transfers heat to the air via sensible heat (conduction/convection) and latent heat of condensation (77%).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 4 & p. 5"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "easy",
        "question": "Which atmospheric constituent is responsible for shielding life from harmful ultraviolet (UV) radiation?",
        "options": ["Carbon dioxide", "Water vapour", "Ozone", "Nitrogen"],
        "answerIndex": 2,
        "explanation": "Stratospheric ozone (O3) absorbs solar UV radiation (especially UV-B), shielding living organisms from biological radiation damage and warming the stratosphere.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 3"
    },
    {
        "topic": "The Atmosphere",
        "difficulty": "medium",
        "question": "Breaks in the tropopause typically occur at latitudes of approximately:",
        "options": ["10° and 30°", "40° and 60°", "0° and 90°", "15° and 75°"],
        "answerIndex": 1,
        "explanation": "The tropopause is not a continuous surface from equator to pole; it exhibits step-like discontinuities or breaks near 40° and 60° latitude where the subtropical and polar front jet streams are located.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'Atmosphere', p. 5 & Q12"
    },

    # -------------------------------------------------------------
    # Topic 2: Atmospheric Pressure
    # -------------------------------------------------------------
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "easy",
        "question": "What is the definition of QFE altimeter setting?",
        "options": [
            "Pressure reduced to Mean Sea Level assuming standard atmosphere conditions",
            "Actual atmospheric pressure measured at the aerodrome elevation reference point",
            "Pressure altitude corresponding to 1013.25 hPa datum",
            "Forecast lowest regional pressure setting valid for one hour"
        ],
        "answerIndex": 1,
        "explanation": "QFE is the actual barometric pressure measured at the aerodrome elevation (or runway threshold). When set on the altimeter subscale on the ground, the altimeter reads zero height.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 18"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "medium",
        "question": "If an airfield elevation is 1,500 ft and QFE is 950 hPa, what is the approximate QNH (using 1 hPa = 30 ft)?",
        "options": ["900 hPa", "980 hPa", "1000 hPa", "1013 hPa"],
        "answerIndex": 2,
        "explanation": "Height difference = Elevation / 30 ft per hPa = 1,500 / 30 = 50 hPa. Since sea level is lower than the airfield, pressure is higher: QNH = QFE + 50 = 950 + 50 = 1000 hPa.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 18"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "medium",
        "question": "When flying from a warm air mass into a cold air mass at a constant indicated altitude, the aircraft's true altitude will:",
        "options": [
            "Increase",
            "Decrease",
            "Remain constant",
            "Fluctuate rhythmically"
        ],
        "answerIndex": 1,
        "explanation": "In cold air, isobaric surfaces are packed closer together (higher density), causing the pressure levels to sit lower in geometric height. An altimeter maintaining a constant indicated pressure level will cause the aircraft to descend: 'From High to Low or Hot to Cold, Look out Below!'",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 19"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "easy",
        "question": "Semi-diurnal pressure oscillations in the tropics exhibit two maxima and two minima daily. The two daily pressure maxima occur at approximately:",
        "options": [
            "0400 hr and 1600 hr local time",
            "1000 hr and 2200 hr local time",
            "0600 hr and 1800 hr local time",
            "1200 hr and 2400 hr local time"
        ],
        "answerIndex": 1,
        "explanation": "Atmospheric solar tidal heating produces a semi-diurnal variation with maxima at approximately 1000 hr and 2200 hr local time, and minima at 0400 hr and 1600 hr local time. A disruption in this rhythm often portends adverse weather.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 14 & Q16"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "hard",
        "question": "Lines connecting geographical points experiencing equal barometric pressure change over a specified period are known as:",
        "options": ["Isobars", "Isallobars", "Isotherms", "Isotachs"],
        "answerIndex": 1,
        "explanation": "Isallobars are lines joining places of equal atmospheric pressure tendency (pressure change over the past 3 hours or 24 hours). An isallobaric low indicates where pressure is falling most rapidly.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 17 & Q5"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "medium",
        "question": "In the International Standard Atmosphere (ISA), the pressure level of 500 hPa corresponds to an altitude of:",
        "options": ["10,000 ft", "18,000 ft", "24,000 ft", "30,000 ft"],
        "answerIndex": 1,
        "explanation": "In standard ISA conditions, 850 hPa corresponds to 5,000 ft, 700 hPa to 10,000 ft, 500 hPa to 18,000 ft (FL180), 300 hPa to 30,000 ft (FL300), and 200 hPa to 38,000 ft (FL380).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 19 (Table 2.1) & Q25"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "hard",
        "question": "What is the D-value in altimetry?",
        "options": [
            "Indicated Altitude minus True Altitude",
            "True Altitude minus Indicated Altitude",
            "Calibrated Airspeed minus True Airspeed",
            "Density Altitude minus Pressure Altitude"
        ],
        "answerIndex": 1,
        "explanation": "D-value is defined as True Altitude minus Indicated Altitude (Pressure Altitude): D = True Alt - Indicated Alt. It is positive when true altitude exceeds indicated altitude and negative when true altitude is lower.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 15"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "medium",
        "question": "In a Low pressure system in the Northern Hemisphere, surface winds blow:",
        "options": [
            "Clockwise and outwards",
            "Anticlockwise and converging inwards",
            "Directly parallel to straight isobars without friction",
            "Clockwise and converging inwards"
        ],
        "answerIndex": 1,
        "explanation": "In the Northern Hemisphere, pressure gradient force drives air towards low pressure, Coriolis deflects it to the right, and surface friction causes winds to blow counter-clockwise (cyclonic) and cross isobars inward towards the center (convergence).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 21 & Q1"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "easy",
        "question": "A neutral area situated between two Highs and two Lows with light and variable winds is designated as a:",
        "options": ["Trough", "Ridge", "Col", "Depression"],
        "answerIndex": 2,
        "explanation": "A Col is the saddle-shaped region between two Highs and two Lows. Pressure is relatively uniform with slack gradients and light variable winds, frequently prone to fog in winter or thunderstorms in summer.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 22 & Q7"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "medium",
        "question": "Why is surface visibility typically poorer in an Anticyclone (High) than in a Depression (Low)?",
        "options": [
            "Because high winds in anticyclones stir up heavy dust storms",
            "Because descending air (subsidence) traps pollutants, dust, and moisture in the lower levels",
            "Because anticyclones are always saturated with continuous rain",
            "Because updrafts in anticyclones carry smoke to high altitudes"
        ],
        "answerIndex": 1,
        "explanation": "Anticyclones are characterized by large-scale descending air (subsidence). Subsidence creates a temperature inversion that acts as an atmospheric lid, trapping haze, smoke, and moisture near the ground, producing poor visibility.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', p. 21 & Q8"
    },
    {
        "topic": "Atmospheric Pressure",
        "difficulty": "hard",
        "question": "An aircraft is cleared to cruise at FL290. Which standard isobaric surface does FL290 correspond closely to?",
        "options": ["500 hPa", "400 hPa", "300 hPa", "250 hPa"],
        "answerIndex": 2,
        "explanation": "FL300 (30,000 ft) corresponds to standard 300 hPa isobaric level (FL290 is 29,000 ft, approximately 315 hPa, closest to 300 hPa).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure', Table 2.1 & Q29"
    },

    # -------------------------------------------------------------
    # Topic 3: Temperature & Heat
    # -------------------------------------------------------------
    {
        "topic": "Temperature & Heat",
        "difficulty": "easy",
        "question": "At what temperature do the Celsius and Fahrenheit temperature scales read the exact same value?",
        "options": ["0°", "-32°", "-40°", "-273°"],
        "answerIndex": 2,
        "explanation": "Using F = (9/5)C + 32, when F = C: C = (9/5)C + 32 => -(4/5)C = 32 => C = -40°. Thus, -40°C is equal to -40°F.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature', p. 26 & Q27"
    },
    {
        "topic": "Temperature & Heat",
        "difficulty": "easy",
        "question": "The fraction of incoming solar radiation reflected back into space by the Earth and its atmosphere is defined as:",
        "options": ["Insolation", "Albedo", "Advection", "Sensible heat"],
        "answerIndex": 1,
        "explanation": "Albedo is the ratio of reflected solar radiation to total incident solar radiation. The Earth's average planetary albedo is approximately 30% (0.30). Snow surfaces have the highest albedo (~80%).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature', p. 31 & Q4"
    },
    {
        "topic": "Temperature & Heat",
        "difficulty": "medium",
        "question": "Stefan-Boltzmann's Law states that the total energy emitted by a black body is directly proportional to:",
        "options": ["T", "T²", "T³", "T⁴"],
        "answerIndex": 3,
        "explanation": "Stefan-Boltzmann's Law states E = σT⁴, meaning total radiant energy emitted per unit surface area of a black body is proportional to the fourth power of its absolute temperature (Kelvin).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature', p. 29 & Q22"
    },
    {
        "topic": "Temperature & Heat",
        "difficulty": "medium",
        "question": "On a clear, calm day, at what time does the minimum surface screen temperature typically occur?",
        "options": [
            "Exactly at midnight",
            "At sunrise",
            "Approximately 30 to 60 minutes after sunrise",
            "Two hours before sunrise"
        ],
        "answerIndex": 2,
        "explanation": "Nocturnal radiative cooling continues until incoming solar radiation balances and then exceeds outgoing terrestrial radiation. This equilibrium occurs approximately 30 to 60 minutes after sunrise, when minimum temperature is reached.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature', p. 32 & Q13"
    },
    {
        "topic": "Temperature & Heat",
        "difficulty": "medium",
        "question": "Why is the diurnal variation of temperature much smaller over the oceans (< 1°C) than over land (up to 20°C)?",
        "options": [
            "Water has a much lower specific heat capacity than soil",
            "Water has higher specific heat, transparency allowing deep solar penetration, and continuous convective mixing",
            "Ocean water radiates only short-wave radiation at night",
            "Clouds never form over the oceans"
        ],
        "answerIndex": 1,
        "explanation": "Water has high specific heat (1.0 vs ~0.2 for dry soil), sunlight penetrates several meters into transparent water distributing heat, evaporation absorbs heat, and wave mixing distributes warmth through a deep layer.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature', p. 31 & Q6"
    },
    {
        "topic": "Temperature & Heat",
        "difficulty": "hard",
        "question": "Wien's Displacement Law dictates that as the temperature of an emitting body increases, the wavelength of its peak radiation:",
        "options": [
            "Becomes longer",
            "Becomes shorter",
            "Remains completely unchanged",
            "Shifts into the ultra-long radio band"
        ],
        "answerIndex": 1,
        "explanation": "Wien's Law states λ_max = constant / T. The wavelength of maximum emission is inversely proportional to absolute temperature. The hot Sun (~6000 K) emits short waves; the cooler Earth (~288 K) emits long infrared waves.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature', p. 29 & Q17/Q24"
    },
    {
        "topic": "Temperature & Heat",
        "difficulty": "easy",
        "question": "Standard surface air temperature is measured in a Stevenson screen at a standard height of:",
        "options": ["1.25 m (4 ft) above ground in shade", "2.50 m (8 ft) above ground", "0.50 m above ground", "At runway surface level"],
        "answerIndex": 0,
        "explanation": "Surface temperature is recorded by thermometers installed in a white, louvered Stevenson screen located at 1.25 m (approx 4 ft) above the ground in the shade to prevent direct solar and ground radiation errors.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature', p. 27 & Q28"
    },
    {
        "topic": "Temperature & Heat",
        "difficulty": "medium",
        "question": "Cloudy nights are generally warmer than clear nights because clouds:",
        "options": [
            "Release ozone that warms the lower atmosphere",
            "Absorb and re-radiate terrestrial long-wave radiation back toward the surface",
            "Trap solar radiation from the following morning",
            "Increase atmospheric pressure which generates compressive heat"
        ],
        "answerIndex": 1,
        "explanation": "Low and medium cloud decks act as a radiation blanket. They absorb outgoing terrestrial infrared radiation emitted by the Earth and re-radiate it downward, curtailing nocturnal radiative cooling.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature', p. 32 & Q15"
    },

    # -------------------------------------------------------------
    # Topic 4: Air Density
    # -------------------------------------------------------------
    {
        "topic": "Air Density",
        "difficulty": "easy",
        "question": "In the International Standard Atmosphere (ISA), what is the standard air density at sea level?",
        "options": ["1.000 kg/m³", "1.225 kg/m³ (1225 g/m³)", "1.500 kg/m³", "0.950 kg/m³"],
        "answerIndex": 1,
        "explanation": "ISA standard sea-level air density is defined as 1.225 kg/m³ (or 1225 g/m³) at a temperature of 15°C and pressure of 1013.25 hPa.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 4 'Air Density', p. 37"
    },
    {
        "topic": "Air Density",
        "difficulty": "medium",
        "question": "For every 1°C increase in temperature above ISA, density altitude increases by approximately:",
        "options": ["30 ft", "60 ft", "120 ft", "240 ft"],
        "answerIndex": 2,
        "explanation": "Density altitude is pressure altitude corrected for non-standard temperature. For every 1°C that ambient temperature exceeds ISA, density altitude increases by roughly 120 ft (Rule of Thumb: DA = PA + 120 * [OAT - ISA]).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 4 'Air Density', p. 36"
    },
    {
        "topic": "Air Density",
        "difficulty": "medium",
        "question": "At constant pressure and temperature, how does moist (humid) air compare in density to dry air?",
        "options": [
            "Moist air is denser than dry air",
            "Moist air is less dense than dry air",
            "Moist air and dry air have identical density",
            "Moist air is denser only when freezing"
        ],
        "answerIndex": 1,
        "explanation": "The molecular weight of water vapour (H2O = 18 g/mol) is lighter than the molecular weight of dry air (approx 29 g/mol). When water vapour displaces nitrogen/oxygen molecules, the mixture becomes less dense.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 4 'Air Density', p. 37 & Q6"
    },
    {
        "topic": "Air Density",
        "difficulty": "hard",
        "question": "How does a high density altitude affect aircraft takeoff and climb performance?",
        "options": [
            "Shortens takeoff ground run and increases rate of climb",
            "Increases takeoff ground run, decreases rate of climb, and increases true airspeed at stall",
            "Decreases engine thrust requirements and increases service ceiling",
            "Requires less runway length due to reduced aerodynamic parasite drag"
        ],
        "answerIndex": 1,
        "explanation": "Low air density (high density altitude) degrades aerodynamic lift and propeller/engine thrust efficiency. The aircraft requires a longer takeoff ground roll, exhibits lower climb gradients, and its true airspeed at any indicated airspeed increases.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 4 'Air Density', p. 36"
    },
    {
        "topic": "Air Density",
        "difficulty": "medium",
        "question": "At what altitude does atmospheric air density reduce to approximately half of its sea-level value?",
        "options": ["3 km (10,000 ft)", "6 km (20,000 ft)", "11 km (36,000 ft)", "16 km (52,000 ft)"],
        "answerIndex": 1,
        "explanation": "Due to gravitational pressure decrease with height, air density reduces to 1/2 of sea level value at ~6 km (20,000 ft), 1/4 at 11 km (36,000 ft), and 1/8 at 17 km (55,000 ft).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 4 'Air Density', p. 38"
    },

    # -------------------------------------------------------------
    # Topic 5: Humidity
    # -------------------------------------------------------------
    {
        "topic": "Humidity",
        "difficulty": "easy",
        "question": "The temperature to which moist air must be cooled at constant pressure to reach saturation is defined as:",
        "options": ["Wet bulb temperature", "Dew point temperature", "Virtual temperature", "Potential temperature"],
        "answerIndex": 1,
        "explanation": "Dew Point (Td) is the temperature to which moist air must be cooled at constant pressure and water vapour content in order to reach saturation (100% Relative Humidity).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 5 'Humidity', p. 41 & Q2"
    },
    {
        "topic": "Humidity",
        "difficulty": "medium",
        "question": "When the air temperature and dew point temperature are equal, what is the Relative Humidity?",
        "options": ["0%", "50%", "75%", "100%"],
        "answerIndex": 3,
        "explanation": "When dry bulb temperature equals dew point temperature (zero spread), the air can hold no additional water vapour at that temperature and Relative Humidity is 100% (saturated).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 5 'Humidity', p. 41 & Q3"
    },
    {
        "topic": "Humidity",
        "difficulty": "hard",
        "question": "When an unsaturated parcel of air is lifted adiabatically without condensation, its Humidity Mixing Ratio (HMR):",
        "options": [
            "Increases steadily",
            "Decreases steadily",
            "Remains constant",
            "Becomes zero at 10,000 ft"
        ],
        "answerIndex": 2,
        "explanation": "Humidity Mixing Ratio (g/kg) is the mass of water vapour per mass of dry air. In adiabatic ascent without condensation, no water is added or removed, so the mixing ratio remains strictly conservative/constant.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 5 'Humidity', p. 42 & Q9"
    },
    {
        "topic": "Humidity",
        "difficulty": "medium",
        "question": "Why is carburetor icing most dangerous between ambient temperatures of -10°C and +30°C in humid air?",
        "options": [
            "Because fuel vaporization and adiabatic pressure drop in the venturi cause temperature drops of up to 20°C to 25°C",
            "Because engines run excessively hot in this temperature band",
            "Because aircraft fly slower in humid air",
            "Because oil viscosity breaks down below +30°C"
        ],
        "answerIndex": 0,
        "explanation": "Fuel vaporization and expansion cooling in the carburetor venturi can cause a temperature drop of up to 20-25°C. In air with high relative humidity (>60%), moisture condenses and freezes into ice even when OAT is as warm as +20°C to +30°C.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 12 'Ice Accretion', p. 107"
    },

    # -------------------------------------------------------------
    # Topic 6: Winds
    # -------------------------------------------------------------
    {
        "topic": "Winds",
        "difficulty": "easy",
        "question": "Buys Ballot's Law states that in the Northern Hemisphere, if an observer stands with their back to the wind:",
        "options": [
            "Low pressure is to their right and High pressure is to their left",
            "Low pressure is to their left and High pressure is to their right",
            "Low pressure is directly ahead",
            "High pressure is directly behind"
        ],
        "answerIndex": 1,
        "explanation": "Buys Ballot's Law: In the Northern Hemisphere, when standing with your back to the wind, lower pressure is to your left and higher pressure is to your right. (In Southern Hemisphere, low pressure is to your right).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 47 & Q1"
    },
    {
        "topic": "Winds",
        "difficulty": "medium",
        "question": "What is the Geostrophic Wind defined as?",
        "options": [
            "Wind blowing directly across isobars caused solely by friction",
            "Horizontal wind resulting from an exact balance between Pressure Gradient Force and Coriolis Force along straight, parallel isobars",
            "Wind blowing around sharply curved cyclonic isobars",
            "Vertical convection wind inside a thunderstorm updraft"
        ],
        "answerIndex": 1,
        "explanation": "The geostrophic wind is the theoretical horizontal wind resulting from an exact balance between the horizontal Pressure Gradient Force (PGF) and the Coriolis Force (f), blowing parallel to straight, parallel isobars above the friction layer.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 48 & Q5"
    },
    {
        "topic": "Winds",
        "difficulty": "medium",
        "question": "Where on the Earth is the Coriolis force equal to zero?",
        "options": ["At the North Pole", "At the South Pole", "At the Equator (0° latitude)", "At 45° latitude"],
        "answerIndex": 2,
        "explanation": "The Coriolis parameter is f = 2Ω sin(φ). At the equator (latitude φ = 0°), sin(0) = 0, so the Coriolis force is zero. It reaches its maximum value at the poles (φ = 90°, sin(90°) = 1).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 47 & Q6"
    },
    {
        "topic": "Winds",
        "difficulty": "hard",
        "question": "In an Anticyclone (High) in the Northern Hemisphere, how does the Gradient Wind speed compare to the Geostrophic Wind speed for the same pressure gradient?",
        "options": [
            "Gradient wind is weaker (sub-geostrophic)",
            "Gradient wind is stronger (super-geostrophic)",
            "Gradient wind is exactly equal to geostrophic wind",
            "Gradient wind cannot exist in an anticyclone"
        ],
        "answerIndex": 1,
        "explanation": "In an anticyclone, centrifugal force acts outwards in the same direction as the pressure gradient force, opposing Coriolis force. To achieve balance, Coriolis force must be larger, requiring the wind speed to be super-geostrophic (faster than geostrophic wind).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 50 & Q41"
    },
    {
        "topic": "Winds",
        "difficulty": "medium",
        "question": "Due to surface friction, how does the surface wind typically differ from the geostrophic wind above the friction layer in the Northern Hemisphere?",
        "options": [
            "Surface wind veers and increases in speed",
            "Surface wind backs (turns counter-clockwise) and decreases in speed by roughly 30% to 50%",
            "Surface wind direction remains unchanged while speed doubles",
            "Surface wind blows perpendicular to isobars towards High pressure"
        ],
        "answerIndex": 1,
        "explanation": "Surface friction retards wind speed, reducing Coriolis force. Consequently, the Pressure Gradient Force pulls the wind across isobars toward low pressure. In the Northern Hemisphere, this causes the wind to back (anti-clockwise) and slow down.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 51"
    },
    {
        "topic": "Winds",
        "difficulty": "easy",
        "question": "A sudden increase in wind speed of at least 16 knots (32 km/h) that sustains for at least one minute before gradually subsiding is classified as a:",
        "options": ["Gust", "Squall", "Gale", "Lull"],
        "answerIndex": 1,
        "explanation": "A squall is a sudden increase in wind speed by at least 16 kt (32 km/h), reaching 22 kt or more, and lasting for at least one minute. In contrast, a gust is a brief, transient fluctuation lasting only seconds.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 46 & Q15"
    },
    {
        "topic": "Winds",
        "difficulty": "medium",
        "question": "The Thermal Wind represents:",
        "options": [
            "Updrafts caused by thermal solar heating over black tarmac",
            "The vector difference between the geostrophic wind at an upper level and the geostrophic wind at a lower level",
            "Warm winds blowing down the lee side of mountain ranges",
            "Surface sea breeze currents during the daytime"
        ],
        "answerIndex": 1,
        "explanation": "The Thermal Wind (Vt) is the vertical geostrophic wind shear: the vector difference between the upper-level geostrophic wind (V1) and lower-level geostrophic wind (V0). It blows parallel to thickness lines with cold air on the left in the Northern Hemisphere.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 57 & Q16"
    },
    {
        "topic": "Winds",
        "difficulty": "hard",
        "question": "Lower level wind is 050°/10 kt and upper level wind is 230°/05 kt. What is the thermal wind vector?",
        "options": ["050°/05 kt", "230°/15 kt", "050°/15 kt", "140°/10 kt"],
        "answerIndex": 1,
        "explanation": "Thermal wind Vt = V_upper - V_lower. Lower = 050/10 = - (230/10). Upper = 230/05. Subtracting lower: 230/05 - (-230/10) = 230° / 15 kt.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 57 & Q31"
    },
    {
        "topic": "Winds",
        "difficulty": "easy",
        "question": "What is the Beaufort Scale threshold for a 'Gale' force wind?",
        "options": ["22 to 27 knots", "28 to 33 knots", "34 to 40 knots", "48 to 55 knots"],
        "answerIndex": 2,
        "explanation": "Under the Beaufort Scale (Force 8), a Gale is defined as a persistent mean wind speed of 34 to 40 knots (62-74 km/h).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 59 (Table 6.2) & Q42"
    },
    {
        "topic": "Winds",
        "difficulty": "medium",
        "question": "A Sea Breeze circulation typically commences in the:",
        "options": [
            "Late afternoon and blows from land to sea",
            "Late morning or early afternoon and blows from sea toward the heated land",
            "Middle of the night due to radiational cooling",
            "Winter months only during cold air outbreaks"
        ],
        "answerIndex": 1,
        "explanation": "During daytime, solar heating warms land much faster than water. Air over land rises, lowering surface pressure; cooler, denser air over the sea moves inland. Sea breezes set in by late morning/afternoon and die down near sunset.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Winds', p. 55 & Q11"
    },

    # -------------------------------------------------------------
    # Topic 7: Visibility & Fog
    # -------------------------------------------------------------
    {
        "topic": "Visibility & Fog",
        "difficulty": "easy",
        "question": "In aviation meteorological reporting, 'Fog' (FG) is officially reported when horizontal visibility is reduced to:",
        "options": ["Less than 500 metres", "Less than 1,000 metres", "Between 1,000 m and 5,000 m", "Less than 2,000 metres"],
        "answerIndex": 1,
        "explanation": "Fog (FG) is reported when visibility is reduced to less than 1,000 metres with relative humidity near 100%. If visibility is between 1,000 m and 5,000 m with high humidity, it is reported as Mist (BR).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 7 'Visibility and Fog', p. 66 & Q1/Q4"
    },
    {
        "topic": "Visibility & Fog",
        "difficulty": "medium",
        "question": "Which set of meteorological conditions is most favourable for the formation of Radiation Fog?",
        "options": [
            "Strong gale winds, overcast cumulonimbus, and high dry air",
            "High relative humidity, clear skies, light winds (2 to 7 knots), and a stable inversion layer",
            "Steep super-adiabatic lapse rate and squally turbulent winds",
            "Passage of a fast-moving cold front over the open sea"
        ],
        "answerIndex": 1,
        "explanation": "Radiation fog requires: high relative humidity near the surface, clear night skies for maximum nocturnal terrestrial radiation cooling, light wind (2-7 kt) to promote gentle turbulent mixing without dissipating fog, and atmospheric stability.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 7 'Visibility and Fog', p. 69 & Q14"
    },
    {
        "topic": "Visibility & Fog",
        "difficulty": "medium",
        "question": "How does Advection Fog form?",
        "options": [
            "By nocturnal radiational cooling of dry ground on clear calm nights",
            "When warm, moist air moves horizontally over a relatively colder land or water surface",
            "By the evaporation of rain falling from altostratus clouds",
            "By the adiabatic expansion of air forced over a steep mountain peak"
        ],
        "answerIndex": 1,
        "explanation": "Advection fog forms when a warm, moist air mass moves horizontally over a cold surface (land or water). The lower layer of the air mass is cooled below its dew point by conduction, triggering widespread condensation.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 7 'Visibility and Fog', p. 70 & Q7/Q12"
    },
    {
        "topic": "Visibility & Fog",
        "difficulty": "hard",
        "question": "Why does radiation fog frequently thicken or persist for about 30–60 minutes after sunrise?",
        "options": [
            "Sunlight generates sudden downdrafts in the upper troposphere",
            "Initial solar heating induces weak thermal turbulence that mixes moist surface air upward without immediately raising temperature above dew point",
            "Relative humidity increases dramatically after sunrise",
            "The sun triggers instantaneous frontal cyclogenesis"
        ],
        "answerIndex": 1,
        "explanation": "Just after sunrise, weak ground heating initiates gentle convective stirring. This mixes the saturated surface air through a slightly deeper layer, causing the fog to thicken temporarily before sustained solar heating evaporates it.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 7 'Visibility and Fog', p. 69"
    },
    {
        "topic": "Visibility & Fog",
        "difficulty": "medium",
        "question": "What is Runway Visual Range (RVR)?",
        "options": [
            "The vertical distance up to which an approaching pilot can see the ground",
            "The range over which the pilot of an aircraft on the centreline of a runway can see the runway surface markings or delineating lights",
            "The general prevailing visibility reported by the airport weather observer",
            "The slant visibility measured from the final approach fix"
        ],
        "answerIndex": 1,
        "explanation": "ICAO defines RVR as the range over which the pilot of an aircraft on the centre line of a runway can see the runway surface markings or the lights delineating the runway or identifying its centre line.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 7 'Visibility and Fog', p. 66"
    },

    # -------------------------------------------------------------
    # Topic 8: Clouds & Vertical Motion
    # -------------------------------------------------------------
    {
        "topic": "Clouds & Precipitation",
        "difficulty": "easy",
        "question": "Which of the following is officially classified as a High Cloud with bases typically between 20,000 ft and 40,000 ft?",
        "options": ["Altocumulus", "Stratocumulus", "Cirrostratus", "Nimbostratus"],
        "answerIndex": 2,
        "explanation": "High clouds consist of Cirrus (CI), Cirrocumulus (CC), and Cirrostratus (CS), composed almost entirely of ice crystals with bases between 20,000 ft and 40,000 ft (6-12 km) in temperate and tropical zones.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 8 'Vertical Motion and Clouds', p. 77"
    },
    {
        "topic": "Clouds & Precipitation",
        "difficulty": "medium",
        "question": "A solar or lunar halo optical phenomenon is uniquely associated with which cloud type?",
        "options": ["Altostratus", "Cirrostratus", "Stratocumulus", "Nimbostratus"],
        "answerIndex": 1,
        "explanation": "Halos (circular 22° rings around the Sun or Moon) are produced by the refraction of light through hexagonal ice crystals found in thin sheets of Cirrostratus (CS) clouds.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 8 'Vertical Motion and Clouds', p. 77 & Q10"
    },
    {
        "topic": "Clouds & Precipitation",
        "difficulty": "medium",
        "question": "Continuous, steady rain or snow falling from an overcast dark gray, thick cloud layer without lightning is characteristic of:",
        "options": ["Cumulonimbus", "Nimbostratus", "Altocumulus lenticularis", "Cirrocumulus"],
        "answerIndex": 1,
        "explanation": "Nimbostratus (NS) is a thick, dark gray, featureless middle/low cloud layer that produces continuous, widespread precipitation (rain or snow) without lightning or thunder.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 8 'Vertical Motion and Clouds', p. 77 & Q6"
    },
    {
        "topic": "Clouds & Precipitation",
        "difficulty": "hard",
        "question": "What does the cloud species name 'Castellanus' indicate to an aviator?",
        "options": [
            "Completely smooth lens-shaped cloud formed in lee waves",
            "Turreted castle-like vertical convective towers indicating mid-level instability",
            "Ragged, torn clouds formed under the base of rain clouds",
            "Fibrous wispy filaments with hooked ends"
        ],
        "answerIndex": 1,
        "explanation": "Castellanus (such as Altocumulus castellanus, ACC) exhibits vertical turrets rising from a common base, resembling castle battlements. It signifies instability in the middle troposphere, often preceding thunderstorms.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 8 'Vertical Motion and Clouds', p. 81"
    },
    {
        "topic": "Clouds & Precipitation",
        "difficulty": "medium",
        "question": "What is 'Virga'?",
        "options": [
            "Precipitation that evaporates or sublimates before reaching the ground",
            "Supercooled rain droplets that freeze on impact with an airframe",
            "Violent downburst winds emerging from a dying thunderstorm",
            "A dense layer of dust suspended above an inversion"
        ],
        "answerIndex": 0,
        "explanation": "Virga refers to streaks or shafts of rain or ice crystals falling from a cloud base that evaporate completely in dry sub-cloud air before reaching the Earth's surface.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 8 'Vertical Motion and Clouds', p. 78 & Q14"
    },
    {
        "topic": "Clouds & Precipitation",
        "difficulty": "easy",
        "question": "According to ICAO meteorological standards, 'Cloud Ceiling' is defined as the height of the base of the lowest cloud layer covering more than:",
        "options": ["2/8 of the sky", "4/8 of the sky (more than half: 5/8 or more)", "7/8 of the sky", "8/8 of the sky only"],
        "answerIndex": 1,
        "explanation": "Ceiling is defined as the height above the ground or water of the base of the lowest layer of cloud below 6,000 m (20,000 ft) covering more than half the sky (i.e., BKN [5-7 oktas] or OVC [8 oktas]).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 8 'Vertical Motion and Clouds', p. 80 & Q16"
    },

    # -------------------------------------------------------------
    # Topic 9: Stability & Adiabatics
    # -------------------------------------------------------------
    {
        "topic": "Stability & Adiabatics",
        "difficulty": "easy",
        "question": "What is the numerical value of the Dry Adiabatic Lapse Rate (DALR)?",
        "options": ["6.5°C per km", "9.8°C per km (approx 3.0°C / 1,000 ft)", "1.5°C per km", "4.0°C per km"],
        "answerIndex": 1,
        "explanation": "DALR is the rate at which unsaturated air cools as it ascends adiabatically, equal to 9.8°C/km (or 3°C per 1,000 ft).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 9 'Stability & Instability', p. 86 & Q11"
    },
    {
        "topic": "Stability & Adiabatics",
        "difficulty": "medium",
        "question": "Why is the Saturated Adiabatic Lapse Rate (SALR) lower than the DALR?",
        "options": [
            "Because saturated air is heavier and rises slower",
            "Because latent heat of condensation is released into the rising parcel, counteracting cooling",
            "Because friction against water droplets generates mechanical heat",
            "Because saturated air absorbs more solar radiation"
        ],
        "answerIndex": 1,
        "explanation": "When saturated air rises, water vapour condenses, releasing latent heat (approx 2.5 x 10^6 J/kg). This latent heat offsets part of the adiabatic expansion cooling, reducing the lapse rate to SALR (~4°C to 7°C/km).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 9 'Stability & Instability', p. 86"
    },
    {
        "topic": "Stability & Adiabatics",
        "difficulty": "medium",
        "question": "Under what condition is an atmospheric layer classified as 'Conditionally Unstable'?",
        "options": [
            "When ELR > DALR",
            "When DALR > ELR > SALR",
            "When ELR < SALR",
            "When ELR is negative (Inversion)"
        ],
        "answerIndex": 1,
        "explanation": "Conditional Instability exists when the Environmental Lapse Rate (ELR) lies between DALR and SALR (DALR > ELR > SALR). The air is stable if unsaturated, but becomes unstable if lifted to saturation.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 9 'Stability & Instability', p. 87 & Q3"
    },
    {
        "topic": "Stability & Adiabatics",
        "difficulty": "hard",
        "question": "If surface temperature is +30°C and DALR prevails, what will be the temperature of a dry air parcel lifted to 2 km?",
        "options": ["+10.4°C", "+18.0°C", "+24.0°C", "+05.0°C"],
        "answerIndex": 0,
        "explanation": "Cooling = 2 km * 9.8°C/km = 19.6°C. Final temperature = 30°C - 19.6°C = +10.4°C (approx +10°C).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 9 'Stability & Instability', p. 91 & Q8"
    },
    {
        "topic": "Stability & Adiabatics",
        "difficulty": "medium",
        "question": "An atmospheric temperature inversion (temperature increasing with height) represents a state of:",
        "options": ["Extreme instability", "Extreme stability", "Neutral equilibrium", "Super-adiabatic convection"],
        "answerIndex": 1,
        "explanation": "In an inversion layer, warm air sits atop cooler, denser air. Any displaced parcel becomes colder than its surroundings and immediately sinks back, suppressing vertical motion and making the layer highly stable.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 9 'Stability & Instability', p. 86 & Q15"
    },

    # -------------------------------------------------------------
    # Topic 10: Optical Phenomena & Atmospheric Electricity
    # -------------------------------------------------------------
    {
        "topic": "Optical Phenomena",
        "difficulty": "easy",
        "question": "A primary rainbow is produced by which physical processes of sunlight in raindrops?",
        "options": [
            "Diffraction and single reflection",
            "Two refractions and one internal reflection",
            "Scattering only",
            "Polarization through ice crystals"
        ],
        "answerIndex": 1,
        "explanation": "A primary rainbow is formed when sunlight enters a raindrop (refraction), undergoes one total internal reflection at the back of the drop, and refracts again as it emerges (two refractions, one reflection), subtending an angle of 42°.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 10 'Optical Phenomena', p. 93"
    },
    {
        "topic": "Optical Phenomena",
        "difficulty": "medium",
        "question": "What is Saint Elmo's Fire?",
        "options": [
            "Ball lightning exploding in the passenger cabin",
            "A luminous bluish-green corona discharge on aircraft extremities caused by high atmospheric electrical fields in clouds",
            "A fiery meteor burning up in the mesosphere",
            "Exhaust flame visible from piston engine stacks at night"
        ],
        "answerIndex": 1,
        "explanation": "Saint Elmo's Fire is a luminous, brush-like electrical corona discharge appearing on wingtips, windshields, and nose cones when flying through clouds with strong static electric fields (CU, CB, or volcanic ash).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 10 'Optical Phenomena', p. 98"
    },
    {
        "topic": "Optical Phenomena",
        "difficulty": "medium",
        "question": "A Corona (colored rings closely encircling the sun or moon) is caused by:",
        "options": [
            "Refraction of light by ice crystals in cirrostratus",
            "Diffraction of light through tiny water droplets in altostratus or mist",
            "Atmospheric refraction through high temperature inversions",
            "Scattering of light by nitrogen molecules"
        ],
        "answerIndex": 1,
        "explanation": "Corona is produced by the diffraction of light by tiny water droplets (such as in Altostratus or thin Stratocumulus). The ring radius is less than 5°, with red on the outside and blue inside.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 10 'Optical Phenomena', p. 94 & Q10"
    },

    # -------------------------------------------------------------
    # Topic 11: Precipitation
    # -------------------------------------------------------------
    {
        "topic": "Precipitation",
        "difficulty": "easy",
        "question": "Precipitation consisting of very small, uniformly dispersed water droplets of diameter less than 0.5 mm that appear to float in air currents is termed:",
        "options": ["Rain (RA)", "Drizzle (DZ)", "Sleet", "Snow pellets (GS)"],
        "answerIndex": 1,
        "explanation": "Drizzle (DZ) is fairly uniform precipitation composed exclusively of fine water droplets with diameters between 0.1 mm and 0.5 mm, falling almost exclusively from Stratus (ST) clouds.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 11 'Precipitation', p. 100"
    },
    {
        "topic": "Precipitation",
        "difficulty": "medium",
        "question": "The Bergeron-Findeisen ice crystal precipitation theory relies on the fundamental physical fact that:",
        "options": [
            "Saturation vapour pressure over water is greater than that over ice at the same sub-zero temperature",
            "Ice crystals fall much faster than large raindrops",
            "Supercooled water freezes instantly whenever air is unsaturated",
            "Ice crystals cannot exist above -40°C"
        ],
        "answerIndex": 0,
        "explanation": "At temperatures between 0°C and -40°C, supercooled water and ice coexist. The saturation vapour pressure over water is higher than over ice. Water vapour evaporates from supercooled droplets and sublimates directly onto ice crystals, causing rapid crystal growth.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 11 'Precipitation', p. 100 & Q1"
    },
    {
        "topic": "Precipitation",
        "difficulty": "medium",
        "question": "What is 'Sleet' officially defined as?",
        "options": [
            "A mixture of rain and snow or melting snow pellets",
            "Hard spherical stones of clear ice > 5 mm diameter",
            "Dry snow blowing across an aerodrome",
            "A dense concentration of fog water droplets"
        ],
        "answerIndex": 0,
        "explanation": "In aviation meteorology (UK/ICAO practice followed by DGCA), Sleet is a mixture of rain and snow, or partially melted snow flakes falling to the ground.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 11 'Precipitation', p. 102 & Q9"
    },

    # -------------------------------------------------------------
    # Topic 12: Ice Accretion
    # -------------------------------------------------------------
    {
        "topic": "Ice Accretion",
        "difficulty": "easy",
        "question": "What are the two main requirements for the formation of structural aircraft airframe icing in flight?",
        "options": [
            "Sub-zero airframe temperature and the presence of visible supercooled liquid water droplets",
            "Flight in clear air above 30,000 ft with OAT below -40°C",
            "Cruising in cirrus clouds with pitot heat on",
            "High humidity in cloudless skies at +15°C"
        ],
        "answerIndex": 0,
        "explanation": "Structural icing occurs when an aircraft flies through visible liquid moisture (clouds or freezing rain) where water droplets are supercooled below 0°C, and the airframe surface temperature is at or below 0°C.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 12 'Ice Accretion', p. 105"
    },
    {
        "topic": "Ice Accretion",
        "difficulty": "medium",
        "question": "Clear (Glaze) ice forms primarily in which clouds and temperature range?",
        "options": [
            "Layer stratiform clouds at temperatures below -20°C",
            "Cumuliform clouds (CU, CB) with large supercooled water droplets between 0°C and -10°C",
            "High cirrus clouds at -50°C",
            "Thin fog layers at -25°C"
        ],
        "answerIndex": 1,
        "explanation": "Clear ice forms when large supercooled water droplets impact the airframe. The slow freezing allows the water to spread out before freezing solid, creating a smooth, transparent, tenacious coating of ice. It is most hazardous between 0°C and -10°C in convective clouds.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 12 'Ice Accretion', p. 106 & Q5"
    },
    {
        "topic": "Ice Accretion",
        "difficulty": "medium",
        "question": "Why is Rime ice typically less dangerous aerodynamically than Clear (Glaze) ice?",
        "options": [
            "It melts instantly upon touching the airframe",
            "It is granular, porous, brittle, traps air, and can be removed more easily by pneumatic de-icing boots",
            "It exclusively accumulates on the trailing edge of control surfaces",
            "It increases aircraft lift by smoothing surface imperfections"
        ],
        "answerIndex": 1,
        "explanation": "Rime ice forms when small supercooled droplets freeze instantly upon contact, trapping air to produce an opaque, white, porous, brittle structure. It has lower density and breaks off more easily than heavy, solid clear ice.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 12 'Ice Accretion', p. 105 & Q3/Q6"
    },
    {
        "topic": "Ice Accretion",
        "difficulty": "hard",
        "question": "What is the primary effect of severe structural ice accumulation on aircraft flight characteristics?",
        "options": [
            "Decreases stalling speed and increases rate of climb",
            "Increases stalling speed significantly, decreases lift, and drastically increases aerodynamic drag",
            "Decreases fuel consumption and improves altimeter accuracy",
            "Increases propeller efficiency due to weight distribution"
        ],
        "answerIndex": 1,
        "explanation": "Ice spoils the aerodynamic camber of wings, causing premature boundary layer separation. This drastically reduces maximum lift coefficient (CL_max), elevates stalling speed by up to 15-20 knots, and increases parasite drag exponentially.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 12 'Ice Accretion', p. 107 & Q20"
    },
    {
        "topic": "Ice Accretion",
        "difficulty": "medium",
        "question": "In what cloud type are flights virtually free from structural airframe icing hazard?",
        "options": ["Cirrus (CI) and Cirrostratus (CS)", "Altocumulus (AC)", "Cumulus congestus (TCU)", "Stratus (ST)"],
        "answerIndex": 0,
        "explanation": "Cirrus, Cirrostratus, and Cirrocumulus clouds are composed almost entirely of dry ice crystals rather than supercooled liquid water droplets. Ice crystals do not stick to cold airframes, posing negligible icing hazard.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 12 'Ice Accretion', p. 106 & Q8"
    },

    # -------------------------------------------------------------
    # Topic 13: Thunderstorms
    # -------------------------------------------------------------
    {
        "topic": "Thunderstorms",
        "difficulty": "easy",
        "question": "What are the three essential conditions required for the development of a thunderstorm?",
        "options": [
            "High atmospheric pressure, strong westerly winds, and dry air",
            "Steep environmental lapse rate (instability), abundant moisture supply, and a trigger action (lifting mechanism)",
            "Strong temperature inversion, clear skies, and calm winds",
            "High density altitude, stratus clouds, and low freezing level"
        ],
        "answerIndex": 1,
        "explanation": "A thunderstorm requires three ingredients: atmospheric instability (steep lapse rate through 5-6 km), adequate moisture in the lower levels, and a trigger action (insolation, orographic lift, frontal convergence, or convergence).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 13 'Thunderstorm', p. 112 & Q1"
    },
    {
        "topic": "Thunderstorms",
        "difficulty": "easy",
        "question": "The beginning of the 'Mature' stage of a thunderstorm cell is marked by:",
        "options": [
            "The first updraft reaching 10,000 ft",
            "The onset of precipitation at the surface and arrival of the downdraft",
            "The complete disappearance of all lightning",
            "The formation of an anvil top"
        ],
        "answerIndex": 1,
        "explanation": "The mature stage begins when falling rain or hail reaches the ground, creating a powerful friction-driven cold downdraft that coexists with the vigorous convective updrafts.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 13 'Thunderstorm', p. 113 & Q5"
    },
    {
        "topic": "Thunderstorms",
        "difficulty": "medium",
        "question": "What is a 'Microburst'?",
        "options": [
            "A small tornado less than 50 metres in diameter",
            "An intense localized downdraft with horizontal outflow diameter < 4 km and winds that can exceed 90 km/h (50 kt)",
            "A minor gust lasting under 5 seconds",
            "A thermal bubble created over an asphalt runway"
        ],
        "answerIndex": 1,
        "explanation": "A microburst is a violent localized downdraft with horizontal dimensions less than 4 km, lasting 15-20 minutes, with downdrafts up to 75 km/h and outflow winds exceeding 90 to 200 km/h, posing fatal wind-shear hazards on approach/takeoff.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 13 'Thunderstorm', p. 117 & Q20"
    },
    {
        "topic": "Thunderstorms",
        "difficulty": "hard",
        "question": "Severe pre-monsoon thunderstorms affecting West Bengal, Bihar, and Assam during March to May are known locally as:",
        "options": ["Western Disturbances", "Norwesters (Kalbaishakhi)", "Andhi", "Loo"],
        "answerIndex": 1,
        "explanation": "Norwesters (Kalbaishakhi) are violent pre-monsoon convective squall lines originating over Chota Nagpur plateau and advancing from the northwest across West Bengal, Bihar, and Assam, accompanied by damaging winds, hail, and squalls.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 13 'Thunderstorm', p. 120 & Q3/Q12"
    },
    {
        "topic": "Thunderstorms",
        "difficulty": "hard",
        "question": "When penetrating a thunderstorm, why is hail hazardous even in cloud-free air outside the active cloud core?",
        "options": [
            "Hail only falls in clear air",
            "Upper-level updrafts toss large hailstones out of the top of the cloud, which then fall through clear air under or around the anvil",
            "Hail generates magnetic interference that disrupts VHF communications",
            "Hail is invisible on all weather radars"
        ],
        "answerIndex": 1,
        "explanation": "Violent updrafts in supercell storms eject hailstones out of the cloud top or overhang, causing hail to fall in clear air up to 10 to 20 km downstream from the storm core, often underneath the spreading anvil.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 13 'Thunderstorm', p. 116 & p. 122 Q20"
    },

    # -------------------------------------------------------------
    # Topic 14: Air Masses, Fronts & Western Disturbances
    # -------------------------------------------------------------
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "easy",
        "question": "A front where cold air is actively displacing and undercutting warm air is called a:",
        "options": ["Warm front", "Cold front", "Stationary front", "Warm occlusion"],
        "answerIndex": 1,
        "explanation": "A Cold Front is the boundary zone where an advancing colder, denser air mass displaces a warmer air mass by wedging underneath it.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts', p. 128"
    },
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "medium",
        "question": "What is the typical average slope of a cold front compared to a warm front?",
        "options": [
            "Cold front is much steeper (approx 1:50 to 1:80) than a warm front (approx 1:150 to 1:200)",
            "Warm front is much steeper (1:20) than a cold front (1:300)",
            "Both fronts have identical slopes of 1:100",
            "Cold fronts are completely horizontal"
        ],
        "answerIndex": 0,
        "explanation": "Because of surface friction retarding the cold air near the ground, the cold front boundary bulges forward with a steep slope (1:50 to 1:80). In contrast, warm fronts have very gentle slopes (1:150 to 1:200).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts', p. 128-129"
    },
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "medium",
        "question": "As an active cold front passes an airfield in the Northern Hemisphere, the surface wind typically:",
        "options": [
            "Backs and decreases in speed",
            "Veers abruptly (e.g., from SW to NW) and becomes strong and squally with sudden temperature drop",
            "Remains completely steady from the South",
            "Becomes calm for several days"
        ],
        "answerIndex": 1,
        "explanation": "Upon the passage of a cold front in the Northern Hemisphere, the wind veers sharply (clockwise, e.g. from SWly to NWly), gusty squalls occur, barometric pressure rises abruptly, and temperature drops sharply.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts', p. 134 & Q21"
    },
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "hard",
        "question": "What are Western Disturbances (WDs) that affect northern and northwest India during the winter months?",
        "options": [
            "Tropical depressions originating in the South Indian Ocean",
            "Extra-tropical shallow depressions or upper westerly troughs originating over the Mediterranean/Caspian region that travel eastward",
            "Cold downdrafts descending from the Tibetan plateau",
            "Monsoon low pressure systems moving from east to west"
        ],
        "answerIndex": 1,
        "explanation": "Western Disturbances are extra-tropical low pressure systems/troughs in the upper westerlies originating over the Mediterranean Sea, Black Sea, or Caspian Sea that move eastwards across Pakistan and northern India, bringing winter rain, snow, and subsequent cold waves.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts', p. 132 & Q29"
    },
    {
        "topic": "Air Masses & Fronts",
        "difficulty": "medium",
        "question": "Frontogenesis is defined in meteorology as the:",
        "options": [
            "Decay and dissipation of a frontal weather boundary",
            "Formation, generation, or intensification of a frontal zone",
            "Movement of fronts across the equator",
            "Freezing of rain droplets in a warm front"
        ],
        "answerIndex": 1,
        "explanation": "Frontogenesis is the meteorological process by which horizontal temperature/density gradients tighten, leading to the creation or intensification of a weather front. The opposite process is Frontolysis.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Air Masses Fronts', p. 128"
    },

    # -------------------------------------------------------------
    # Topic 15: Jet Streams
    # -------------------------------------------------------------
    {
        "topic": "Jet Streams",
        "difficulty": "easy",
        "question": "According to the World Meteorological Organization (WMO), what is the minimum core wind speed required to classify an upper-air wind current as a Jet Stream?",
        "options": ["40 knots", "60 knots (approx 30 m/s)", "100 knots", "150 knots"],
        "answerIndex": 1,
        "explanation": "WMO defines a jet stream as a strong, narrow current of wind concentrated along a quasi-horizontal axis in the upper troposphere or stratosphere characterized by strong vertical and lateral wind shears, with minimum core speed of 60 kt (30 m/s).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 15 'Jet Streams', p. 136 & Q1"
    },
    {
        "topic": "Jet Streams",
        "difficulty": "medium",
        "question": "During the winter season, the Sub-Tropical Westerly Jet Stream (STJ) over northern India is typically located at an altitude of:",
        "options": ["6 km (FL200)", "9 km (FL300)", "12 km (FL390, ~200 hPa) near 27°N", "18 km (FL600) near the Equator"],
        "answerIndex": 2,
        "explanation": "The Sub-Tropical Westerly Jet Stream (STJ) prevails over northern India from October to May. In winter, its core is located at roughly 12 km (approx FL390 / 200 hPa level) near 27°N with core speeds commonly reaching 100 to 150 knots.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 15 'Jet Streams', p. 137 & Q10"
    },
    {
        "topic": "Jet Streams",
        "difficulty": "hard",
        "question": "The Tropical Easterly Jet Stream (TEJ) over peninsular India is prominent during which season?",
        "options": [
            "Winter (January to February)",
            "Pre-monsoon (March to May)",
            "Southwest Monsoon (June to August) near latitude 13°N at 15 km altitude",
            "Post-monsoon (October to November)"
        ],
        "answerIndex": 2,
        "explanation": "The Tropical Easterly Jet Stream (TEJ) establishes over southern/peninsular India (near 13°N, Chennai latitude) during the southwest monsoon season (June to August) at an altitude of 15 to 16 km (FL500 / 100 hPa level) with speeds around 60 to 100 kt.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 15 'Jet Streams', p. 139 & Q17/Q18"
    },
    {
        "topic": "Jet Streams",
        "difficulty": "medium",
        "question": "On which side of a westerly jet stream core in the Northern Hemisphere is the horizontal wind shear and Clear Air Turbulence (CAT) typically strongest?",
        "options": [
            "On the southern (warm/anticyclonic) side",
            "On the northern (colder/cyclonic) side, just below the tropopause",
            "Directly in the exact geometric center of the core",
            "There is never any shear around a jet stream"
        ],
        "answerIndex": 1,
        "explanation": "The cyclonic (northern/poleward) side of a westerly jet stream core exhibits significantly tighter horizontal wind shear (often ~100 kt per 100 NM) than the anticyclonic side (~35 kt per 100 NM), generating the most severe CAT.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 15 'Jet Streams', p. 139 & Chapter 16 p. 143"
    },

    # -------------------------------------------------------------
    # Topic 16: Clear Air Turbulence (CAT)
    # -------------------------------------------------------------
    {
        "topic": "Clear Air Turbulence",
        "difficulty": "easy",
        "question": "Clear Air Turbulence (CAT) is turbulence encountered by aircraft at high altitudes in:",
        "options": [
            "Severe thunderstorms with hail",
            "Cloud-free airspace or thin stratiform haze above 18,000 ft",
            "Low-level sea breezes below 2,000 ft",
            "Heavy monsoon rain showers"
        ],
        "answerIndex": 1,
        "explanation": "CAT is defined as bumpiness experienced by aircraft at high altitudes (typically above 18,000 ft / FL180) in cloud-free conditions or in stratiform cloud layers, generated primarily by strong vertical and horizontal wind shears near jet streams.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 16 'Clear Air Turbulence', p. 143 & Q9"
    },
    {
        "topic": "Clear Air Turbulence",
        "difficulty": "medium",
        "question": "What is the recommended pilot action when encountering severe Clear Air Turbulence in flight?",
        "options": [
            "Accelerate immediately to maximum operating speed (Vmo)",
            "Disengage altitude hold, establish recommended turbulence penetration airspeed (Vb), and initiate a climb or descent to change flight level",
            "Extend full flaps and lower landing gear",
            "Execute a steep 60° bank turn immediately"
        ],
        "answerIndex": 1,
        "explanation": "When entering severe CAT, pilots should reduce airspeed to the certified turbulence penetration speed (Vb / Va) to protect structural limits, disengage altitude hold to allow gentle altitude excursions, and request a change in flight level to exit the shear zone.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 16 'Clear Air Turbulence', p. 144"
    },
    {
        "topic": "Clear Air Turbulence",
        "difficulty": "hard",
        "question": "Which combination of factors provides the most reliable indication of impending CAT near a jet stream?",
        "options": [
            "Sudden outside air temperature (OAT) change of > 1°C per minute with vertical wind shear exceeding 6 kt per 1,000 ft",
            "A sudden decrease in pressure altitude of 5,000 ft",
            "Complete absence of cirrus streaks on weather satellite imagery",
            "Uniform barometric pressure over 500 NM"
        ],
        "answerIndex": 0,
        "explanation": "Rapid horizontal temperature changes (>1°C per minute at cruise) indicate crossing a strong frontal/baroclinic boundary near the jet core. When coupled with vertical wind shear > 6 kt/1,000 ft or horizontal shear > 20 kt/50 NM, severe CAT is probable.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 16 'Clear Air Turbulence', p. 143"
    },

    # -------------------------------------------------------------
    # Topic 17: Mountain Waves
    # -------------------------------------------------------------
    {
        "topic": "Mountain Waves",
        "difficulty": "easy",
        "question": "Which cloud type provides the classic visual signature of standing lee waves over and downwind of a mountain range?",
        "options": [
            "Altocumulus lenticularis (lens-shaped clouds)",
            "Cumulonimbus capillatus",
            "Nimbostratus fractus",
            "Cirrostratus nebulosus"
        ],
        "answerIndex": 0,
        "explanation": "Standing mountain waves produce Altocumulus lenticularis (lens-shaped or almond-shaped clouds) at the crests of the waves downwind of the mountain ridge, remaining quasi-stationary despite strong through-flowing winds.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 17 'Mountain Waves', p. 146"
    },
    {
        "topic": "Mountain Waves",
        "difficulty": "medium",
        "question": "What wind speed and directional alignment are required across a mountain ridge to initiate well-developed mountain waves?",
        "options": [
            "Wind parallel to the ridge at 5 knots",
            "Wind blowing within 30° of perpendicular to the ridge with a speed of at least 15 to 25 knots, increasing with altitude",
            "Variable light winds under 10 knots",
            "A descending katabatic wind at midnight"
        ],
        "answerIndex": 1,
        "explanation": "Mountain waves require: a wind direction within 30° of normal (perpendicular) to the mountain ridge line, wind speed of at least 15-20 kt across the ridge, wind speed increasing with altitude, and a stable layer near the ridge crest.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 17 'Mountain Waves', p. 145 & Q1/Q2"
    },
    {
        "topic": "Mountain Waves",
        "difficulty": "hard",
        "question": "Where does the most violent and hazardous turbulence occur in a mountain wave system?",
        "options": [
            "At the top of the lenticular cloud at 30,000 ft",
            "In the Rotor Zone (roll clouds) formed beneath the crest of the primary lee wave on the downwind side",
            "On the windward upwind slope in smooth laminar flow",
            "In the stratosphere directly above the mountain crest"
        ],
        "answerIndex": 1,
        "explanation": "The Rotor Zone forms in the lower levels beneath the crests of the lee waves. It contains violent turbulent eddies with severe vertical gusts and accelerations of up to 4g, capable of causing aircraft loss of control or structural failure.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 17 'Mountain Waves', p. 146 & Q6/Q10"
    },
    {
        "topic": "Mountain Waves",
        "difficulty": "medium",
        "question": "How do mountain waves affect an aircraft's barometric altimeter readings?",
        "options": [
            "Altimeter always underreads by exactly 500 ft",
            "Rapid vertical accelerations and localized pressure drops in the lee wave trough can cause the altimeter to overread by up to 1,000 ft (actual terrain clearance is less than indicated)",
            "Barometric altimeter reads zero when crossing the ridge",
            "Altimeters are unaffected by mountain waves"
        ],
        "answerIndex": 1,
        "explanation": "High winds across the ridge and hydrodynamic pressure reduction in the lee wave trough lower local atmospheric pressure. The altimeter overreads (indicates higher than actual true altitude), which dangerously reduces terrain clearance.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 17 'Mountain Waves', p. 147"
    },

    # -------------------------------------------------------------
    # Topic 18: Tropical Systems & Monsoon
    # -------------------------------------------------------------
    {
        "topic": "Tropical Systems & Monsoon",
        "difficulty": "easy",
        "question": "The Inter-Tropical Convergence Zone (ITCZ) is formed by the convergence of:",
        "options": [
            "Polar easterlies and mid-latitude westerlies",
            "Northeast trade winds of the Northern Hemisphere and Southeast trade winds of the Southern Hemisphere",
            "Sub-tropical jet streams with polar jet streams",
            "Land breezes with sea breezes"
        ],
        "answerIndex": 1,
        "explanation": "The ITCZ is the equatorial trough of low pressure where the trade winds of the two hemispheres (NE trades from the north and SE trades from the south) converge, causing widespread convective cloudiness and heavy showers.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Tropical Systems', p. 150 & Q15"
    },
    {
        "topic": "Tropical Systems & Monsoon",
        "difficulty": "easy",
        "question": "What is the minimum sea surface temperature required for the genesis of a Tropical Cyclone?",
        "options": ["+15°C", "+21°C", "+26.5°C to +27°C", "+35°C"],
        "answerIndex": 2,
        "explanation": "Tropical cyclogenesis requires an expansive warm ocean surface with sea temperatures of at least 26.5°C to 27°C to a depth of roughly 60 metres, providing abundant latent heat energy through evaporation.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Tropical Systems', p. 156 & Q31"
    },
    {
        "topic": "Tropical Systems & Monsoon",
        "difficulty": "medium",
        "question": "What are the primary meteorological characteristics of the 'Eye' of a mature tropical cyclone?",
        "options": [
            "Violent hurricane force squalls, dark clouds, and torrential rains",
            "Relatively calm or light winds, subsiding air, little or no cloudiness, and lowest surface barometric pressure",
            "Massive cumulonimbus towers with severe icing throughout",
            "Continuous tornadoes touching down"
        ],
        "answerIndex": 1,
        "explanation": "The eye is a central circular region (typically 20-50 km diameter) characterized by calm or light winds, clearing skies due to subsiding air (which warms adiabatically), and the lowest barometric pressure of the entire system.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Tropical Systems', p. 157 & Q3"
    },
    {
        "topic": "Tropical Systems & Monsoon",
        "difficulty": "hard",
        "question": "Under India Meteorological Department (IMD) classification, a low pressure system is designated as a 'Cyclonic Storm' when sustained surface winds are:",
        "options": ["17 to 27 knots", "28 to 33 knots", "34 to 47 knots (62 to 88 km/h)", "48 to 63 knots"],
        "answerIndex": 2,
        "explanation": "IMD classification: Low Pressure (<17 kt), Depression (17-27 kt), Deep Depression (28-33 kt), Cyclonic Storm (34-47 kt), Severe Cyclonic Storm (48-63 kt), Very Severe Cyclonic Storm (64-119 kt), Super Cyclone (>=120 kt).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Tropical Systems', p. 154 (Table 18.1) & Q27"
    },
    {
        "topic": "Tropical Systems & Monsoon",
        "difficulty": "hard",
        "question": "In the Northern Hemisphere, which quadrant of a moving Tropical Cyclone is known as the 'Dangerous Semi-Circle'?",
        "options": [
            "The rear left quadrant",
            "The right-hand (forward and right) semi-circle in the direction of storm movement",
            "The rear right quadrant only",
            "The entire left semi-circle"
        ],
        "answerIndex": 1,
        "explanation": "In the Northern Hemisphere, the right-hand semi-circle is dangerous because the forward motion of the cyclone adds to the rotational wind speed, resulting in the highest sustained winds, and the winds tend to blow an aircraft/vessel into the path of the storm center.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Tropical Systems', p. 157 & p. 159"
    },

    # -------------------------------------------------------------
    # Topic 19: Climatology of India & Meteorological Codes
    # -------------------------------------------------------------
    {
        "topic": "Climatology of India",
        "difficulty": "easy",
        "question": "The normal onset date of the Southwest Monsoon over the mainland of India (Kerala coast) is:",
        "options": ["15th May", "01st June", "15th June", "01st July"],
        "answerIndex": 1,
        "explanation": "The official climatological normal date for the arrival of the southwest monsoon over mainland India (Kerala) is 1st June (reaching South Andaman Sea earlier around 20th May).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 19 'Climatology of India', p. 171 & Q7"
    },
    {
        "topic": "Climatology of India",
        "difficulty": "medium",
        "question": "During a 'Break Monsoon' period in India, what happens to the distribution of rainfall?",
        "options": [
            "Heavy rain covers all of Rajasthan and Gujarat",
            "Rainfall ceases over most of central and peninsular India, while heavy to very heavy rain shifts to the Himalayan foothills and northeastern states",
            "Continuous rain falls over Mumbai and the Konkan coast exclusively",
            "Rainfall across the entire subcontinent drops to zero without exception"
        ],
        "answerIndex": 1,
        "explanation": "During a 'break', the monsoon trough shifts north close to the foot of the Himalayas. Central India experiences dry weather while catastrophic rainfall and floods occur over the Himalayan foothills, Bihar, UP, and northeast India.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 19 'Climatology of India', p. 172 & Q10/Q32"
    },
    {
        "topic": "Climatology of India",
        "difficulty": "medium",
        "question": "Which meteorological phenomenon is primarily responsible for winter precipitation and subsequent cold waves in Northwest India?",
        "options": ["Southwest Monsoon", "Western Disturbances (WDs)", "Tropical Easterly Jet", "Norwesters"],
        "answerIndex": 1,
        "explanation": "Western Disturbances (WDs) track across northwest India between December and March, generating rain in the plains of Punjab, Haryana, and Delhi, snow in J&K and Himachal, followed by dense radiation fog and cold wave incursions.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 19 'Climatology of India', p. 166 & Q4"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "easy",
        "question": "In a METAR report, what does the abbreviation 'CAVOK' indicate?",
        "options": [
            "Clear Air Turbulence observed in the vicinity",
            "Visibility 10 km or more, no clouds below 1,500 m (5,000 ft) or minimum sector altitude, no CB or TCU, and no significant weather",
            "Ceiling and visibility zero due to radiation fog",
            "Continuous thunderstorm activity at the airport"
        ],
        "answerIndex": 1,
        "explanation": "CAVOK (Ceiling And Visibility OK) replaces visibility, RVR, and cloud groups when: visibility is 10 km or more, no cloud below 1500 m (5000 ft) or minimum sector altitude (whichever is higher), no CB/TCU, and no significant weather.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 25 'METAR & SPECI Codes', p. 219 & Q34/Q36"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "medium",
        "question": "In an aerodrome forecast (TAF), what is the validity of a 'TREND' forecast appended to a METAR or SPECI?",
        "options": ["30 minutes", "1 hour", "2 hours", "6 hours"],
        "answerIndex": 2,
        "explanation": "A TREND landing forecast is valid for strictly 2 hours from the time of the METAR or SPECI report to which it is appended.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 25 'METAR & SPECI Codes', p. 223 & Q15"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "hard",
        "question": "In a METAR code, what does the report 'R27/P1500U' signify?",
        "options": [
            "Runway 27 RVR is less than 1500 metres and decreasing",
            "Runway 27 RVR is greater than 1500 metres and has shown an increasing tendency over the past 10 minutes",
            "Runway 27 is closed for pilot use above 1500 ft",
            "Pressure on runway 27 is 1500 hPa"
        ],
        "answerIndex": 1,
        "explanation": "In RVR reporting: 'R27' = Runway 27; 'P1500' = Greater than maximum measurable value (1500 m); 'U' = Upward (increasing) tendency in the past 10 minutes. ('D' = Downward, 'N' = No change).",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 25 'METAR & SPECI Codes', p. 221 & p. 225"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "medium",
        "question": "A SPECI (Aviation Selected Special Weather Report) is issued when:",
        "options": [
            "Routine observations are scheduled every hour",
            "Significant deterioration or improvement occurs in meteorological elements (e.g. wind, visibility, cloud ceiling, thunderstorm onset) between routine METARs",
            "An aircraft lands ahead of scheduled flight plan",
            "The sun crosses the local meridian"
        ],
        "answerIndex": 1,
        "explanation": "SPECI is a special weather report issued immediately when specified changes occur that are operationally significant to aircraft, such as wind direction change >= 60° with speed >= 10 kt, visibility passing thresholds (800, 1500, 3000, 5000 m), or onset of TS.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 25 'METAR & SPECI Codes', p. 220 & Q37"
    },
    {
        "topic": "Meteorological Services & Codes",
        "difficulty": "hard",
        "question": "What is a SIGMET message issued for?",
        "options": [
            "Routine 24-hour public forecast",
            "Severe en-route weather phenomena (such as active TS, severe turbulence, severe icing, volcanic ash, severe mountain waves) that may affect safety of aircraft operations",
            "Notifying changes in airport landing fee schedules",
            "Reporting calm wind conditions in the terminal area"
        ],
        "answerIndex": 1,
        "explanation": "SIGMET messages are issued by Meteorological Watch Offices (MWOs) to advise pilots of the occurrence or expected occurrence of specified en-route weather phenomena which may affect the safety of aircraft operations.",
        "source": "I.C. Joshi Aviation Meteorology, Chapter 21 'Met Services', p. 192 & Q18/Q20"
    }
]

def main():
    print(f"Total new candidate questions loaded: {len(METEOROLOGY_EXPANSION_BANK)}")

if __name__ == "__main__":
    main()

