# -*- coding: utf-8 -*-
"""
High-quality, verified question sets for Aviation Meteorology, Technical General,
Technical Specific, and RTR based strictly on DGCA CPL official syllabi,
I.C. Joshi Aviation Meteorology, Oxford ATPL Aircraft General Knowledge / PoF,
Cessna 172 / Light Twin POH standards, and ICAO Doc 9432 / Doc 8400 / WPC RTR(A).
"""

MET_NEW_QUESTIONS = [
  # The Atmosphere
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
    "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'The Atmosphere'"
  },
  {
    "topic": "The Atmosphere",
    "difficulty": "medium",
    "question": "What is the standard ISA temperature lapse rate in the troposphere up to 11 km (36,090 ft)?",
    "options": [
      "1.0°C per 1,000 ft (3.0°C/km)",
      "1.98°C per 1,000 ft (6.5°C/km)",
      "3.0°C per 1,000 ft (9.8°C/km)",
      "0.5°C per 1,000 ft (1.5°C/km)"
    ],
    "answerIndex": 1,
    "explanation": "In the standard troposphere, temperature decreases uniformly with altitude at a rate of 1.98°C per 1,000 ft (approximately 6.5°C per kilometre) up to the standard tropopause at 11,000 m (36,090 ft), where it remains constant at -56.5°C.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'The Atmosphere'"
  },
  {
    "topic": "The Atmosphere",
    "difficulty": "hard",
    "question": "Why is the average tropopause altitude higher and colder over the Equator than over the Poles?",
    "options": [
      "Due to greater rotational centrifugal force pushing cold air upward at the poles",
      "Because strong solar heating causes deep vertical convective overturning in the tropics, lifting the tropopause to ~16-18 km (-75°C to -80°C)",
      "Because the ozone layer is situated lowest at the equator",
      "Due to descending polar easterly wind currents cooling the upper stratosphere"
    ],
    "answerIndex": 1,
    "explanation": "Intense thermal convection in equatorial and tropical regions pushes the tropopause up to 16-18 km (FL500-600) where temperatures drop to -75°C to -85°C. At the poles, where convective lifting is minimal, the tropopause sits at only 8-10 km with temperatures around -45°C to -50°C.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 1 'The Atmosphere'"
  },

  # Atmospheric Pressure
  {
    "topic": "Atmospheric Pressure",
    "difficulty": "easy",
    "question": "When an aircraft altimeter subscale is set to QNH, the altimeter indicates:",
    "options": [
      "Height above the aerodrome elevation",
      "Altitude above Mean Sea Level (MSL)",
      "Pressure altitude relative to the 1013.25 hPa datum",
      "True height above the instantaneous ground level (AGL)"
    ],
    "answerIndex": 1,
    "explanation": "QNH is the altimeter subscale setting obtained by reducing station pressure to mean sea level using ISA temperature lapse rates. Setting QNH causes the altimeter to read altitude above Mean Sea Level (MSL), reading aerodrome elevation when on the runway.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure'"
  },
  {
    "topic": "Atmospheric Pressure",
    "difficulty": "medium",
    "question": "An aircraft flies from a region of high atmospheric pressure to an area of low atmospheric pressure without resetting its altimeter. The altimeter will:",
    "options": [
      "Overread (indicate higher than actual true altitude)",
      "Underread (indicate lower than actual true altitude)",
      "Indicate true altitude accurately regardless of pressure changes",
      "Remain unchanged while true airspeed decreases by 10%"
    ],
    "answerIndex": 0,
    "explanation": "Flying 'high to low' pressure without adjusting the subscale causes the aircraft to descend along the sloping isobaric surface. The altimeter continues sensing the same pressure and indicates the assigned altitude, meaning the altimeter is overreading (actual true altitude is lower: 'High to low, look out below').",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure'"
  },
  {
    "topic": "Atmospheric Pressure",
    "difficulty": "medium",
    "question": "What is the approximate vertical pressure gradient in the lower atmosphere near sea level?",
    "options": [
      "1 hPa per 30 feet (27-30 ft/hPa)",
      "1 hPa per 100 feet",
      "1 hPa per 10 feet",
      "1 hPa per 500 feet"
    ],
    "answerIndex": 0,
    "explanation": "In the lower levels of the atmosphere near sea level, 1 hPa (or 1 millibar) corresponds to approximately 27 to 30 feet (typically taken as 30 ft/hPa in standard DGCA computations). As altitude increases and air density drops, the vertical distance per hPa increases.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure'"
  },
  {
    "topic": "Atmospheric Pressure",
    "difficulty": "hard",
    "question": "An aircraft cruises at FL100 (subscale 1013.25 hPa) with an outside air temperature of -25°C. ISA temperature at FL100 is -5°C. What is the aircraft's approximate true altitude?",
    "options": [
      "10,800 ft",
      "9,200 ft",
      "10,000 ft",
      "8,400 ft"
    ],
    "answerIndex": 1,
    "explanation": "Temperature deviation is -25°C - (-5°C) = -20°C (ISA -20). The rule of thumb for temperature error is 4 feet per 1,000 feet per °C deviation. Height = 10,000 ft, so error = 4 * 10 * (-20) = -800 ft. True altitude = 10,000 - 800 = 9,200 ft. In cold air, true altitude is lower than indicated ('Cold air, beware').",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 2 'Atmospheric Pressure'"
  },

  # Temperature & Heat
  {
    "topic": "Temperature & Heat",
    "difficulty": "easy",
    "question": "A surface temperature inversion is characterized by:",
    "options": [
      "Temperature increasing with altitude rather than decreasing",
      "Temperature dropping at more than the dry adiabatic lapse rate",
      "Constant temperature up to 10,000 ft",
      "Rapid formation of deep cumulus and cumulonimbus clouds"
    ],
    "answerIndex": 0,
    "explanation": "A temperature inversion is an atmospheric condition where temperature increases with increasing altitude, inverting the normal tropospheric environmental lapse rate. It creates extremely stable conditions and traps pollutants, haze, or fog near the surface.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature & Heat'"
  },
  {
    "topic": "Temperature & Heat",
    "difficulty": "medium",
    "question": "At what time of day does the minimum surface air temperature typically occur under clear skies?",
    "options": [
      "At midnight",
      "Shortly after sunrise",
      "Two hours before sunrise",
      "At 03:00 hours local time"
    ],
    "answerIndex": 1,
    "explanation": "The minimum surface air temperature occurs shortly after sunrise (approximately 15 to 30 minutes post-sunrise) because terrestrial radiation continues to exceed incoming solar radiation until the sun rises high enough to balance heat loss.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature & Heat'"
  },
  {
    "topic": "Temperature & Heat",
    "difficulty": "hard",
    "question": "Which mechanism is primarily responsible for transferring heat from the Earth's surface through the first few millimetres of the atmosphere?",
    "options": [
      "Conduction",
      "Convection",
      "Advection",
      "Latent heat release"
    ],
    "answerIndex": 0,
    "explanation": "Conduction transfers heat between the physical ground surface and the very thin microscopic boundary layer of air in direct molecular contact with it. Beyond this contact layer, convection and turbulent mixing take over as the dominant upward heat transfer mechanisms.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature & Heat'"
  },

  # Air Density
  {
    "topic": "Air Density",
    "difficulty": "easy",
    "question": "How does an increase in ambient temperature affect air density and aircraft takeoff performance?",
    "options": [
      "Density decreases; takeoff run increases and climb rate decreases",
      "Density increases; takeoff run shortens and climb performance improves",
      "Density increases; true airspeed becomes lower for the same indicated airspeed",
      "Density remains unchanged because pressure compensates for temperature"
    ],
    "answerIndex": 0,
    "explanation": "Warm air expands and becomes less dense. Lower air density reduces aerodynamic lift, engine thrust/power, and propeller efficiency, resulting in a longer takeoff ground roll and a lower rate of climb.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 4 'Air Density'"
  },
  {
    "topic": "Air Density",
    "difficulty": "medium",
    "question": "Density altitude is defined as:",
    "options": [
      "Pressure altitude corrected for non-standard temperature",
      "Indicated altitude corrected for instrument and position error",
      "True altitude corrected for terrain elevation",
      "The altitude indicated when subscale is set to 1013.25 hPa"
    ],
    "answerIndex": 0,
    "explanation": "Density altitude is pressure altitude corrected for variations from standard temperature. It represents the altitude in the standard atmosphere at which the air density equals the existing ambient density.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 4 'Air Density'"
  },
  {
    "topic": "Air Density",
    "difficulty": "hard",
    "question": "Given an airfield elevation of 3,000 ft, QNH 1003 hPa, and ambient temperature of +35°C, what is the approximate density altitude? (Take ISA at sea level = +15°C)",
    "options": [
      "Approximately 6,200 ft",
      "Approximately 3,300 ft",
      "Approximately 4,500 ft",
      "Approximately 8,100 ft"
    ],
    "answerIndex": 0,
    "explanation": "1) Pressure altitude = Elevation + (1013 - QNH) * 30 = 3000 + (10) * 30 = 3300 ft. 2) ISA temp at 3300 ft = 15 - (3.3 * 2) = +8.4°C. 3) Temp deviation = +35°C - 8.4°C = +26.6°C. 4) Density altitude = Pressure Alt + (118 * temp dev) = 3300 + (118 * 26.6) = 3300 + 3138 ≈ 6,438 ft (approx 6,200 - 6,500 ft).",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 4 'Air Density'"
  },

  # Humidity
  {
    "topic": "Humidity",
    "difficulty": "easy",
    "question": "The temperature to which moist air must be cooled at constant pressure to become saturated is called:",
    "options": [
      "Dew point temperature",
      "Wet bulb potential temperature",
      "Virtual temperature",
      "Condensation point"
    ],
    "answerIndex": 0,
    "explanation": "Dew point is the temperature to which unsaturated air must be cooled at constant pressure and water vapor content in order to reach saturation (100% relative humidity).",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 5 'Humidity'"
  },
  {
    "topic": "Humidity",
    "difficulty": "medium",
    "question": "As ambient air temperature rises during the afternoon while moisture content remains constant, relative humidity will:",
    "options": [
      "Decrease",
      "Increase",
      "Remain unchanged",
      "Reach 100% automatically"
    ],
    "answerIndex": 0,
    "explanation": "Relative humidity is the ratio of actual water vapor pressure to the saturation vapor pressure. As temperature rises, saturation vapor pressure increases exponentially, meaning the air can hold more water vapor; thus relative humidity decreases.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 5 'Humidity'"
  },

  # Stability & Adiabatics
  {
    "topic": "Stability & Adiabatics",
    "difficulty": "easy",
    "question": "The Dry Adiabatic Lapse Rate (DALR) of an unsaturated parcel of air is approximately:",
    "options": [
      "3.0°C per 1,000 ft (9.8°C/km)",
      "1.5°C per 1,000 ft (5.0°C/km)",
      "1.98°C per 1,000 ft (6.5°C/km)",
      "0.5°C per 1,000 ft (1.8°C/km)"
    ],
    "answerIndex": 0,
    "explanation": "The Dry Adiabatic Lapse Rate (DALR) is constant at approximately 3.0°C per 1,000 ft (or 9.8°C per kilometre / ~1°C per 100 metres) for any dry or unsaturated rising or sinking parcel of air.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Stability & Adiabatics'"
  },
  {
    "topic": "Stability & Adiabatics",
    "difficulty": "medium",
    "question": "Why is the Saturated Adiabatic Lapse Rate (SALR) always less than the Dry Adiabatic Lapse Rate (DALR)?",
    "options": [
      "Latent heat of condensation is released into the saturated parcel as water vapor condenses, counteracting adiabatic cooling",
      "Water droplets absorb surrounding sensible heat during expansion",
      "Moist air has higher molecular weight than dry air",
      "Coriolis force retards upward vertical air motion"
    ],
    "answerIndex": 0,
    "explanation": "When saturated air rises, condensation occurs, releasing the latent heat of vaporization (approx 2.5 x 10^6 J/kg). This released heat warms the parcel, partially offsetting adiabatic expansion cooling and lowering the cooling rate (SALR ~1.5°C/1,000 ft near sea level).",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Stability & Adiabatics'"
  },
  {
    "topic": "Stability & Adiabatics",
    "difficulty": "hard",
    "question": "An environmental lapse rate (ELR) of 4.0°C per 1,000 ft indicates that the atmosphere is:",
    "options": [
      "Absolutely unstable",
      "Absolutely stable",
      "Conditionally unstable",
      "Neutrally stable for unsaturated air"
    ],
    "answerIndex": 0,
    "explanation": "DALR is 3°C/1000 ft and SALR is ~1.5°C/1000 ft. When the ELR (4.0°C/1000 ft) is greater than DALR, any displaced parcel (whether dry or saturated) will always be warmer and less dense than surrounding ambient air and will accelerate upward. This is absolute instability.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 6 'Stability & Adiabatics'"
  },

  # Clouds & Precipitation
  {
    "topic": "Clouds & Precipitation",
    "difficulty": "easy",
    "question": "Which cloud genus is classified as a high cloud with a mean base height above 20,000 ft (6,000 m)?",
    "options": [
      "Cirrus (Ci)",
      "Altocumulus (Ac)",
      "Stratocumulus (Sc)",
      "Nimbostratus (Ns)"
    ],
    "answerIndex": 0,
    "explanation": "High clouds (base above 20,000 ft / 6,000 m in temperate latitudes) include Cirrus (Ci), Cirrocumulus (Cc), and Cirrostratus (Cs), composed almost entirely of ice crystals.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 7 'Clouds & Precipitation'"
  },
  {
    "topic": "Clouds & Precipitation",
    "difficulty": "medium",
    "question": "Continuous, widespread, steady rain or snow falling from an extensive, dark, overcast layer is typical of which cloud genus?",
    "options": [
      "Nimbostratus (Ns)",
      "Cumulonimbus (Cb)",
      "Cirrocumulus (Cc)",
      "Altocumulus lenticularis (Ac len)"
    ],
    "answerIndex": 0,
    "explanation": "Nimbostratus produces continuous, steady precipitation that reaches the ground, characterized by a thick, dark grey, diffuse overcast layer without lightning or hail.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 7 'Clouds & Precipitation'"
  },
  {
    "topic": "Clouds & Precipitation",
    "difficulty": "hard",
    "question": "What is the physical difference between rain and drizzle?",
    "options": [
      "Drizzle consists of uniform water droplets with diameter less than 0.5 mm that appear to float, whereas raindrops exceed 0.5 mm",
      "Drizzle originates from cirrus clouds while rain originates from cumuliform clouds",
      "Drizzle only occurs when the surface temperature is below freezing",
      "Raindrops always freeze upon surface contact while drizzle remains liquid"
    ],
    "answerIndex": 0,
    "explanation": "By international WMO definition, drizzle consists of very small, numerous water droplets with diameters less than 0.5 mm falling almost exclusively from Stratus (St) clouds. Raindrops have diameters greater than 0.5 mm (up to ~6 mm max before aerodynamic breakup).",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 7 'Clouds & Precipitation'"
  },

  # Winds
  {
    "topic": "Winds",
    "difficulty": "easy",
    "question": "What is Buys Ballot's Law for an observer in the Northern Hemisphere?",
    "options": [
      "If you stand with your back to the wind, low pressure is on your left",
      "If you stand with your back to the wind, low pressure is on your right",
      "Wind blows directly from low pressure toward high pressure",
      "Coriolis force always acts to the left of the wind vector"
    ],
    "answerIndex": 0,
    "explanation": "Buys Ballot's Law states that in the Northern Hemisphere, if an observer stands with their back to the wind, the area of lower atmospheric pressure is on their left (and higher pressure on their right). In the Southern Hemisphere, the reverse is true.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 8 'Winds'"
  },
  {
    "topic": "Winds",
    "difficulty": "medium",
    "question": "The geostrophic wind is the theoretical wind resulting from an exact balance between which two forces?",
    "options": [
      "Horizontal Pressure Gradient Force and Coriolis Force",
      "Centrifugal Force and Gravity",
      "Surface Friction and Pressure Gradient Force",
      "Thermal buoyancy and Coriolis Force"
    ],
    "answerIndex": 0,
    "explanation": "The geostrophic wind represents straight, frictionless, steady horizontal flow where the horizontal Pressure Gradient Force (PGF) is exactly balanced by the Coriolis force.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 8 'Winds'"
  },
  {
    "topic": "Winds",
    "difficulty": "hard",
    "question": "In the Northern Hemisphere, how does the surface wind compare with the 2,000 ft geostrophic wind due to ground friction?",
    "options": [
      "Surface wind is backed (counter-clockwise) and has lower speed than 2,000 ft wind",
      "Surface wind is veered (clockwise) and has higher speed than 2,000 ft wind",
      "Surface wind blows parallel to isobars while 2,000 ft wind crosses isobars at 30°",
      "Surface wind is completely calm regardless of the isobaric gradient"
    ],
    "answerIndex": 0,
    "explanation": "Surface friction retards wind speed, reducing the Coriolis force (which depends on speed). The Pressure Gradient Force dominates, deflecting the surface wind across isobars toward low pressure. In the Northern Hemisphere, this backs the wind (counter-clockwise, ~10° over water, ~30° over land) and reduces speed to ~50% of geostrophic value.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 8 'Winds'"
  },

  # Local Winds
  {
    "topic": "Local Winds",
    "difficulty": "easy",
    "question": "A katabatic wind is an airflow that:",
    "options": [
      "Blows down a cold mountain slope or valley at night due to nocturnal radiative cooling",
      "Blows up a heated slope during the daytime",
      "Blows from sea to land during the late morning",
      "Circulates around a thermal low over flat desert terrain"
    ],
    "answerIndex": 0,
    "explanation": "Katabatic winds are gravity-driven drainage winds of cold, dense air flowing downslope along mountains or hillsides at night after surface radiative cooling.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 9 'Local Winds'"
  },
  {
    "topic": "Local Winds",
    "difficulty": "medium",
    "question": "A sea breeze typically develops under which conditions and at what time of day?",
    "options": [
      "Under sunny skies with weak synoptic winds, blowing onshore from sea to land, reaching peak intensity in mid-afternoon",
      "At night, blowing from land to sea due to cooling coastal terrain",
      "Only during deep monsoon depressions with heavy continuous rain",
      "Just before dawn when the sea surface temperature reaches its minimum"
    ],
    "answerIndex": 0,
    "explanation": "During the day, solar heating warms the land faster than the adjacent sea. Air over the land expands and rises, forming a local low pressure area at the surface. Cooler, denser air moves onshore from the sea (sea breeze), reaching maximum strength between 13:00 and 16:00 local time.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 9 'Local Winds'"
  },

  # Visibility & Fog
  {
    "topic": "Visibility & Fog",
    "difficulty": "easy",
    "question": "What meteorological conditions are most favorable for the formation of radiation fog?",
    "options": [
      "Clear skies, high relative humidity near the ground, and light winds (2 to 8 knots)",
      "Strong gusty winds (over 25 knots), overcast cirrostratus, and dry air",
      "Warm air advecting rapidly over cold sea water in gale force conditions",
      "Deep convective updrafts during mid-day solar heating"
    ],
    "answerIndex": 0,
    "explanation": "Radiation fog requires clear nocturnal skies (allowing maximum terrestrial radiation heat loss), high relative humidity, and light wind (2-8 knots) to provide just enough gentle turbulent mixing without dissipating the cooling layer.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 10 'Visibility & Fog'"
  },
  {
    "topic": "Visibility & Fog",
    "difficulty": "medium",
    "question": "Advection fog forms when:",
    "options": [
      "Warm, moist air moves horizontally over a cooler underlying surface",
      "Terrestrial radiation cools the ground on a calm winter night",
      "Moist air is forced upward along the windward slope of a mountain ridge",
      "Cold air blows over a hot desert lake causing rapid evaporation"
    ],
    "answerIndex": 0,
    "explanation": "Advection fog occurs when warm, moist air travels horizontally over a colder surface (land or water). The lower layers of the air mass are chilled below their dew point by conduction, causing condensation. It requires moderate winds (typically 8-15 knots) to transport the air mass.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 10 'Visibility & Fog'"
  },
  {
    "topic": "Visibility & Fog",
    "difficulty": "hard",
    "question": "Runway Visual Range (RVR) is officially reported in a METAR when prevailing visibility drops below:",
    "options": [
      "1,500 metres",
      "5,000 metres",
      "800 metres",
      "3,000 metres"
    ],
    "answerIndex": 0,
    "explanation": "In accordance with ICAO Annex 3 and DGCA regulations, Runway Visual Range (RVR) is measured and reported when the horizontal visibility or RVR is less than 1,500 metres.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 10 'Visibility & Fog'"
  },

  # Thunderstorms
  {
    "topic": "Thunderstorms",
    "difficulty": "easy",
    "question": "What three basic environmental ingredients are essential for thunderstorm development?",
    "options": [
      "Atmospheric instability, high moisture content, and a lifting mechanism",
      "High barometric pressure, cold dry air, and strong surface inversions",
      "Dry adiabatic lapse rates, low humidity, and calm upper winds",
      "Strong katabatic winds, clear skies, and freezing sea surface temperatures"
    ],
    "answerIndex": 0,
    "explanation": "The three essential ingredients for any thunderstorm are: 1) sufficient atmospheric instability, 2) abundant moisture in the lower to middle troposphere, and 3) a trigger or lifting mechanism (e.g., surface heating, front, orography, or convergence).",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 11 'Thunderstorms'"
  },
  {
    "topic": "Thunderstorms",
    "difficulty": "medium",
    "question": "The mature stage of a thunderstorm is definitively marked by:",
    "options": [
      "The initiation of rain or precipitation reaching the surface",
      "The dissipation of the anvil top",
      "The total cessation of all internal updrafts",
      "The appearance of pure cirrus mammatus clouds at 40,000 ft"
    ],
    "answerIndex": 0,
    "explanation": "The mature stage begins when precipitation produced in the cloud becomes too heavy for the updrafts to support, falling through the cloud and reaching the ground. This creates co-existing strong updrafts and downdrafts.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 11 'Thunderstorms'"
  },
  {
    "topic": "Thunderstorms",
    "difficulty": "hard",
    "question": "When an aircraft penetrates a microburst during approach, what sequence of airspeed and flight path deviations is experienced?",
    "options": [
      "A rapid increase in indicated airspeed (headwind), followed by strong downdraft, and then a sudden drop in indicated airspeed (tailwind) with loss of lift",
      "A sudden severe drop in airspeed followed by a prolonged ballooning climb",
      "Constant airspeed with a gradual barometric pressure rise of 10 hPa",
      "Gradual tailwind increase throughout with no vertical shear"
    ],
    "answerIndex": 0,
    "explanation": "A microburst produces intense outward-diverging winds near the ground. An aircraft encounters: 1) an initial strong headwind causing airspeed and lift to surge, 2) a severe vertical downdraft, and 3) a sudden transition to a strong tailwind causing airspeed and lift to plunge, driving the aircraft toward the ground.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 11 'Thunderstorms'"
  },

  # Ice Accretion
  {
    "topic": "Ice Accretion",
    "difficulty": "easy",
    "question": "Clear ice (glaze) forms under which of the following in-flight meteorological conditions?",
    "options": [
      "Large supercooled water droplets at temperatures between 0°C and -10°C in cumuliform clouds",
      "Small supercooled droplets at temperatures below -20°C in stratiform clouds",
      "Dry ice crystals at temperatures below -40°C in cirrus clouds",
      "In clear air with relative humidity below 30%"
    ],
    "answerIndex": 0,
    "explanation": "Clear ice forms when large supercooled water droplets impact an airframe at temperatures near freezing (0°C to -10°C). Due to slow freezing, the droplets spread out before solidifying, forming a smooth, transparent, dense, and tenacious sheet of ice that is extremely difficult to dislodge.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 12 'Ice Accretion'"
  },
  {
    "topic": "Ice Accretion",
    "difficulty": "medium",
    "question": "Rime ice is typically characterized by:",
    "options": [
      "A rough, milky white, opaque, and brittle appearance formed by instantaneous freezing of small supercooled droplets",
      "A transparent, smooth sheet of heavy ice forming horns on the leading edge",
      "Liquid water freezing in fuel lines due to high altitude evaporation",
      "Thin ice needles accumulating only on heated windshields"
    ],
    "answerIndex": 0,
    "explanation": "Rime ice forms when small supercooled water droplets freeze instantaneously upon contact with the airframe at lower temperatures (-10°C to -20°C), trapping air pockets between frozen droplets, resulting in a brittle, milky-white, opaque structure.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 12 'Ice Accretion'"
  },
  {
    "topic": "Ice Accretion",
    "difficulty": "hard",
    "question": "Carburettor icing can occur even at outside ambient air temperatures as high as +25°C under what conditions?",
    "options": [
      "High relative humidity (above 60-80%) and low throttle settings",
      "Extremely dry desert air at full throttle cruise",
      "Sub-zero temperatures with lean mixture settings only",
      "High altitude flight above FL200 in standard atmosphere"
    ],
    "answerIndex": 0,
    "explanation": "Fuel vaporization and adiabatic pressure reduction through the carburettor venturi can lower internal temperatures by up to 20°C to 25°C. In humid air (RH > 60-80%), water vapor condenses and freezes onto the throttle valve and throat even when ambient temperature is +20°C to +25°C.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 12 'Ice Accretion'"
  },

  # Clear Air Turbulence & Jet Streams
  {
    "topic": "Clear Air Turbulence",
    "difficulty": "medium",
    "question": "Clear Air Turbulence (CAT) is most frequently encountered in which region relative to a jet stream core?",
    "options": [
      "On the polar (cold) side of the jet core in regions of strong horizontal and vertical wind shear",
      "Directly in the center of the jet core where wind speed is highest",
      "On the equatorial (warm) side far below the level of maximum wind",
      "Only over tropical oceans near the inter-tropical convergence zone"
    ],
    "answerIndex": 0,
    "explanation": "CAT is caused by severe wind shear. The strongest vertical and horizontal wind shear occurs on the polar (cold, low-pressure) side of the jet stream core and in the upper troposphere just above and below the jet core.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 13 'Clear Air Turbulence'"
  },
  {
    "topic": "Jet Streams",
    "difficulty": "easy",
    "question": "By international WMO definition, what is the minimum core wind speed required for an upper-level wind stream to be classified as a jet stream?",
    "options": [
      "60 knots",
      "100 knots",
      "40 knots",
      "150 knots"
    ],
    "answerIndex": 0,
    "explanation": "By WMO definition, a jet stream is a strong, narrow current of wind concentrated along a quasi-horizontal axis in the upper troposphere or stratosphere, characterized by vertical and horizontal wind shear and possessing a minimum wind speed of 60 knots (approx 110 km/h).",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Jet Streams'"
  },
  {
    "topic": "Jet Streams",
    "difficulty": "hard",
    "question": "The Tropical Easterly Jet (TEJ) over peninsular India and the northern Indian Ocean is active during which season and at what typical altitude?",
    "options": [
      "Southwest Monsoon season (June to September) around 100-150 hPa (FL450-FL500)",
      "Winter season (December to February) around 300 hPa (FL300)",
      "Post-monsoon transition (October) at 500 hPa (FL180)",
      "Throughout the entire calendar year at FL340"
    ],
    "answerIndex": 0,
    "explanation": "The Tropical Easterly Jet (TEJ) is a unique seasonal upper-tropospheric jet stream that establishes itself over peninsular India and the Arabian Sea during the Southwest Monsoon (June to September). It flows from east to west at altitudes between FL450 and FL500 (150-100 hPa) with core speeds often exceeding 80-100 knots.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 14 'Jet Streams'"
  },

  # Air Masses & Fronts
  {
    "topic": "Air Masses & Fronts",
    "difficulty": "easy",
    "question": "A cold front is defined as the leading boundary of an advancing:",
    "options": [
      "Cold air mass replacing a warmer air mass at the surface",
      "Warm air mass sliding up over a cold air mass",
      "Quasi-stationary thermal trough without temperature change",
      "Occluded upper trough where both fronts have dissipated"
    ],
    "answerIndex": 0,
    "explanation": "A cold front is the leading edge of a colder, denser air mass that wedges under and displaces a warmer air mass as it advances.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 15 'Air Masses & Fronts'"
  },
  {
    "topic": "Air Masses & Fronts",
    "difficulty": "medium",
    "question": "As a classic active cold front passes over an airfield, what characteristic surface weather changes occur?",
    "options": [
      "Wind veers sharply, temperature drops, barometric pressure rises abruptly, accompanied by gusty showers",
      "Wind backs, temperature rises, pressure drops steadily, and skies become clear",
      "Pressure drops to minimum followed by continuous light drizzle and warming",
      "Wind remains constant in direction while barometric pressure stays unchanged"
    ],
    "answerIndex": 0,
    "explanation": "With the passage of a Northern Hemisphere cold front: wind veers (shifts clockwise, e.g. SW to NW), temperature drops sharply, atmospheric pressure rises rapidly following the frontal trough line, and heavy showery precipitation or thunderstorms occur.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 15 'Air Masses & Fronts'"
  },

  # Climatology of India & Monsoon
  {
    "topic": "Climatology of India",
    "difficulty": "easy",
    "question": "The onset of the Southwest Monsoon over the southern mainland of India (Kerala coast) typically occurs around:",
    "options": [
      "1st of June",
      "1st of April",
      "15th of July",
      "1st of September"
    ],
    "answerIndex": 0,
    "explanation": "The normal climatological onset date of the Indian Southwest Monsoon over the Kerala coast is 1st of June (with a standard deviation of about 7 days).",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 16 'Climatology of India'"
  },
  {
    "topic": "Climatology of India",
    "difficulty": "medium",
    "question": "Western Disturbances that bring vital winter rain and snowfall to Northwest India and the Himalayas originate over:",
    "options": [
      "The Mediterranean Sea and Caspian Sea region as extra-tropical wave depressions",
      "The Bay of Bengal as severe tropical cyclonic storms",
      "The equatorial Indian Ocean as warm core convective systems",
      "The Tibetan Plateau as thermal katabatic winds"
    ],
    "answerIndex": 0,
    "explanation": "Western Disturbances are shallow extra-tropical wave depressions originating over the Mediterranean / Caspian Sea region that travel eastward embedded in the subtropical westerly jet stream, bringing winter precipitation to northern and north-western India.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 16 'Climatology of India'"
  },
  {
    "topic": "Tropical Systems & Monsoon",
    "difficulty": "medium",
    "question": "In the eye of a mature tropical cyclone, what weather conditions are typically observed?",
    "options": [
      "Light winds, subsiding air, little or no cloudiness, and the lowest barometric pressure of the system",
      "The strongest hurricane-force winds and heaviest torrential rainfall",
      "Extreme vertical wind shear with continuous severe thunderstorm downbursts",
      "Rapidly rising barometric pressure with dense overcast nimbostratus"
    ],
    "answerIndex": 0,
    "explanation": "The eye of a tropical cyclone is a central calm region surrounded by the violent eyewall. It features light descending air, low cloud amounts or partly clear skies, and contains the lowest central pressure of the storm.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 17 'Tropical Systems & Monsoon'"
  },

  # Meteorological Services & Codes (METAR / TAF / SIGMET)
  {
    "topic": "Meteorological Services & Codes",
    "difficulty": "easy",
    "question": "In a METAR report, the code group 'CAVOK' replaces visibility, weather, and cloud groups when which conditions are all simultaneously met?",
    "options": [
      "Visibility 10 km or more, no cloud below 5,000 ft or MSA (whichever is higher), no CB/TCU, and no significant weather",
      "Visibility 5,000 m or more, ceiling above 1,500 ft, and no rain",
      "Visibility 8 km or more, sky clear, and surface winds below 10 knots",
      "Airfield is in VFR daylight conditions with no reported icing"
    ],
    "answerIndex": 0,
    "explanation": "CAVOK (Ceiling And Visibility OK) requires: 1) Visibility 10 km or more; 2) No cloud of operational significance (no cloud below 5,000 ft or minimum sector altitude, whichever is greater, and no CB or TCU at any level); and 3) No significant weather at or near the aerodrome.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Meteorological Services & Codes'"
  },
  {
    "topic": "Meteorological Services & Codes",
    "difficulty": "medium",
    "question": "In a METAR, what does the group 'R27/1200D' signify?",
    "options": [
      "Runway 27 Runway Visual Range is 1,200 metres with a downward (decreasing) trend over the last 10 minutes",
      "Runway 27 is closed for 1,200 minutes due to fog",
      "Runway 27 touchdown zone has 12 mm of dry snow",
      "Runway heading 270° with wind 12 knots gusting during daylight"
    ],
    "answerIndex": 0,
    "explanation": "In RVR reporting: 'R27' denotes runway 27; '1200' represents 1,200 metres visual range; and the suffix 'D' indicates a downward (decreasing) trend over the preceding 10-minute period (U = upward, N = no change).",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Meteorological Services & Codes'"
  },
  {
    "topic": "Meteorological Services & Codes",
    "difficulty": "medium",
    "question": "In an aerodrome forecast (TAF), what does the change indicator 'BECMG 1416' indicate?",
    "options": [
      "A regular or irregular change expected to commence at 14:00 UTC and be completed by 16:00 UTC",
      "Temporary fluctuations lasting less than one hour between 14:00 and 16:00 UTC",
      "A sudden severe weather change occurring exactly at 14:16 UTC",
      "Weather conditions valid only for 14 hours starting at 16:00 UTC"
    ],
    "answerIndex": 0,
    "explanation": "BECMG (becoming) indicates a transition where weather conditions are forecast to change at a regular or irregular rate between the start time (14:00 UTC) and the end time (16:00 UTC), after which the new conditions persist.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Meteorological Services & Codes'"
  },
  {
    "topic": "Meteorological Services & Codes",
    "difficulty": "hard",
    "question": "What type of phenomenon warrants the issuance of a SIGMET for en-route aircraft?",
    "options": [
      "Severe turbulence, severe icing, volcanic ash, heavy thunderstorm (obscured, embedded, or squall line), and tropical cyclones",
      "Moderate turbulence at FL050 in VFR conditions",
      "Light chop and isolated fair weather cumulus clouds",
      "Routine diurnal wind shifts between land and sea breezes"
    ],
    "answerIndex": 0,
    "explanation": "SIGMETs are issued by Meteorological Watch Offices (MWOs) to warn pilots of en-route weather phenomena that may affect the safety of all aircraft operations: severe turbulence, severe icing, severe mountain waves, heavy sandstorm, tropical cyclone, volcanic ash, and obscured/embedded/frequent thunderstorms.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Meteorological Services & Codes'"
  }
]

