import threading
import pickle
import math
from typing import Any
import requests
import pandas as pd
import numpy as np
import random
import time
import requests
import zipfile
from io import BytesIO
import os

import threed_optix.utils.api as au
import threed_optix.utils.vars as v
import threed_optix.utils.math as mu
import threed_optix.utils.general as gu
import threed_optix.analyses as an
import threed_optix.simulations as sim

class ThreedOptixAPI:
    """
    Used to manage the communication with the server of 3DOptix.

    Args:
        api_key (str): The API key used for authentication.

    Attributes:
        api_key (str): The API key of the user.
        jobs (list): A list of Job objects for batch jobs.
        setups (list): The list of setups of the user.
    """
    setups = None
    ##Magic methods
    def __init__(self, 
                 api_key: str,
                 verbose = True
                 ):
        self.api_key = api_key
        self.jobs = []

        assert self.is_up(), v.SERVER_DOWN_MESSAGE
        assert self.is_key_valid(), v.INVALID_KEY_MESSAGE

        if verbose:
            welcome_thread = threading.Thread(target=au._welcome)
            welcome_thread.start()

        setups_thread = threading.Thread(target=self._initialize_setups)
        setups_thread.start()

        # Wait for both threads to finish
        if verbose:
            welcome_thread.join()

        setups_thread.join()
        if self.setups is None:
            raise Exception("Could not initialize setups, check your API key")

    def __contains__(self,
                     item
                     ):
        """
        Allows checking if a setup name or id is in the API.

        Args:
            item: The setup name, id, or object.

        Returns:
            bool: True if the setup exists, False otherwise.
        """
        contains = False
        if isinstance(item, str):
            for setup in self:
                if setup.id == item:
                    contains = True
                    break
        elif isinstance(item, sim.Setup):
            for setup in self:
                if setup.id == item.id:
                    contains = True
                    break
        return contains

    def __len__(self) -> int:
        """
        Returns the number of setups.

        Returns:
            int: The number of setups.
        """
        return len(self.setups)

    def __iter__(self):
        """
        Allows iterating through the setups.

        Yields:
            Setup: The next Setup object.
        """
        return iter(self.setups)

    def __str__(self) -> str:
        string = f"API with {len(self)} setups:\n"
        for setup in self:
            string += f"  - {setup.name} ({setup.id})\n"
        return string

    def __getitem__(self, key):
        """
        Allows accessing API setups by index, id, or name.

        Args:
            key: The index or id of the setup.

        Returns:
            Setup: The corresponding Setup object.
        """
        if isinstance(key, int):
            return self.setups[key]
        elif isinstance(key, str):
            for setup in self:
                if setup.id == key:
                    return setup
            raise KeyError(f"Setup with id {key} not found.")
        raise TypeError(f"Invalid key type {type(key)}. Must be setup index or id.")

    ##'Private' Utils
    def _initialize_setups(self):
        self.setups = self._get_setups_info()
        if self.setups is not None:
            self.setups = [sim.Setup._new(_api=self, setup_tuple=setup) for setup in self.setups]
        return self.setups

    def _get_setups_info(self) -> list:
        """
        Returns a list of Setup objects that are associated with the user.

        Returns:
            list: A list of Setup objects.
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
        parts = au._get_setup(setup_id, self.api_key)[0]
        return parts

    def _get_part(self, part_id: str, setup_id) -> dict:
        part = au._get_part(setup_id,part_id,  self.api_key)[0]
        return part

    def _extract_setup_object(self, setup):

        if isinstance(setup, str):

            if setup in self:
                setup_object = self[setup]
                return setup_object

            elif self.get(setup) is not None:
                setup_object = self.get(setup)
                return setup_object

            else:
                raise Exception(f"Setup with id or name {setup} not found.")

        if isinstance(setup, sim.Setup):
            return setup

        if isinstance(setup, int):
            return self.setups[setup]

        raise TypeError(f"Invalid setup type {type(setup)}. Must be Setup object, name, index or id.")

    ##'Public' Utils
    def get(self,
            setup_name: str,
            all: bool = False
            ):
        """
        Returns the Setup object with the specified name.


        Args:
            setup_name (str): The name of the setup.
            all (bool): If True, returns all setups with the specified name. else, returns the first one

        Returns:
            Setup: The Setup object.
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

    def is_key_valid(self) -> bool:
        return True

    def update_part(self, setup_id, part):
        success, message = au._set_part(setup_id, part.id, part.data, self.api_key)
        if not success:
            raise Exception(message)
        return (success, message)

    ##Main 'Public' Methods
    def get_setups(self):
        """
        Returns a list of Setup objects that are associated with the user.

        Returns:
            list: A list of Setup objects.
        """
        return self.setups

    def run(self,
            setup
            ):
        """
        Sends the opt file to the 3DOptix server and returns a Results object.

        Args:
            setup (Setup): The setup to run.

        Returns:
            Results: The Results object.
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
            return an.RayTable._new(ray_table, maps_url, setup_object)
        else:
            raise Exception(message)

    def run_async(self, setup):
        setup_object = self._extract_setup_object(setup)
        data, message = au._run_simulation(setup_object.id, self.api_key, is_sync = False)
        if data == None:
            raise Exception(message)
        if data['results'][0]['error']['code'] != 0:
            raise Exception(v.SIMULATION_ERROR.format(message = data['results'][0]['error']['message']))

        if data is not None:
            ray_table = data['results'][0]['data']['ray_table']
            maps_url = data['maps_url']
            return an.RayTable._new(ray_table, maps_url, setup_object)
        else:
            raise Exception(message)

    def run_batch(self,
                  setup,
                  configuration: dict
                  ):
        """
        Sends the setup id with the configuration to 3DOptix server and returns a Job object.
        Job object will be appended to self.jobs list.

        Args:
            setup (Setup): The setup to run.
            configuration (dict): The configuration for the batch job.

        Returns:
            Job: The Job object.
        """
        response = au._run_batch(setup.id, configuration, self.api_key)
        if response[0] is not None:
            json_ = response[0]
            json_['number_of_changes'] = configuration['number_of_changes']
            json_['simulation_file_prefix'] = configuration['simulation_file_prefix']
            job = sim.Job._from_json(response[0], _api = self, _setup = setup)
            job._url = job._url.replace('$', '')
            self.jobs.append(job)
            return job
        else:
            raise Exception(response[1])

    def run_analysis(self, analysis, auto_add = False, force = False):
        successful, failed =  self.run_analyses([analysis], auto_add = auto_add, force = force)
        if len(successful) == 1:
            return True
        return False

    def run_analyses(self, analyses, auto_add = False, force = False):

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
                analysis.results = analysis.process_results()
            else:
                ran_failed.append((analysis, analysis.id))
        gu.print_completed_failed(ran_successfully, ran_failed, message = 'Ran')
        return ran_successfully, ran_failed

    def add_analysis(self, analysis, force = False):

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