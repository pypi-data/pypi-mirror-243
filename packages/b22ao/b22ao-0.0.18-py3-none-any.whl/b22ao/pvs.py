
AD_PVBASE = "BL22B-DI-CAM-10"  # Area Detector

DM1_PVBASE = "BL22B-OP-ALPAO-01"  # Deformable mirror 1
DM2_PVBASE = "BL22B-OP-ALPAO-02"  # Deformable mirror 2


AD_ARRAY_COUNTER = "PVA:UniqueId_RBV"  # Frame counter
AD_ACQUIRE = "CAM:Acquire"  # Acquire button - write with 'Acquire'
AD_GAIN = "CAM:Gain_RBV"  # Gain set on Windows app
AD_SHUTTER_STATE = "CAM:SHUTTER_RBV"
AD_ARRAY_DATA = "PVA:ARRAY" # Structured data - use p4p calls
AD_IMAGE_MODE = "CAM:ImageMode"
AD_IMAGE_MODE_SINGLE = "Single"

DM_ACTUATOR_PREFIX = "ACT"  # individual actuator pv: pv base + ACT + actuator number
DM_ACTUATOR_SETPOINT = ":SP"
DM_APPLY_MASK = "CP_ST_TO_ACT.PROC"

'''
The following PV is a gate signal used to allow/inhibit acquisitions.
The signal responds to topup events, beam dump, and a manual override.
PV values: 0 = disallow; 1 = allow

Note that this is not the exact PV accessible via the EPICS screen.
That PV adjusts this result to the specific endstation in use (the
signal is inverted for one of them). The PV in use here is the
endstation-independent result of their gating logic.
'''
ALLOW_ACQUISITION = "BL22B-EA-FTIR-02:CALC"