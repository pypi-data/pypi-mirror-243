import requests
from colorama import init, Fore, Style
import time
import json
import math
import numpy as np
from threed_optix.utils import vars as v
import pandas as pd
import threed_optix.utils.math as mu
import copy


def verify_response(response):
    if int(response.status_code) not in v.VALID_RESPONSE_CODES:
        raise Exception(f'Error: {response.status_code} - {response.text}')
    return None


#General Purpose
def _healthcheck():
    """
    Checks if the server is up and well.
    """
    url = f'{v.API_URL}/healthcheck'

    r = requests.get(url)
    verify_response(r)
    r = r.json()
    return (r['status'] == 'SUCCESS', r['message'])

#API Endpoints
##General
def _get(
    endpoint: str,
    api_key: str,
    #payload: dict = {}
    ):
    """
    Sends a GET request to the endpoint with the API key.

    Args:
        endpoint (str): The endpoint to send the request to.
        api_key (str): The API key.

    Returns:
        dict: The response JSON.
    """
    url = f'{v.API_URL}/{endpoint}'
    headers = {'X-API-KEY': api_key}
    r = requests.get(url, headers=headers)
    verify_response(r)
    r = r.json()
    return (r['data'] if 'status' in r and r['status'] == 'SUCCESS' else None, r['message'])

def _put(endpoint: str, api_key: str, json_data: dict = None):
    """
    Sends a PUT request to the endpoint.

    Args:
        endpoint (str): The endpoint to send the request to.
        json_data (dict): The JSON payload for the request.
        api_key (str): The API key.
    """
    url = f'{v.API_URL}/{endpoint}'
    headers = {'X-API-Key': api_key, 'Content-Type': 'application/json'}
    r = requests.put(url, headers=headers, json=json_data)
    verify_response(r)
    r = r.json()
    return (r['data'] if 'status' in r and r['status'] == 'SUCCESS' else None, r['message'])

def _set(endpoint, data, api_key):
    url = f'{v.API_URL}/{endpoint}'
    headers = {'X-API-KEY': api_key}

    r = requests.post(url, headers=headers, json=data)
    verify_response(r)
    r = r.json()
    return ('status' in r and r['status'] == 'SUCCESS', r['message'])

def _post(endpoint, data, api_key):
    url = f'{v.API_URL}/{endpoint}'
    headers = {'X-API-KEY': api_key}

    r = requests.post(url, headers=headers, json=data)
    verify_response(r)
    r = r.json()
    return ('status' in r and r['status'] == 'SUCCESS', r['message'])

##Setups
def _get_setups(api_key: str):
    """
    Returns the list of setup names and ids of the user.

    Args:
        api_key (str): The API key.

    Returns:
        list: A list of setup names and ids.
    """
    endpoint = v.GET_SETUPS_ENDPOINT
    response = _get(endpoint, api_key)

    return response

def _get_setup(
    setup_id: str,
    api_key: str
    ):
    """
    Returns the opt file for the specified setup id.

    Args:
        setup_id (str): The setup id.
        api_key (str): The API key.

    Returns:
        str: The opt file content.
    """

    endpoint = v.GET_SETUP_ENDPOINT.format(setup_id=setup_id)

    return _get(endpoint, api_key)
    #return _dummy_opt()

##Parts
def _get_part(setup_id: str, part_id: str, api_key: str):
    endpoint = v.GET_PART_ENDPOINT.format(setup_id=setup_id, part_id=part_id)
    part =  _get(endpoint, api_key)
    return part

def _set_part(setup_id, part_id, data, api_key):
    data_copy = copy.deepcopy(data)
    data_copy['pose']['rotation'] =[mu.deg_to_rad(x) for x in data_copy['pose']['rotation']]
    endpoint = v.SET_PART_ENDPOINT.format(setup_id=setup_id, part_id=part_id)
    r = _set(endpoint, data_copy, api_key)
    return r

##Run Simulations
def _run_async(setup_id, api_key):
    endpoint =  v.PUT_SIMULATION_ENDPOINT.format(setup_id=setup_id)
    json_data = {
        "gpu_type": v.GPU_TYPE,
        "is_sync": True,
        "snellius_version": v.SNELLIUS_VERSION
    }
    r = _put(endpoint = endpoint, json_data=json_data, api_key= api_key)
    return r

def _run_batch(
    setup_id: str,
    configuration: dict,
    api_key: str):
    """
    Puts the batch run request.

    Args:
        setup_id (str): The setup id.
        configuration (dict): The batch configuration.
        api_key (str): The API key.
    """
    endpoint = v.PUT_BATCH_CHANGES_ENDPOINT.format(setup_id=setup_id)
    return _put(endpoint = endpoint, api_key= api_key, json_data = configuration)

def _run_simulation(setup_id, api_key, is_sync = True):
    endpoint =  v.PUT_SIMULATION_ENDPOINT.format(setup_id=setup_id)
    json_data = {
        "gpu_type": v.GPU_TYPE,
        "is_sync": is_sync,
        "snellius_version": v.SNELLIUS_VERSION
    }
    r = _put(endpoint = endpoint, json_data=json_data, api_key= api_key)
    return r

##Analyses
def _add_analyses(setup_id, part_id, data, api_key):
    endpoint = v.POST_ADD_ANALYSIS_ENDPOINT.format(setup_id=setup_id, part_id=part_id)
    return _put(endpoint = endpoint, json_data=data, api_key = api_key)

def _run_analyses(setup_id: str, api_key: str, analyses_ids: str):

    endpoint = v.PUT_SIMULATION_ENDPOINT.format(setup_id=setup_id)

    json_data = {
        "gpu_type": v.GPU_TYPE,
        "is_sync": True,
        "analyses_to_run": analyses_ids,
        "snellius_version": v.SNELLIUS_VERSION
    }

    return _put(endpoint = endpoint, json_data = json_data, api_key = api_key)


#Others
def _set_api_url(url, are_you_sure=False):

    if not are_you_sure:
        raise Exception(v.SET_API_URL_WARNING)

    print(v.SET_API_URL_WARNING)
    print('Previous API URL was', v.API_URL)
    print('Setting API URL to', url)
    v.API_URL = url

def _welcome():

    init(autoreset=True)
    color = Fore.WHITE
    print('******************')
    for i, char in enumerate(v.WELCOME_MESSAGE):
        print(f"{color}{char}", end="")
        time.sleep(0.02)  # Adjust the delay for the desired speed

    print(Style.RESET_ALL)  # Reset the style after the rainbow effect
    print('******************')

def _map_ray_row(row, map):
    row['surface_id'] = map['surfaces'][int(row['hit_surface_idx'])]
    row['wavelength'] = map['wavelengths'][int(row['wavelength_idx'])]
    row['light_source'] = map['sources'][int(row['source_idx'])]
    del row['hit_surface_idx']
    del row['wavelength_idx']
    del row['source_idx']
    return row

def _map_ray_table(rays_url, maps_url):
    rays_df = pd.read_csv(rays_url)
    rays_df = rays_df.copy()
    maps_json = requests.get(maps_url).json()
    rays_df = rays_df.apply(lambda row: _map_ray_row(row, maps_json), axis=1)
    return rays_df
