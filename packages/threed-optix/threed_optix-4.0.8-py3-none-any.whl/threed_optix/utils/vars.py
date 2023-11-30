import numpy as np
import pkg_resources

VALID_RESPONSE_CODES = [200, 201, 202, 204]

#Base API URL
API_URL = "https://api.3doptix.com/v1"

#GET endpoints
GET_SETUPS_ENDPOINT = 'setups'
GET_SETUP_ENDPOINT = 'setups/{setup_id}'
GET_PART_ENDPOINT = 'setups/{setup_id}/parts/{part_id}'

#PUT endpoints
PUT_BATCH_CHANGES_ENDPOINT = "setups/{setup_id}/batch_changes"
PUT_ANALYSIS_ENDPOINT = 'setups/{setup_id}/run_analyses'
PUT_SIMULATION_ENDPOINT = 'setups/{setup_id}/simulation'

#SET endpoints
SET_PART_ENDPOINT = 'setups/{setup_id}/parts/{part_id}'

#POST endpoints
POST_ADD_ANALYSIS_ENDPOINT = "setups/{setup_id}/parts/{part_id}/add_analyses"

#Snellius version: must be compatible
SNELLIUS_VERSION = "2.2.23"
GPU_TYPE = "g4"

#Messages and warnings
SET_API_URL_WARNING = "Are you sure you want to change the API URL? This is internal option and should not be used by users."
SERVER_DOWN_MESSAGE = "The server is down. Please try again later."

WELCOME_MESSAGE = f"Welcome to 3DOptix! 🌈 You are now being connected to the 3DOptix API (version {pkg_resources.get_distribution('threed_optix').version}). Let's start!"

#Analysis
##Analysis file decoding format
ANALYSIS_HEADER_DTYPES = np.dtype([
        ('magic number', np.int32),
        ('analysis kind', np.int32),
        ('data kind', np.int32),
        ('polarization kind', np.int32),
        ('version', np.int32),
        ('num_hits', np.int64),
        ('num_wavelengths', np.int32),
        ('resolution_x', np.int32),
        ('resolution_y', np.int32),
    ])

ANALYSIS_MATRIX_DTYPES = np.float32
HEADER_BYTES = 40

##Analysis headers mappings
DATA_KINDS_MAPPING = {
    0: 'SPOT_INCOHERENT_IRRADIANCE_S',
    1: 'SPOT_INCOHERENT_IRRADIANCE_P',
    2: 'SPOT_COHERENT_IRRADIANCE_S',
    3: 'SPOT_COHERENT_IRRADIANCE_P',
    4: 'SPOT_COHERENT_PHASE_S',
    5: 'SPOT_COHERENT_PHASE_P',
    6: 'SPOT_INCOHERENT_IRRADIANCE',
    7: 'SPOT_COHERENT_IRRADIANCE',
    8: 'SPOT_COHERENT_PHASE',
}

POLARIZATION_MAPPING = {
    0: 'NONE_POLARIZATION',
    1: 'X_POLARIZATION',
    2: 'Y_POLARIZATION',
    3: 'Z_POLARIZATION',
}

##Fast analysis valid names
FAST_ANALYSIS_NAMES = [
    "Spot (Incoherent Irradiance)",
    "Spot (Incoherent Irradiance) Through Focus",
    "Grid Distortion",
    "Distortion & Field Curvature",
    "OPD (Optical Path Difference)",
    "Ray Abberations (TRA and LRA)",
    "Polarization Map"
]
ADVANCED_ANALYSIS_NAMES = [
    "Spot (Incoherent Irradiance)",
    "Spot (Coherent Irradiance)",
    "Coherent Phase",
    "Spot (Coherent Irradiance) Huygens",
    "Coherent Phase Huygens",
    "Spot (Coherent Irradiance) Fresnel",
    "Coherent Phase Fresnel",
    "Spot (Coherent Irradiance) Polarized",
    "Coherent Phase Polarized",
    "Spot (Incoherent Irradiance) Polarized"
]

ANALYSIS_NAMES =  [
    "Spot (Incoherent Irradiance)",
    "Spot (Coherent Irradiance)",
    "Coherent Phase",
    "Spot (Coherent Irradiance) Huygens",
    "Coherent Phase Huygens",
    "Spot (Coherent Irradiance) Polarized",
    "Coherent Phase Polarized",
    "Spot (Incoherent Irradiance) Polarized"
]

## Errors
#simulation errors
SIMULATION_ERROR = """Simulation failed (server side).\n Error message: "{message}"."""

#Analyses errors
ANALYSES_ADD_ERROR = "Analyses {not_added} were not added. Please add them first"
ANALYSES_NOT_SAME_SETUP_ERROR = f"Analyses must be from the same setup."
ANALYSIS_RUN_ERROR = """Analyses failed (server side).\n Error message: "{message}"."""
ANALYSES_DUPLICATED_ERROR = """Analyses with ids {duplicated} are duplicated.\nYou can use the existing analyses with the same parameters or force this action by setting 'force' argument to True"""

COLOR_SCALE = [
    [0.0, '#0000FF'],
    [0.25, '#00FF00'],
    [0.5, 'yellow'],
    [0.75, 'orange'],
    [1.0, '#FF0000']
]