TG_NEW_QUESTIONS = [
  # Principles of Flight
  {
    "topic": "Principles of Flight",
    "difficulty": "easy",
    "question": "The total aerodynamic drag of an aircraft in level unaccelerated flight is the sum of:",
    "options": [
      "Parasite drag and induced drag",
      "Wave drag and skin friction drag only",
      "Form drag and interference drag only",
      "Lift-dependent drag and thrust drag"
    ],
    "answerIndex": 0,
    "explanation": "Total aircraft drag consists of parasite drag (form, skin friction, and interference drag, which increases with the square of speed) and induced drag (vortex drag created as a byproduct of producing lift, which decreases with the square of speed).",
    "source": "Oxford ATPL Principles of Flight / AC 65-9A, Chapter 'Aerodynamic Drag'"
  },
  {
    "topic": "Principles of Flight",
    "difficulty": "medium",
    "question": "How does induced drag vary with aircraft airspeed in straight-and-level flight?",
    "options": [
      "Induced drag is inversely proportional to the square of airspeed (decreases as speed increases)",
      "Induced drag increases directly with the cube of airspeed",
      "Induced drag remains constant at all airspeeds",
      "Induced drag increases linearly with airspeed"
    ],
    "answerIndex": 0,
    "explanation": "Induced drag is a byproduct of generating lift at angle of attack (Di ∝ CL² / π*AR). At high speeds, CL is low, so induced drag is small. At low speeds near stall, high CL produces strong wingtip vortices, making induced drag highest.",
    "source": "Oxford ATPL Principles of Flight / AC 65-9A, Chapter 'Aerodynamic Drag'"
  },
  {
    "topic": "Principles of Flight",
    "difficulty": "medium",
    "question": "What is the effect of extending trailing-edge flaps on stall speed and glide angle?",
    "options": [
      "Decreases stall speed and steepens the glide approach angle",
      "Increases stall speed and flattens the glide path",
      "Decreases stall speed and increases maximum glide distance",
      "Has no effect on stall speed but reduces parasite drag"
    ],
    "answerIndex": 0,
    "explanation": "Trailing-edge flaps increase wing camber and surface area, raising the maximum lift coefficient (CLmax). This lowers the stall speed (Vs), while significantly increasing drag, enabling a steeper landing approach without gaining airspeed.",
    "source": "Oxford ATPL Principles of Flight / AC 65-9A, Chapter 'High Lift Devices'"
  },
  {
    "topic": "Principles of Flight",
    "difficulty": "hard",
    "question": "In a coordinated, level, constant-altitude turn at a 60-degree bank angle, what is the load factor (g)?",
    "options": [
      "2.0 g",
      "1.41 g",
      "3.0 g",
      "1.15 g"
    ],
    "answerIndex": 0,
    "explanation": "Load factor n = 1 / cos(bank angle). For 60°: n = 1 / cos(60°) = 1 / 0.5 = 2.0 g. Stall speed in a turn increases by the square root of load factor (√2 ≈ 1.414, or a 41.4% increase in stall speed).",
    "source": "Oxford ATPL Principles of Flight / AC 65-9A, Chapter 'Turning Flight & Load Factors'"
  },

  # Piston Engines
  {
    "topic": "Piston Engines",
    "difficulty": "easy",
    "question": "What is the primary function of dual independent ignition systems (two spark plugs per cylinder and two magnetos) in aero piston engines?",
    "options": [
      "Safety redundancy and improved combustion efficiency",
      "To allow the engine to run on automotive diesel fuel",
      "To power the aircraft avionics bus directly",
      "To prevent carburettor ice accumulation"
    ],
    "answerIndex": 0,
    "explanation": "Aero piston engines employ two independent magnetos each firing one of two spark plugs per cylinder. This ensures safety redundancy (the engine operates smoothly if one magneto fails) and provides faster, more complete combustion, increasing power output.",
    "source": "Oxford ATPL Aircraft General Knowledge / Piston Engines, Chapter 'Ignition Systems'"
  },
  {
    "topic": "Piston Engines",
    "difficulty": "medium",
    "question": "What is engine detonation and what typically causes it?",
    "options": [
      "Uncontrolled, instantaneous explosive combustion of the remaining fuel-air charge caused by excessive cylinder head temperature, too low fuel octane, or excessively high manifold pressure",
      "Ignition of the fuel charge prior to the timed spark discharge due to glowing carbon deposits",
      "Flame flashing back into the induction intake manifold during starting",
      "Excessive fuel richness washing lubricating oil off cylinder walls"
    ],
    "answerIndex": 0,
    "explanation": "Detonation is the spontaneous, explosive combustion of the end-gas ahead of the normal flame front, causing rapid pressure spikes, severe knocking, high cylinder head temperatures, and catastrophic piston damage.",
    "source": "Oxford ATPL Aircraft General Knowledge / Piston Engines, Chapter 'Combustion & Fuels'"
  },
  {
    "topic": "Piston Engines",
    "difficulty": "hard",
    "question": "What happens to the fuel-air mixture ratio delivered by an uncompensated carburettor as an aircraft climbs to higher altitude?",
    "options": [
      "The mixture becomes excessively rich because air density decreases while fuel nozzle metering pressure remains relatively constant",
      "The mixture becomes excessively lean due to lower ambient temperatures",
      "The mixture remains exactly stoichiometric automatically",
      "Fuel flow drops to zero due to fuel tank depressurization"
    ],
    "answerIndex": 0,
    "explanation": "As altitude increases, air density decreases, meaning less mass of air enters the carburettor for a given volume. Without leaning the mixture control, the carburettor meters fuel based on air velocity, causing the mixture to become progressively richer.",
    "source": "Oxford ATPL Aircraft General Knowledge / Piston Engines, Chapter 'Fuel Metering'"
  },

  # Propellers
  {
    "topic": "Propellers",
    "difficulty": "easy",
    "question": "Why is an aircraft propeller blade twisted along its length from root to tip?",
    "options": [
      "To maintain a relatively constant angle of attack along the entire length of the blade despite higher linear velocities near the tip",
      "To prevent flutter caused by gyroscopic precession",
      "To ensure equal centrifugal force across the hub",
      "To direct exhaust fumes away from the cabin intake"
    ],
    "answerIndex": 0,
    "explanation": "Because the blade tip travels through a much larger circumference than the root, its rotational speed is much higher. Twisting the blade (reducing blade angle toward the tip) maintains a uniform angle of attack and even thrust distribution along the blade.",
    "source": "Oxford ATPL Aircraft General Knowledge / Propellers, Chapter 'Propeller Geometry'"
  },
  {
    "topic": "Propellers",
    "difficulty": "medium",
    "question": "On a multi-engine aircraft, what does 'feathering' a propeller achieve after an engine failure?",
    "options": [
      "Rotates the propeller blades to an angle approximately 90° into the airflow (edge forward) to minimize aerodynamic drag and stop windmilling",
      "Locks the propeller into fine pitch for maximum climb thrust",
      "Reverses blade pitch to provide reverse aerodynamic braking",
      "Disengages the propeller governor and dumps hydraulic oil into the engine sump"
    ],
    "answerIndex": 0,
    "explanation": "Feathering rotates the blades until they are edge-on to the relative airflow (pitch angle ~90°). This eliminates windmilling drag, stops engine rotation to prevent further mechanical damage, and dramatically preserves single-engine climb and glide performance.",
    "source": "Oxford ATPL Aircraft General Knowledge / Propellers, Chapter 'Multi-Engine Propellers'"
  },

  # Aircraft Systems & Instruments
  {
    "topic": "Aircraft Systems",
    "difficulty": "easy",
    "question": "What is the primary function of an accumulator in an aircraft hydraulic system?",
    "options": [
      "To store fluid under pressure, absorb hydraulic shock loads, and provide emergency pressure for limited actuator operation",
      "To cool the hydraulic fluid before it returns to the reservoir",
      "To convert electrical AC power to direct DC current",
      "To filter particulate contaminants from the return lines"
    ],
    "answerIndex": 0,
    "explanation": "An accumulator holds a volume of fluid under compressed gas (nitrogen) pressure. It dampens pump pressure pulsations, assists the pump during peak demand periods, and provides emergency pressure to operate systems (e.g., landing gear or brakes) if the primary pump fails.",
    "source": "Oxford ATPL Aircraft General Knowledge / Hydraulic Systems"
  },
  {
    "topic": "Aircraft Systems",
    "difficulty": "medium",
    "question": "Mineral-based aircraft hydraulic fluid (MIL-H-5606) is dyed which distinctive color?",
    "options": [
      "Red",
      "Blue",
      "Purple",
      "Straw yellow"
    ],
    "answerIndex": 0,
    "explanation": "Mineral-based hydraulic fluid conforming to MIL-PRF-5606 is dyed red for rapid identification and leak detection. Synthetic fluids (like Skydrol) are purple, while vegetable-based fluids are blue.",
    "source": "Oxford ATPL Aircraft General Knowledge / Hydraulic Systems"
  },
  {
    "topic": "Pitot-Static Instruments",
    "difficulty": "medium",
    "question": "If the pitot tube ram air intake and its drain hole become completely blocked by ice during flight, how will the Airspeed Indicator (ASI) behave?",
    "options": [
      "The ASI will act like an altimeter: overreading during a climb and underreading during a descent",
      "The ASI will immediately drop to zero and stay at zero",
      "The ASI will freeze at the cruise airspeed and never change regardless of altitude or pitch",
      "The ASI will underread during a climb and overread during a descent"
    ],
    "answerIndex": 0,
    "explanation": "With pitot tube and drain blocked, trapped air pressure in the capsule remains constant. During a climb, ambient static pressure decreases, causing the diaphragm to expand, making the ASI overread (behave like an altimeter). During descent, static pressure rises, making the ASI underread.",
    "source": "Oxford ATPL Instrumentation / Pitot-Static Systems"
  },
  {
    "topic": "Gyroscopic Instruments",
    "difficulty": "medium",
    "question": "What are the two fundamental physical properties that govern the operation of all aircraft mechanical gyroscopic instruments?",
    "options": [
      "Rigidity in space (gyroscopic inertia) and Precession",
      "Coriolis acceleration and centrifugal force",
      "Magnetic dip and variation",
      "Pascal's law and Bernoulli's theorem"
    ],
    "answerIndex": 0,
    "explanation": "All gyroscopic flight instruments (Attitude Indicator, Directional Gyro, Turn and Slip Indicator) operate on two fundamental principles: 1) Rigidity in space (rotor remains fixed in plane of rotation), and 2) Precession (force applied manifests 90° ahead in the direction of rotation).",
    "source": "Oxford ATPL Instrumentation / Gyroscopes"
  },
  {
    "topic": "Weight & Balance",
    "difficulty": "hard",
    "question": "What are the aerodynamic consequences of operating an aircraft with its Center of Gravity (CG) located at the aft limit?",
    "options": [
      "Reduced longitudinal stability, lower stall speed, and difficult stall/spin recovery",
      "Increased longitudinal stability, higher stall speed, and increased control forces",
      "Higher cruise drag due to increased downward tail load",
      "Inability to rotate the aircraft during takeoff"
    ],
    "answerIndex": 0,
    "explanation": "An aft CG reduces the tail moment arm and reduces the downward tail load required for trim. This lowers the aircraft's effective weight and stall speed, and improves cruise speed. However, longitudinal static stability is severely degraded, control forces are light, and recovery from stalls and spins becomes difficult or impossible.",
    "source": "Oxford ATPL Principles of Flight / Weight and Balance"
  }
]

