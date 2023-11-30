import threading
import pickle
import math
import requests
import pandas as pd
import numpy as np
import random
import time
import requests
import zipfile
import os

from io import BytesIO
from typing import Any, Union, List, Tuple, Dict, Optional

import threed_optix.utils.api as au
import threed_optix.utils.vars as v
import threed_optix.utils.math as mu
import threed_optix.utils.general as gu
import threed_optix.analyses as tdo_analyses
import threed_optix.simulations as tdo_simulations

class ThreedOptixAPI:
    """
    Used to manage the communication with the server of 3DOptix.

    Args:
        api_key (str): The API key used for authentication.

    Properties:
        api_key (str): The API key of the user.
        setups (list): The list of setups of the user.
    """


    def __init__(self,
                 api_key: str,
                 verbose: bool = True
                 ):
        '''
        Initializes the API object.
        Args:
            api_key (str): The API key of the user.
            verbose (bool): If True, prints welcome message. Default is True.
        '''

        self.api_key = api_key
        self.jobs = []
        self.setups = None

        # Check if the server is up and the API key is valid
        assert self.is_up(), v.SERVER_DOWN_MESSAGE
        assert self.is_key_valid(), v.INVALID_KEY_MESSAGE

        if verbose:
            # Print welcome message
            welcome_thread = threading.Thread(target=au._welcome)
            welcome_thread.start()

        # Fetch setups from the server
        setups_thread = threading.Thread(target=self._initialize_setups)
        setups_thread.start()

        # Wait for both threads to finish
        if verbose:
            welcome_thread.join()

        # Wait for both threads to finish
        setups_thread.join()
        if self.setups is None:
            #If setups is None, it means that the API key is invalid
            raise Exception("Could not initialize setups, check your API key")

    def __contains__(self, item: Union[str, tdo_simulations.Setup]) -> bool:
        """
        Allows checking if a setup id is in the API.

        Args:
            item (tdo.Setup): The setup name, id, or object.

        Returns:
            bool: True if the setup exists, False otherwise.
        """
        contains = False
        if isinstance(item, str):
            for setup in self:
                if setup.id == item:
                    contains = True
                    break
        elif isinstance(item, tdo_simulations.Setup):
            for setup in self:
                if setup.id == item.id:
                    contains = True
                    break
        return contains

    def __len__(self) -> int:
        '''
        Returns the number of setups in the API.
        '''
        return len(self.setups)

    def __iter__(self):
        """
        Iterates over the setups of the API.
        """
        return iter(self.setups)

    def __str__(self) -> str:
        '''
        Prints the API object and the setups it contains.
        '''
        string = f"API with {len(self)} setups:\n"
        for setup in self:
            string += f"  - {setup.name} ({setup.id})\n"
        return string

    def __getitem__(self, key: str) -> tdo_simulations.Setup:
        """
        Args:
            key (str): The id of the requested setup.
        Returns:
            Setup (tdo.Setup): The requested Setup object.
        """
        # if isinstance(key, int):
        #     return self.setups[key]
        if isinstance(key, str):
            for setup in self:
                if setup.id == key:
                    return setup
            raise KeyError(f"Setup with id {key} not found.")
        raise TypeError(f"Invalid key type {type(key)}. Must be setup id.")

    def _initialize_setups(self):
        '''
        Private.
        Shouldn't be called directly. Initializes the setups property.
        '''
        self.setups = self._get_setups_info()
        if self.setups is not None:
            self.setups = [tdo_simulations.Setup._new(_api=self, setup_tuple=setup) for setup in self.setups]
        return self.setups

    def _get_setups_info(self) -> list:
        """
        Private.
        Shouldn't be called directly. Returns a list of setups info.
        """
        data, message = au._get_setups(self.api_key)
        if data is not None:
            infos = []
            for info_json in data['setups']:
                infos.append((info_json['id'], info_json['name']))
            return infos
        #else:
            #raise Exception(message)
        return None

    def _get_setup_parts(self, setup_id: str) -> list:
        '''
        Private.
        Shouldn't be called directly. Returns a list of parts of the specified setup.
        '''
        parts = au._get_setup(setup_id, self.api_key)[0]
        return parts

    def _get_part(self, part_id: str, setup_id) -> dict:
        '''
        Private.
        Shouldn't be called directly. Returns a dictionary of the specified part.
        '''
        part = au._get_part(setup_id,part_id,  self.api_key)[0]
        return part

    def _extract_setup_object(self, setup):
        '''
        Private.
        Shouldn't be called directly. Returns the setup object from the specified setup.
        '''
        if isinstance(setup, str):

            if setup in self:
                setup_object = self[setup]
                return setup_object

            elif self.get(setup) is not None:
                setup_object = self.get(setup)
                return setup_object

            else:
                raise Exception(f"Setup with id or name {setup} not found.")

        if isinstance(setup, tdo_simulations.Setup):
            return setup

        if isinstance(setup, int):
            return self.setups[setup]

        raise TypeError(f"Invalid setup type {type(setup)}. Must be Setup object, name, index or id.")

    def get(self,
            setup_name: str,
            all: bool = False
            ) -> tdo_simulations.Setup:
        """
        Returns the Setup object with the specified name.
        Args:
            setup_name (str): The name of the setup.
            all (bool): If True, returns all setups with the specified name. else, returns the first one

        Returns:
            Setup (tdo.Setup): The Setup object.
        """
        if all:
            setups = []
            for setup in self:
                if setup.name == setup_name:
                    setups.append(setup)
            return setups

        else:
            setup = None
            for s in self.setups:
                if s.name == setup_name:
                    setup = s
                    return setup

    def is_up(self) -> bool:
        """
        Calls _healthcheck and returns a boolean indicating if the server is up.

        Returns:
            bool: True if the server is up, False otherwise.
        """
        return au._healthcheck()[0]

    def is_key_valid(self):
        '''
        Not implemented yet.
        '''
        return True

    def update_part(self, setup_id, part) -> tuple:
        '''
        Modifies the part's data to the setup with that id.
        Args:
            setup_id (str): The id of the setup.
            part (Part): The part object to update.

        Returns:
            tuple: A tuple of (success, message), where:
                success (bool): True if the part was updated successfully, False otherwise.
                message (str): The message from the server.
        Raises:
            Exception: If the part was not updated successfully.
        '''
        success, message = au._set_part(setup_id, part.id, part.data, self.api_key)
        if not success:
            raise Exception(message)
        return (success, message)

    def get_setups(self) -> list:
        """
        Returns a list of Setup objects that are associated with the user.

        Returns:
            list: A list of Setup objects.
        """
        return self.setups

    def run(self,
            setup: tdo_simulations.Setup
            ) -> tdo_analyses.RayTable:
        """
        Propagate the rays in the setup and returns a RayTable object.

        Args:
            setup (tdo.Setup): The setup to run.

        Returns:
            RayTable (tdo.analyses.RayTable): The RayTable object with the results.

        Raises:
            Exception: If the simulation failed.
        """
        setup_object = self._extract_setup_object(setup)

        data, message = au._run_simulation(setup_object.id, self.api_key)

        if data == None:
            raise Exception(message)

        if data['results'][0]['error']['code'] != 0:
            raise Exception(v.SIMULATION_ERROR.format(message = data['results'][0]['error']['message']))



        if data is not None:
            ray_table = data['results'][0]['data']['ray_table']
            maps_url = data['maps_url']
            return tdo_analyses.RayTable._new(ray_table, maps_url, setup_object)
        else:
            raise Exception(message)

    def run_async(self, setup):
        '''
        Not implemented yet.
        '''
        setup_object = self._extract_setup_object(setup)
        data, message = au._run_simulation(setup_object.id, self.api_key, is_sync = False)
        if data == None:
            raise Exception(message)
        if data['results'][0]['error']['code'] != 0:
            raise Exception(v.SIMULATION_ERROR.format(message = data['results'][0]['error']['message']))

        if data is not None:
            ray_table = data['results'][0]['data']['ray_table']
            maps_url = data['maps_url']
            return tdo_analyses.RayTable._new(ray_table, maps_url, setup_object)
        else:
            raise Exception(message)

    def run_batch(self,
                  setup: tdo_simulations.Setup,
                  configuration: dict
                  ):
        """
        Not implemented yet.
        """
        response = au._run_batch(setup.id, configuration, self.api_key)
        if response[0] is not None:
            json_ = response[0]
            json_['number_of_changes'] = configuration['number_of_changes']
            json_['simulation_file_prefix'] = configuration['simulation_file_prefix']
            job = tdo_simulations.Job._from_json(response[0], _api = self, _setup = setup)
            job._url = job._url.replace('$', '')
            self.jobs.append(job)
            return job
        else:
            raise Exception(response[1])

    def run_analysis(self, analysis: tdo_analyses.Analysis, auto_add: bool = False, force: bool = False) -> bool:
        '''
        Runs the specified analysis.
        Args:
            analysis (tdo.analyses.Analysis): The analysis to run.
            auto_add (bool): If True, adds the analysis to the setup if it doesn't exist. Default is False.
            force (bool): If True, adds the analysis to the setup even if identical analysis already exists.
            Default is False.
            Each analysis stores its result seperately.
            Filling the same analysis twice will result in larger user's memory resources consumption.

        Returns:
            bool: True if the analysis was run successfully and that results are stored in analysis.results, False otherwise.

        Raises:
            Exception:
                - If force is used without auto_add.
                - If auto_add is used and the analysis was not added successfully.
                - If the server failed to respond.
        '''

        successful, failed =  self.run_analyses([analysis], auto_add = auto_add, force = force)
        if len(successful) == 1:
            return True
        return False

    def run_analyses(self, analyses, auto_add = False, force = False):
        '''
        Private.
        '''
        ids = [analysis.id for analysis in analyses]
        setup_id = analyses[0].surface._part._setup.id

        response = {'success': [], 'failed': []}

        if not all([analysis.surface._part._setup.id == setup_id for analysis in analyses]):
            raise Exception(v.ANALYSES_NOT_SAME_SETUP_ERROR)

        if not auto_add and force:
            raise Exception("Force argument can only be used with auto_add argument")

        if auto_add:
            added_successfully = []
            added_failed = []

            for analysis in analyses:
                added = self.add_analysis(analysis, force = force)
                if added:
                    added_successfully.append((analysis, analysis.id))
                else:
                    print(f"Analysis {analysis.id} was failed to be added")
                    added_failed.append((analysis, analysis.id))
            response['added'] = added_successfully
            response['failed'] += added_failed
            ids = [analysis[1] for analysis in added_successfully]

        ran_successfully = []
        ran_failed = []

        if not all([analysis._added for analysis in analyses]):
            not_added = [analysis.id if analysis._added else None for analysis in analyses]
            raise Exception(v.ANALYSES_ADD_ERROR.format(not_added = not_added))

        data, message =  au._run_analyses(setup_id, self.api_key, ids)

        if data == None:
            raise Exception(message)

        for i, analysis in enumerate(analyses):
            is_successful = data['results'][i]['error']['code'] == 0
            ran_successfully.append((analysis, analysis.id))
            if is_successful:
                analysis_datos = data['results'][i]['data']['analysis']
                for data in analysis_datos:
                    url = data['url']
                    analysis._urls.append(url)
                analysis.results = analysis._process_results()
            else:
                ran_failed.append((analysis, analysis.id))
        gu.print_completed_failed(ran_successfully, ran_failed, message = 'Ran')
        return ran_successfully, ran_failed

    def add_analysis(self, analysis, force = False) -> bool:
        '''
        Adds the specified analysis to the setup.
        Args:
            analysis (tdo.Analysis): The analysis to add.
            force (bool): If True, adds the analysis to the setup even if identical analysis already exists.
            Default is False.
            Each analysis stores its result seperately.
            Filling the same analysis twice will result in larger user's memory resources consumption.
        Returns:
            bool: True if the analysis was added successfully, False otherwise.
        Raises:
            Exception:
                - If the server failed to respond.
                - If the analysis is duplicated and force is False.

        '''
        if analysis.id in [a.id for a in analysis.surface.analyses]:
            analysis._added = True
            return analysis._added

        if not force:
            is_duplicated = False
            duplicated = []

            for existing_analysis in analysis.surface.analyses:
                if analysis == existing_analysis:
                    is_duplicated = True
                    duplicated.append(analysis.id)
            if is_duplicated:
                raise Exception(v.ANALYSES_DUPLICATED_ERROR.format(duplicated = ", ".join(duplicated)))

        data = {
            "surface_id": analysis.surface.id,
            "analyses_data": [
                {
                    "id": analysis.id ,
                    "name": analysis.name,
                    "num_rays": analysis.rays,
                    "resolution": analysis.resolution,
                    "type": 0 if analysis.fast == True else 1,
                }
                ]
            }
        part = analysis.surface._part
        response = au._add_analyses(part._setup.id, part.id, data, self.api_key)
        if response[1] == 'analyses successfully added':
            analysis._added = True
            analysis.surface.analyses.append(analysis)
            return analysis._added
        raise Exception(response[1])
