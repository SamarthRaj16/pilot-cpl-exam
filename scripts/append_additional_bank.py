# -*- coding: utf-8 -*-
import os
import sys

BASE = r"c:\VS Code\Codes\dgcacpllearning"
target_file = os.path.join(BASE, "scripts", "build_met_tg_ts_rtr_bank.py")

more_code = '''
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
'''

with open(target_file, "a", encoding="utf-8") as f:
    f.write(more_code)

print("Appended additional verified questions successfully!")