TS_NEW_QUESTIONS = [
  # V-speeds and their meanings
  {
    "topic": "V-speeds and their meanings",
    "difficulty": "easy",
    "question": "What does the abbreviation 'Vs0' represent in aircraft flight performance?",
    "options": [
      "Stalling speed or minimum steady flight speed in the landing configuration",
      "Stalling speed in the clean (flaps and gear retracted) configuration",
      "Design maneuvering speed at maximum gross weight",
      "Maximum speed with flaps fully extended"
    ],
    "answerIndex": 0,
    "explanation": "Vs0 is the stalling speed or minimum steady flight speed at which the airplane is controllable in the landing configuration (landing gear extended and full flaps). On the Airspeed Indicator, it marks the lower boundary of the white arc.",
    "source": "Aircraft Flight Manual / POH Section 1 'V-speeds'"
  },
  {
    "topic": "V-speeds and their meanings",
    "difficulty": "easy",
    "question": "What does the abbreviation 'Vx' represent?",
    "options": [
      "Speed for best angle of climb (greatest gain of altitude in a given horizontal distance)",
      "Speed for best rate of climb (greatest gain of altitude in a given time)",
      "Maximum structural cruising speed",
      "Design maneuvering speed"
    ],
    "answerIndex": 0,
    "explanation": "Vx is the best angle-of-climb speed. It delivers the maximum altitude gain over a given horizontal distance forward, making it critical for obstacle clearance after takeoff.",
    "source": "Aircraft Flight Manual / POH Section 4 'Performance & V-speeds'"
  },
  {
    "topic": "V-speeds and their meanings",
    "difficulty": "medium",
    "question": "Why does design maneuvering speed (Va) decrease as aircraft weight decreases?",
    "options": [
      "A lighter aircraft flies at a lower angle of attack for a given airspeed, so a strong gust can induce higher g-loads before the wing stalls to relieve structural strain",
      "Lighter aircraft experience higher skin friction drag",
      "The elevator authority increases by the square of weight reduction",
      "Engine power drops linearly as cargo weight is unloaded"
    ],
    "answerIndex": 0,
    "explanation": "At lower weights, the wing operates at a lower cruise angle of attack. A sharp vertical gust will produce a larger change in angle of attack and therefore generate higher load factors before reaching the stall angle. Thus, Va must be reduced at lower weights to allow the aircraft to stall before exceeding structural limit load factors.",
    "source": "Aircraft Flight Manual / POH Section 2 'Limitations'"
  },
  {
    "topic": "V-speeds and their meanings",
    "difficulty": "medium",
    "question": "On a multi-engine aircraft, what does the blue radial line on the Airspeed Indicator indicate?",
    "options": [
      "Vyse: Best rate-of-climb speed with one engine inoperative",
      "Vmc: Minimum control speed with critical engine inoperative",
      "Vne: Never exceed speed in smooth air",
      "Vfe: Maximum flap extended speed"
    ],
    "answerIndex": 0,
    "explanation": "On light multi-engine aircraft, the blue radial line on the ASI marks Vyse, which is the best rate-of-climb speed with the critical engine inoperative (single-engine best rate of climb).",
    "source": "Multi-Engine Flight Manual / POH Section 1 & 2"
  },

  # Airspeed indicator markings
  {
    "topic": "Airspeed indicator markings",
    "difficulty": "easy",
    "question": "What airspeed range is represented by the white arc on an aircraft Airspeed Indicator?",
    "options": [
      "The full flap operating range, from Vs0 to Vfe",
      "The normal operating range, from Vs1 to Vno",
      "The caution range, from Vno to Vne",
      "The inverted flight operating range"
    ],
    "answerIndex": 0,
    "explanation": "The white arc represents the flap operating range. The lower limit is the stall speed in landing configuration (Vs0), and the upper limit is the maximum permissible airspeed with flaps extended (Vfe).",
    "source": "Aircraft Flight Manual / POH Section 2 'Airspeed Limitations'"
  },
  {
    "topic": "Airspeed indicator markings",
    "difficulty": "medium",
    "question": "Operation in the yellow arc of the Airspeed Indicator is permitted only:",
    "options": [
      "In smooth air, and with caution",
      "During normal climb with flaps fully retracted",
      "During intentional aerobatics with gear extended",
      "Only below 10,000 ft in turbulence"
    ],
    "answerIndex": 0,
    "explanation": "The yellow arc is the caution range (between Vno and Vne). Flights within this airspeed range must be conducted with caution and only in smooth, non-turbulent air to prevent structural damage from gusts.",
    "source": "Aircraft Flight Manual / POH Section 2 'Limitations'"
  },

  # Fuel grades and colors
  {
    "topic": "Fuel grades and colors",
    "difficulty": "easy",
    "question": "What is the official dyed color of Aviation Gasoline 100LL (Low Lead)?",
    "options": [
      "Blue",
      "Green",
      "Red",
      "Clear / Straw"
    ],
    "answerIndex": 0,
    "explanation": "AVGAS 100LL is dyed blue. Standard AVGAS 100 is green, AVGAS 80/87 is red, and Jet A-1 is clear or light straw-colored.",
    "source": "Aircraft Flight Manual / POH Section 2 'Fuel Specifications'"
  },
  {
    "topic": "Fuel grades and colors",
    "difficulty": "medium",
    "question": "When draining a fuel sample during pre-flight inspection, how can water contamination be visually identified in the tester cup?",
    "options": [
      "Water is denser than aviation gasoline and collects at the bottom of the tester cup, forming a distinct clear bubble or separation line beneath the blue fuel",
      "Water floats on top of the fuel as a bright orange layer",
      "Water turns the entire fuel sample bright purple",
      "Water immediately evaporates leaving a crystalline salt deposit"
    ],
    "answerIndex": 0,
    "explanation": "Because water has a higher density (1.0 kg/L) than avgas (~0.72 kg/L), free water quickly settles to the lowest point of the sumps and tester cup, creating a visible separation boundary line or bubble beneath the dyed avgas.",
    "source": "Aircraft Flight Manual / POH Section 4 'Preflight Procedures'"
  },

  # Altimeter setting procedures
  {
    "topic": "Altimeter setting procedures",
    "difficulty": "easy",
    "question": "When an aircraft altimeter is set to QFE on the ground at an aerodrome, the altimeter pointers indicate:",
    "options": [
      "Zero feet",
      "The elevation of the aerodrome above sea level",
      "Pressure altitude relative to the standard 1013.25 hPa datum",
      "The density altitude of the runway"
    ],
    "answerIndex": 0,
    "explanation": "QFE is the barometric pressure measured at the aerodrome datum. When set on the subscale while on the runway, the altimeter reads zero feet (height above ground level).",
    "source": "Aircraft Flight Manual / ICAO Doc 8168 Altimeter Procedures"
  },
  {
    "topic": "Altimeter setting procedures",
    "difficulty": "medium",
    "question": "When climbing through the Transition Altitude, what altimeter subscale adjustment must the pilot make?",
    "options": [
      "Set the altimeter to the standard pressure setting of 1013.25 hPa (29.92 inHg)",
      "Set the altimeter to regional minimum QNH",
      "Set the altimeter to runway QFE",
      "Leave the altimeter on aerodrome QNH until reaching the cruise descent point"
    ],
    "answerIndex": 0,
    "explanation": "In accordance with standard ICAO and DGCA procedures, when climbing through the Transition Altitude (TA), altimeters are reset from local QNH to the standard altimeter setting of 1013.25 hPa (Flight Level mode).",
    "source": "DGCA CAR Section 9 / ICAO Doc 8168"
  },

  # Performance & Limitations
  {
    "topic": "Performance charts",
    "difficulty": "medium",
    "question": "How does an uphill runway slope affect an aircraft's takeoff run and landing ground roll?",
    "options": [
      "Increases the takeoff ground roll distance and decreases the landing ground roll distance",
      "Decreases both takeoff distance and landing distance",
      "Increases both takeoff distance and landing distance",
      "Decreases takeoff distance and increases landing distance"
    ],
    "answerIndex": 0,
    "explanation": "An uphill runway slope retards aircraft acceleration, requiring a longer takeoff run to achieve rotation speed. On landing, gravity aids deceleration, shortening the landing ground roll.",
    "source": "Aircraft Flight Manual / POH Section 5 'Performance'"
  },
  {
    "topic": "POH sections",
    "difficulty": "easy",
    "question": "In the standard GAMA format Pilot's Operating Handbook (POH), which section contains Emergency Procedures?",
    "options": [
      "Section 3",
      "Section 2",
      "Section 4",
      "Section 5"
    ],
    "answerIndex": 0,
    "explanation": "In standardized GAMA format POHs: Section 1 is General, Section 2 is Limitations, Section 3 is Emergency Procedures, Section 4 is Normal Procedures, Section 5 is Performance, and Section 6 is Weight & Balance.",
    "source": "General Aviation Manufacturers Association (GAMA) Specification No. 1"
  }
]

RTR_NEW_QUESTIONS = [
  # Standard phraseology
  {
    "topic": "Standard phraseology",
    "difficulty": "easy",
    "question": "What is the exact aviation meaning of the phraseology term 'ROGER' in radiotelephony?",
    "options": [
      "I have received all of your last transmission",
      "I understand your message and will comply with it",
      "Permission for proposed action granted",
      "That is correct"
    ],
    "answerIndex": 0,
    "explanation": "Under ICAO Doc 9432 and WPC guidelines, 'ROGER' means strictly: 'I have received all of your last transmission.' It must NEVER be used to indicate agreement, approval, or compliance (which is 'WILCO').",
    "source": "ICAO Doc 9432 'Manual of Radiotelephony' / WPC RTR(A)"
  },
  {
    "topic": "Standard phraseology",
    "difficulty": "easy",
    "question": "What is the correct radiotelephony term used to mean 'I understand your message and will comply with it'?",
    "options": [
      "WILCO",
      "ROGER",
      "AFFIRM",
      "ACKNOWLEDGE"
    ],
    "answerIndex": 0,
    "explanation": "'WILCO' is the standard radiotelephony abbreviation for 'Will Comply' and means 'I understand your message and will comply with it.'",
    "source": "ICAO Doc 9432 'Manual of Radiotelephony' / WPC RTR(A)"
  },
  {
    "topic": "Standard phraseology",
    "difficulty": "medium",
    "question": "Which radiotelephony phrase must be used to request a station to repeat all, or a specific part, of a message?",
    "options": [
      "SAY AGAIN",
      "REPEAT",
      "SPEAK ONCE MORE",
      "OVER"
    ],
    "answerIndex": 0,
    "explanation": "The phrase 'SAY AGAIN' is used. The word 'REPEAT' is prohibited in civil radiotelephony communications because in military firing operations 'repeat' is an instruction to artillery to fire again.",
    "source": "ICAO Doc 9432 'Manual of Radiotelephony' / WPC RTR(A)"
  },
  {
    "topic": "Standard phraseology",
    "difficulty": "medium",
    "question": "What is the correct standard radiotelephony transmission to request a radio check from an ATC station?",
    "options": [
      "Delhi Tower, VT-ABC, RADIO CHECK 118.1",
      "Delhi Tower, VT-ABC, HOW DO YOU HEAR ME?",
      "Delhi Tower, VT-ABC, READABILITY CHECK PLEASE",
      "Delhi Tower, VT-ABC, SIGNAL STRENGTH TEST"
    ],
    "answerIndex": 0,
    "explanation": "The standard ICAO Doc 9432 phraseology for requesting a transmission quality report is: '[Station callsign], [Aircraft callsign], RADIO CHECK [frequency].'",
    "source": "ICAO Doc 9432 'Manual of Radiotelephony' / WPC RTR(A)"
  },

  # Phonetic alphabet and numbers
  {
    "topic": "Phonetic alphabet",
    "difficulty": "easy",
    "question": "In aeronautical radiotelephony, how is the number '9' correctly pronounced?",
    "options": [
      "NIN-ER",
      "NINE",
      "NO-VE-NA",
      "NYNE"
    ],
    "answerIndex": 0,
    "explanation": "To prevent confusion with the German word 'nein' (no) or the number 'one' and 'five', the number 9 is phonetically spoken as 'NIN-ER'.",
    "source": "ICAO Doc 9432 / Annex 10 Vol II"
  },
  {
    "topic": "Phonetic alphabet",
    "difficulty": "easy",
    "question": "How is an altitude of 10,500 feet transmitted in standard radiotelephony?",
    "options": [
      "ONE ZERO THOUSAND FIVE HUNDRED FEET",
      "TEN POINT FIVE THOUSAND",
      "TEN THOUSAND FIVE HUNDRED FEET",
      "WUN ZERO FIVE ZERO ZERO FEET"
    ],
    "answerIndex": 0,
    "explanation": "Under ICAO Annex 10 and Doc 9432 standards, numbers involving thousands are spoken by pronouncing each digit in the number of thousands followed by the word 'THOUSAND' and then each digit of hundreds followed by 'HUNDRED': 'ONE ZERO THOUSAND FIVE HUNDRED FEET'.",
    "source": "ICAO Doc 9432 'Manual of Radiotelephony'"
  },

  # Readability scale
  {
    "topic": "Readability scale",
    "difficulty": "easy",
    "question": "In radiotelephony signal reports, what does a readability of '3' mean?",
    "options": [
      "Readable but with difficulty",
      "Readable now and then",
      "Unreadable",
      "Perfectly readable"
    ],
    "answerIndex": 0,
    "explanation": "The ICAO Readability Scale is: 1 = Unreadable, 2 = Readable now and then, 3 = Readable but with difficulty, 4 = Readable, 5 = Perfectly readable.",
    "source": "ICAO Annex 10 Vol II / ICAO Doc 9432"
  },
  {
    "topic": "Readability scale",
    "difficulty": "easy",
    "question": "If ATC transmits: 'VT-ABC, READ YOU FIVE', what does this communicate to the pilot?",
    "options": [
      "Transmission is perfectly readable",
      "Transmission is received on frequency band 5",
      "Transmission has 5 seconds of delay",
      "Transmission is readable now and then"
    ],
    "answerIndex": 0,
    "explanation": "'Read you 5' refers to the maximum score on the 1-to-5 readability scale, meaning reception is perfectly clear and readable.",
    "source": "ICAO Doc 9432 / WPC RTR(A)"
  },

  # Distress and urgency calls
  {
    "topic": "Distress and urgency calls",
    "difficulty": "easy",
    "question": "What is the spoken distress signal indicating that an aircraft is threatened by grave and imminent danger and requests immediate assistance?",
    "options": [
      "MAYDAY (spoken three times)",
      "PAN PAN (spoken three times)",
      "EMERGENCY (spoken three times)",
      "SECURITY (spoken three times)"
    ],
    "answerIndex": 0,
    "explanation": "MAYDAY (derived from French 'm'aider', help me) spoken three times is the international aeronautical distress signal. It has absolute priority over all other radio communications.",
    "source": "ICAO Annex 10 Vol II / ICAO Doc 9432 Chapter 8"
  },
  {
    "topic": "Distress and urgency calls",
    "difficulty": "easy",
    "question": "What is the radiotelephony urgency signal spoken to indicate a condition concerning the safety of an aircraft or person on board, but not requiring immediate assistance?",
    "options": [
      "PAN PAN (spoken three times)",
      "MAYDAY (spoken three times)",
      "ATTENTION (spoken three times)",
      "STANDBY EMERGENCY"
    ],
    "answerIndex": 0,
    "explanation": "PAN PAN (from French 'panne', breakdown) spoken three times indicates an urgency condition concerning the safety of an aircraft, vehicle, or person, but not requiring immediate assistance.",
    "source": "ICAO Annex 10 Vol II / ICAO Doc 9432 Chapter 8"
  },
  {
    "topic": "Distress and urgency calls",
    "difficulty": "medium",
    "question": "What phraseology is transmitted by an aeronautical station to impose radio silence on all stations during an ongoing distress situation?",
    "options": [
      "STOP TRANSMITTING, MAYDAY",
      "SEELONCE MAYDAY",
      "EMERGENCY SILENCE NOW",
      "CLEAR THE FREQUENCY"
    ],
    "answerIndex": 0,
    "explanation": "Under international radiotelephony standards (ICAO Doc 9432), an aircraft or controlling station may impose silence on interference using the words: 'STOP TRANSMITTING, MAYDAY' or 'SEELONCE MAYDAY'.",
    "source": "ICAO Doc 9432 'Manual of Radiotelephony' Chapter 8"
  },

  # Transponder codes (SSR)
  {
    "topic": "Transponder codes",
    "difficulty": "easy",
    "question": "What Secondary Surveillance Radar (SSR) transponder code indicates a general airborne emergency (MAYDAY)?",
    "options": [
      "Code 7700",
      "Code 7600",
      "Code 7500",
      "Code 2000"
    ],
    "answerIndex": 0,
    "explanation": "SSR Mode A Code 7700 is the international emergency code, alerting all ATC radar displays to a state of distress or emergency.",
    "source": "ICAO Doc 8168 / DGCA CAR Section 9"
  },
  {
    "topic": "Transponder codes",
    "difficulty": "easy",
    "question": "What SSR transponder code must a pilot squawk upon experiencing total two-way radio communications failure?",
    "options": [
      "Code 7600",
      "Code 7700",
      "Code 7500",
      "Code 1200"
    ],
    "answerIndex": 0,
    "explanation": "SSR Code 7600 signifies radio communication failure (lost communications). Memory aid: '76 - radio nix'.",
    "source": "ICAO Doc 8168 / DGCA CAR Section 9"
  },
  {
    "topic": "Transponder codes",
    "difficulty": "easy",
    "question": "What SSR transponder code signifies unlawful interference (hijacking)?",
    "options": [
      "Code 7500",
      "Code 7600",
      "Code 7700",
      "Code 7000"
    ],
    "answerIndex": 0,
    "explanation": "SSR Code 7500 notifies ATC covertly of unlawful interference / hijacking. Memory aid: '75 - taken alive'.",
    "source": "ICAO Doc 8168 / DGCA CAR Section 9"
  },

  # ATC clearances and readback
  {
    "topic": "ATC clearances and readback",
    "difficulty": "medium",
    "question": "Which of the following ATC instructions must ALWAYS be read back in full by the flight crew?",
    "options": [
      "Runway in use, altimeter settings (QNH), level instructions, heading instructions, and transponder codes",
      "Weather observations and wind speed reports",
      "Airport facility operating hours",
      "Names of surrounding airspace sectors"
    ],
    "answerIndex": 0,
    "explanation": "ICAO Annex 11 strictly mandates full readback of safety-critical elements: runway in use, clearance to enter/land/takeoff/hold short of any runway, level instructions (altitudes, flight levels), heading and speed instructions, altimeter settings (QNH), and SSR transponder codes.",
    "source": "ICAO Annex 11 / Doc 9432 Chapter 2"
  },

  # Frequency management & Propagation
  {
    "topic": "Frequency management",
    "difficulty": "easy",
    "question": "What is the internationally designated VHF Aeronautical Emergency Frequency?",
    "options": [
      "121.500 MHz",
      "243.000 MHz",
      "123.450 MHz",
      "118.000 MHz"
    ],
    "answerIndex": 0,
    "explanation": "121.500 MHz is the international civil aeronautical emergency frequency guarded continuously by ATC and flight crews.",
    "source": "ICAO Annex 10 Vol V / WPC RTR(A)"
  },
  {
    "topic": "VHF propagation basics",
    "difficulty": "hard",
    "question": "What is the approximate theoretical line-of-sight VHF communication range (in nautical miles) between an aircraft cruising at 10,000 ft and a ground station located at sea level (0 ft)?",
    "options": [
      "Approximately 123 NM",
      "Approximately 60 NM",
      "Approximately 250 NM",
      "Approximately 300 NM"
    ],
    "answerIndex": 0,
    "explanation": "VHF range formula is: Maximum Range (NM) = 1.23 * (√H1 + √H2), where H is height in feet. Range = 1.23 * (√10,000 + √0) = 1.23 * 100 = 123 Nautical Miles.",
    "source": "ICAO Doc 9432 / WPC RTR(A) Radio Theory"
  }
]

# ADDITIONAL VERIFIED QUESTIONS

MORE_MET = [
  {
    "topic": "Clear Air Turbulence",
    "difficulty": "hard",
    "question": "What is the primary indicator of severe mountain waves (lee waves) to an approaching pilot?",
    "options": [
      "Stationary lens-shaped Altocumulus lenticularis clouds over crests and Rotor clouds (Roll clouds) in the turbulent zone beneath the crests",
      "Dense cirrostratus overcast extending for 500 nautical miles",
      "Heavy continuous drizzle over the leeward valleys",
      "Sudden drops in ambient barometric pressure exceeding 50 hPa"
    ],
    "answerIndex": 0,
    "explanation": "Mountain waves form when stable air flows across a mountain barrier at >20-25 kt perpendicular to the ridge. The principal visual cues are Altocumulus lenticularis (standing lens-shaped clouds) at the crests and dangerous turbulent Rotor (Roll) clouds beneath the wave crests.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 13 'Mountain Waves'"
  },
  {
    "topic": "Temperature & Heat",
    "difficulty": "medium",
    "question": "A subsidence inversion is typically formed by:",
    "options": [
      "Slowly sinking and adiabatically compressing air within a high-pressure anticyclone",
      "Nocturnal radiation cooling of the earth surface on a winter night",
      "Warm air being forced over a cold mountain slope",
      "Advection of polar air over warm tropical waters"
    ],
    "answerIndex": 0,
    "explanation": "Subsidence inversions form in anticyclones (high pressure systems) where air gently sinks over a wide area. As it descends, it is adiabatically compressed and heated, becoming warmer than the air layer immediately beneath it.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 3 'Temperature Inversions'"
  },
  {
    "topic": "Winds",
    "difficulty": "medium",
    "question": "How does the Coriolis force vary with latitude from the Equator to the Poles?",
    "options": [
      "Zero at the Equator and reaches maximum magnitude at the Poles",
      "Maximum at the Equator and decreases to zero at the Poles",
      "Constant at all latitudes regardless of earth rotation",
      "Directly proportional to longitude rather than latitude"
    ],
    "answerIndex": 0,
    "explanation": "Coriolis acceleration is given by 2 * omega * V * sin(latitude). Because sin(0°) = 0, Coriolis force is zero at the Equator, and because sin(90°) = 1, it reaches maximum at the North and South Poles.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 8 'Winds'"
  },
  {
    "topic": "Climatology of India",
    "difficulty": "medium",
    "question": "Violent pre-monsoon convective thunderstorms occurring in West Bengal, Bihar, and Assam during April and May are locally termed:",
    "options": [
      "Nor'westers (Kalbaishakhi)",
      "Andhi",
      "Loo",
      "Elephantas"
    ],
    "answerIndex": 0,
    "explanation": "In West Bengal and Bangladesh, severe pre-monsoon thunderstorms originating from the northwest during the hot season (April-May) are known as Nor'westers or Kalbaishakhi. They produce severe squalls, heavy rain, lightning, and hail.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 16 'Climatology of India'"
  },
  {
    "topic": "Climatology of India",
    "difficulty": "easy",
    "question": "The hot, dry, dust-raising summer wind blowing across the plains of northern India during May and June is known as:",
    "options": [
      "Loo",
      "Mistral",
      "Sirocco",
      "Pampero"
    ],
    "answerIndex": 0,
    "explanation": "The 'Loo' is a strong, gusty, hot, and dry summer wind from the west which blows over the Indo-Gangetic Plain region of North India during May and June, with temperatures often exceeding 45°C.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 16 'Climatology of India'"
  },
  {
    "topic": "Meteorological Services & Codes",
    "difficulty": "easy",
    "question": "In a TAF, what probability percentage values are officially permitted by ICAO and DGCA for forecasting weather phenomena?",
    "options": [
      "PROB30 and PROB40 only",
      "PROB10, PROB20, PROB50, and PROB80",
      "Any probability percentage between 10% and 90%",
      "PROB25 and PROB75 only"
    ],
    "answerIndex": 0,
    "explanation": "Under ICAO Annex 3 and DGCA regulations, only PROB30 (30% probability) and PROB40 (40% probability) may be used in TAFs to describe the probability of alternative weather conditions. Conditions with 50% or higher probability are stated using BECMG, TEMPO, or FM.",
    "source": "I.C. Joshi Aviation Meteorology, Chapter 18 'Meteorological Services & Codes'"
  }
]

MORE_TG = [
  # Airspeed Definitions
  {
    "topic": "Airspeed Definitions",
    "difficulty": "easy",
    "question": "Calibrated Airspeed (CAS) is defined as:",
    "options": [
      "Indicated Airspeed (IAS) corrected for instrument and position (pressure) errors",
      "True Airspeed (TAS) corrected for wind drift",
      "Equivalent Airspeed (EAS) corrected for compressibility effects",
      "Groundspeed corrected for magnetic track deviation"
    ],
    "answerIndex": 0,
    "explanation": "Calibrated Airspeed (CAS) is Indicated Airspeed (IAS) corrected for instrument manufacturing tolerances and position/pressure error caused by the placement of the pitot tube and static ports.",
    "source": "Oxford ATPL Instrumentation / Airspeed Definitions"
  },
  {
    "topic": "Airspeed Definitions",
    "difficulty": "medium",
    "question": "For a constant Indicated Airspeed (IAS) in standard atmosphere, how does True Airspeed (TAS) change as an aircraft climbs to higher altitude?",
    "options": [
      "TAS increases at approximately 1.5% to 2% per 1,000 feet of altitude gain",
      "TAS decreases because temperature drops",
      "TAS remains constant because the dynamic pressure is unchanged",
      "TAS increases by 10% per 1,000 feet up to the tropopause"
    ],
    "answerIndex": 0,
    "explanation": "Dynamic pressure q = 1/2 * rho * TAS^2 = 1/2 * rho_0 * IAS^2. As altitude increases, air density (rho) decreases; therefore, to produce the same indicated dynamic pressure, TAS must increase (rule of thumb: ~2% per 1,000 ft).",
    "source": "Oxford ATPL Principles of Flight / Airspeed Definitions"
  },
  {
    "topic": "Airspeed Definitions",
    "difficulty": "hard",
    "question": "Equivalent Airspeed (EAS) is Calibrated Airspeed (CAS) corrected for:",
    "options": [
      "Compressibility error of air at high speeds and high altitudes",
      "Instrument friction and mechanical linkage play",
      "Altimeter temperature deviation",
      "Sideslip and rudder deflection angles"
    ],
    "answerIndex": 0,
    "explanation": "At high speeds (Mach > 0.3) and high altitudes, air compresses ahead of the pitot tube, causing CAS to overread. Correcting CAS for adiabatic compressibility error yields Equivalent Airspeed (EAS).",
    "source": "Oxford ATPL Instrumentation / Airspeed Definitions"
  },

  # Principles of Flight
  {
    "topic": "Principles of Flight",
    "difficulty": "easy",
    "question": "What is the critical (stall) angle of attack of an aerofoil?",
    "options": [
      "The angle of attack at which maximum lift coefficient (CLmax) is produced and beyond which airflow separates smoothly",
      "The pitch attitude of the fuselage relative to the horizon",
      "The angle between the chord line and the longitudinal datum axis",
      "The angle of climb during engine failure at takeoff"
    ],
    "answerIndex": 0,
    "explanation": "The critical angle of attack (stalling angle) is the angle of attack at which the aerofoil generates its maximum lift coefficient (CLmax). Increasing angle of attack beyond this point causes widespread airflow separation and a catastrophic loss of lift, regardless of airspeed, aircraft weight, or bank angle.",
    "source": "Oxford ATPL Principles of Flight / Stalling"
  },
  {
    "topic": "Principles of Flight",
    "difficulty": "medium",
    "question": "When an aircraft enters 'ground effect' during landing (within approximately one wingspan of the ground), what aerodynamic changes occur?",
    "options": [
      "Induced drag decreases significantly, effective lift increases, and the aircraft tends to float",
      "Parasite drag increases dramatically and stall speed rises by 20%",
      "Induced drag increases causing rapid settling onto the runway",
      "The elevator loses all aerodynamic effectiveness"
    ],
    "answerIndex": 0,
    "explanation": "Near the ground (within one wingspan), the physical ground restricts the formation of wingtip vortices and downwash. This reduces induced drag substantially, increases effective lift curve slope, and creates a floating tendency.",
    "source": "Oxford ATPL Principles of Flight / Ground Effect"
  },
  {
    "topic": "Principles of Flight",
    "difficulty": "hard",
    "question": "What are the standard control inputs required to recover an aircraft from an intentional or unintentional spin?",
    "options": [
      "Throttle to IDLE, Ailerons NEUTRAL, apply FULL OPPOSITE RUDDER, and smoothly ease forward control column to break the stall",
      "Apply full power and pull back forcefully on the control column",
      "Apply full in-spin aileron with neutral rudder",
      "Extend full flaps and maintain full nose-up elevator"
    ],
    "answerIndex": 0,
    "explanation": "Standard spin recovery (PARE procedure): 1) Power to IDLE; 2) Ailerons NEUTRAL; 3) Rudder FULL OPPOSITE to spin direction; 4) Elevator FORWARD smoothly past neutral to break the wing stall; and once rotation stops, neutralize rudder and recover smoothly from the dive.",
    "source": "Oxford ATPL Principles of Flight / Spins & Stalls"
  },

  # Piston Engines & Fuel Systems
  {
    "topic": "Piston Engines",
    "difficulty": "easy",
    "question": "What is the primary difference between supercharging and turbocharging in aircraft piston engines?",
    "options": [
      "A supercharger is mechanically driven directly by the engine crankshaft, whereas a turbocharger is driven by engine exhaust gases",
      "A supercharger uses exhaust gas while a turbocharger is electric",
      "A supercharger operates only at sea level while turbochargers work only above 30,000 ft",
      "Superchargers inject nitrous oxide while turbochargers inject water"
    ],
    "answerIndex": 0,
    "explanation": "A supercharger is mechanically coupled via gears directly to the engine crankshaft (consuming engine power). A turbocharger uses the otherwise wasted kinetic and thermal energy of exhaust gases passing through a turbine to drive an intake compressor.",
    "source": "Oxford ATPL Aircraft General Knowledge / Piston Engines"
  },
  {
    "topic": "Piston Engines",
    "difficulty": "medium",
    "question": "What is 'vapour lock' in an aircraft fuel system?",
    "options": [
      "Vaporization of aviation fuel in lines or pumps caused by low ambient pressure, high temperature, or excessive suction, blocking liquid fuel flow",
      "Condensation of ambient water vapor freezing the fuel filter screen",
      "Hydraulic lock of engine cylinders caused by unburned avgas during priming",
      "Locking of the fuel tank filler cap due to negative pressure differential"
    ],
    "answerIndex": 0,
    "explanation": "Vapour lock occurs when fuel vaporizes prematurely in fuel delivery lines or pumps due to high temperatures, low ambient atmospheric pressure at altitude, or excessive line suction, creating gas bubbles that block liquid fuel delivery to the engine.",
    "source": "Oxford ATPL Aircraft General Knowledge / Fuel Systems"
  },

  # Electrical Systems & Instruments
  {
    "topic": "Aircraft Systems",
    "difficulty": "medium",
    "question": "What is the primary function of a Transformer Rectifier Unit (TRU) in an aircraft electrical system?",
    "options": [
      "To step down high-voltage AC electrical power and convert it into DC electrical power",
      "To convert DC battery power into 115V 400Hz AC power",
      "To regulate alternator field current during sudden electrical load shedding",
      "To prevent electrostatic discharge during in-cloud flight"
    ],
    "answerIndex": 0,
    "explanation": "A Transformer Rectifier Unit (TRU) transforms high-voltage Alternating Current (typically 115V AC) down to a lower voltage and rectifies it into Direct Current (typically 28V DC) to supply DC consumer buses and charge batteries.",
    "source": "Oxford ATPL Aircraft General Knowledge / Electrical Systems"
  },
  {
    "topic": "Gyroscopic Instruments",
    "difficulty": "medium",
    "question": "In an aircraft turn coordinator, the gyro gimbal is tilted upward at approximately 30 degrees. This enables the instrument to sense:",
    "options": [
      "Both rate of roll and rate of yaw",
      "Rate of yaw only, without any roll sensitivity",
      "Rate of pitch and angle of bank only",
      "Pure magnetic heading changes"
    ],
    "answerIndex": 0,
    "explanation": "Unlike the older Turn and Slip indicator (horizontal gimbal sensing yaw only), the modern Turn Coordinator has its gyro gimbal tilted up ~30° from the horizontal axis. This allows the gyro to precess in response to both rate of roll and rate of yaw.",
    "source": "Oxford ATPL Instrumentation / Gyroscopes"
  }
]

MORE_TS = [
  # V-speeds and their meanings
  {
    "topic": "V-speeds and their meanings",
    "difficulty": "easy",
    "question": "What does the abbreviation 'Vno' represent?",
    "options": [
      "Maximum structural cruising speed (normal operating limit)",
      "Never exceed speed",
      "Design maneuvering speed",
      "Stall speed in clean configuration"
    ],
    "answerIndex": 0,
    "explanation": "Vno is the maximum structural cruising speed. Airspeeds up to Vno are safe for flight in rough or turbulent air; speeds above Vno enter the caution (yellow) range and are only permissible in smooth air.",
    "source": "Aircraft Flight Manual / POH Section 2 'Limitations'"
  },
  {
    "topic": "V-speeds and their meanings",
    "difficulty": "easy",
    "question": "What does the red radial line on an Airspeed Indicator indicate?",
    "options": [
      "Vne: Never exceed speed",
      "Vs0: Stall speed landing configuration",
      "Vno: Maximum cruising speed",
      "Vfe: Flap extension speed limit"
    ],
    "answerIndex": 0,
    "explanation": "The red radial line marks Vne (Never Exceed speed). Flying above Vne risks immediate structural failure or control flutter under any atmospheric conditions.",
    "source": "Aircraft Flight Manual / POH Section 2 'Limitations'"
  },
  {
    "topic": "V-speeds and their meanings",
    "difficulty": "hard",
    "question": "On a multi-engine aircraft, which engine is defined as the 'critical engine' on a conventional twin with both propellers rotating clockwise (as viewed from the cockpit)?",
    "options": [
      "The left engine, because its failure creates the greatest adverse yaw and roll due to P-factor, accelerated slipstream, and torque",
      "The right engine, because its exhaust heats the cabin heater exchanger",
      "Either engine equally because thrust vectors are symmetric",
      "The engine equipped with the primary hydraulic pump"
    ],
    "answerIndex": 0,
    "explanation": "On aircraft where both propellers rotate clockwise, the descending blade on the right side of each engine creates thrust further to the right. The right engine thrust vector acts with a much longer arm from the fuselage centerline than the left. Therefore, failure of the LEFT engine induces the greatest yaw and roll, making it the critical engine.",
    "source": "Multi-Engine Flying Manual / DGCA Multi-Engine Syllabus"
  },

  # Fuel, Weight & Systems
  {
    "topic": "Fuel grades and colors",
    "difficulty": "easy",
    "question": "What is the consequence of fueling an aircraft engine rated for 100LL AVGAS with 80/87 octane aviation fuel?",
    "options": [
      "Severe risk of detonation, engine overheating, and catastrophic cylinder failure under high power settings",
      "Engine will fail to start under cold weather conditions",
      "Fuel will immediately freeze in the carburettor nozzle",
      "Spark plugs will suffer rapid lead fouling"
    ],
    "answerIndex": 0,
    "explanation": "Using fuel with a lower octane rating than specified by the engine manufacturer will cause severe detonation (uncontrolled knocking combustion) at high power settings, causing rapid cylinder head overheating, piston erosion, and engine failure.",
    "source": "Aircraft Flight Manual / POH Section 2 'Limitations'"
  },
  {
    "topic": "Weight limits",
    "difficulty": "easy",
    "question": "What is the difference between Maximum Ramp Weight and Maximum Takeoff Weight (MTOW)?",
    "options": [
      "Maximum Ramp Weight includes the allowance for fuel burned during engine startup, warmup, and taxi to the runway",
      "Maximum Ramp Weight is the maximum permissible landing weight",
      "Maximum Ramp Weight is always lower than MTOW due to strut compression",
      "There is no difference between the two terms"
    ],
    "answerIndex": 0,
    "explanation": "Maximum Ramp Weight is the structural weight limit for taxiing on the ground. It is greater than Maximum Takeoff Weight by the mass of fuel expected to be consumed during engine start, run-up, and taxi to the active runway.",
    "source": "Aircraft Flight Manual / POH Section 2 'Weight & Limitations'"
  },
  {
    "topic": "POH sections",
    "difficulty": "easy",
    "question": "Which section of a standardized GAMA Pilot's Operating Handbook contains aircraft operating limitations (airspeeds, engine limits, weight and CG limits)?",
    "options": [
      "Section 2",
      "Section 1",
      "Section 3",
      "Section 7"
    ],
    "answerIndex": 0,
    "explanation": "Section 2 of every standardized GAMA POH is dedicated strictly to 'Limitations'. Compliance with the limits in Section 2 is legally mandatory under Civil Aviation Requirements.",
    "source": "GAMA Specification No. 1 / POH Standards"
  }
]

MORE_RTR = [
  # Distress, Urgency, Lost Comms
  {
    "topic": "Distress and urgency calls",
    "difficulty": "medium",
    "question": "What are the essential contents of an initial MAYDAY distress message in standard radiotelephony?",
    "options": [
      "MAYDAY (x3), Aircraft Callsign (x3), Nature of distress condition, Intentions of person in command, Present position, Level/Altitude, and Heading",
      "MAYDAY, Pilot license number, Total flight hours, and Departure airfield name",
      "MAYDAY, Fuel onboard in litres and passengers' names",
      "MAYDAY, Aircraft registration, Color of fuselage, and Engine serial number"
    ],
    "answerIndex": 0,
    "explanation": "In accordance with ICAO Doc 9432 Section 8.2: 1) Distress signal 'MAYDAY' (x3); 2) Name of station addressed; 3) Aircraft identification (x3); 4) Nature of distress; 5) Intentions of commander; 6) Present position, level, and heading; 7) Pilot qualifications / endurance / persons on board.",
    "source": "ICAO Doc 9432 Chapter 8 / WPC RTR(A)"
  },
  {
    "topic": "Distress and urgency calls",
    "difficulty": "easy",
    "question": "When an aircraft distress situation has terminated and normal radio communication can resume, what phraseology is broadcast?",
    "options": [
      "SEELONCE FEENEE",
      "MAYDAY OVER",
      "CANCEL EMERGENCY",
      "RESUME NORMAL TALKING"
    ],
    "answerIndex": 0,
    "explanation": "Under ICAO Doc 9432, when distress traffic has ceased, the station controlling the frequency broadcasts: '[Aircraft/Station Callsign], ALL STATIONS, SEELONCE FEENEE', followed by the time, permitting normal transmissions to resume.",
    "source": "ICAO Doc 9432 Chapter 8 / WPC RTR(A)"
  },
  {
    "topic": "ATC clearances and readback",
    "difficulty": "medium",
    "question": "What is the standard phraseology used by a pilot to correct an error made during their own ongoing radiotelephony transmission?",
    "options": [
      "CORRECTION, followed by the last correct phrase or word, and then the correct version",
      "MISTAKE, CANCEL LAST",
      "DISREGARD LAST SENTENCE",
      "WRONG, STANDBY"
    ],
    "answerIndex": 0,
    "explanation": "ICAO Doc 9432 specifies: 'CORRECTION: An error has been made in this transmission (or message indicated). The correct version is...'",
    "source": "ICAO Doc 9432 Chapter 2 'General Operating Procedures'"
  },
  {
    "topic": "ATIS",
    "difficulty": "easy",
    "question": "How are successive Automatic Terminal Information Service (ATIS) airport broadcasts identified by flight crews?",
    "options": [
      "By consecutive letters of the ICAO phonetic alphabet (Information Alpha, Information Bravo, Information Charlie, etc.)",
      "By military Zulu hour codes (e.g. Broadcast 0100, Broadcast 0200)",
      "By sequential numbers (e.g. ATIS 1, ATIS 2)",
      "By the duty air traffic controller's operating initials"
    ],
    "answerIndex": 0,
    "explanation": "Under ICAO Annex 11, each successive ATIS message is identified by a code letter assigned in alphabetical sequence (Alpha, Bravo, Charlie, etc.), advancing to the next letter with each new broadcast issuance.",
    "source": "ICAO Annex 11 / Doc 9432 Chapter 5"
  },
  {
    "topic": "Lost communication procedures",
    "difficulty": "hard",
    "question": "Under ICAO and DGCA regulations, if an IFR aircraft encounters complete two-way radio failure in Instrument Meteorological Conditions (IMC), what level and route must it maintain?",
    "options": [
      "Maintain the last assigned level and speed for 20 minutes following failure to report over a compulsory reporting point, then adjust level and speed in accordance with the filed flight plan, adhering strictly to the current flight plan route",
      "Immediately descend to minimum safe altitude and land at the nearest non-towered airstrip",
      "Climb immediately to FL410 to ensure line-of-sight radar contact",
      "Turn 90 degrees right of course and hold until fuel exhaustion"
    ],
    "answerIndex": 0,
    "explanation": "ICAO Annex 2 Rule 3.6.5.2 mandates that in IMC (or when weather prevents VMC landing), an aircraft with communication failure shall: maintain the last assigned speed and level (or minimum flight altitude if higher) for 20 minutes following the failure to report over a compulsory reporting point, and thereafter adjust level and speed according with the filed flight plan, flying the assigned or filed route to the destination IAF.",
    "source": "ICAO Annex 2 'Rules of the Air' / DGCA CAR Section 9"
  }
]

MET_NEW_QUESTIONS.extend(MORE_MET)
TG_NEW_QUESTIONS.extend(MORE_TG)
TS_NEW_QUESTIONS.extend(MORE_TS)
RTR_NEW_QUESTIONS.extend(MORE_RTR)
