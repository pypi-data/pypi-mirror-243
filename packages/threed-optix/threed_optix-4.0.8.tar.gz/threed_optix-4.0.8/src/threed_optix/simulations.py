import os
import pickle
import time
import random
import requests
import zipfile
import dill
import copy

from typing import Union
from io import BytesIO

import numpy as np
import pandas as pd

import threed_optix.utils.math as mu
import threed_optix.utils.general as gu
import threed_optix.utils.api as au
import threed_optix.utils.vars as v
import threed_optix.analyses as tdo_analyses
import threed_optix.parts as tdo_parts

class Setup(object):
    """
    Used to manage the simulation setup and its parts.

    Properties:
        name (str): The name of the setup.
        id (str): The id of the setup.
        _api (ThreedOptixAPI): The pointer to the API that created it.
        parts (list): The list of part objects (or classes that inherit from Part).
    """

    def __init__(self):
        '''
        Private
        '''
        raise TypeError("Cannot directly create an instance of Setup.")

    @classmethod
    def _new(cls, _api, setup_tuple: tuple):
        """
        Private.
        Creates a setup with API pointer, id, and name only.

        Args:
            _api (ThreedOptixAPI): The API pointer.
            info_json (dict): Information JSON.

        Returns:
            Setup: The newly created Setup object.
        """
        setup = object.__new__(cls)
        setup.id = setup_tuple[0]
        setup.name = setup_tuple[1]
        setup._api = _api
        setup._opt = None
        setup._parts = None
        return setup

    def __len__(self) -> int:
        """
        Returns the number of parts that the setup has.

        Returns:
            int: The number of parts in the setup.
        """
        return len(self.parts)

    def __iter__(self):
        """
        Iterates through the parts of the setup.
        """
        return iter(self.parts)

    def __contains__(self, part: Union[tdo_parts.Part, str]) -> bool:
        """
        Allows checking if a part is in the setup.

        Args:
            part (tdo.Part): The part to check.

        Returns:
            bool: True if the part is in the setup, False otherwise.

        Raises:
            TypeError: If the part is not a Part object or a part id.
        """

        if not isinstance(part, (tdo_parts.Part, str)):
            raise TypeError(f"Invalid part type {type(part)}. Must be Part or part id.")

        if isinstance(part, tdo_parts.Part):
            for p in self:
                if p.id == part.id:
                    return True

        if isinstance(part, str):
            for p in self:
                if p.id == part:
                    return True

        return False

    def __getitem__(self, key: str):
        """
        Getting parts by index.

        Args:
            key (str): The id of the part.

        Returns:
            Part (tdo.Part): The requested Part object.

        Raises:
            TypeError: If the key is not an int or a str.
            KeyError: If the key is a str and the part is not found.
        """
        # if isinstance(key, int):
        #     return self.parts[key]
        if isinstance(key, str):
            for part in self:
                if part.id == key:
                    return part
            raise KeyError(f"Part with id {key} not found in the setup.")
        raise TypeError(f"Invalid key type {type(key)}. Must be part index or id.")

    def __str__(self):
        '''
        Returns a string representation of the setup and its parts ids and labels.
        '''
        string = f"Setup {self.name} ({self.id}) with {len(self)} parts:\n"
        for part in self:
            string += f"  - {part.label} ({part.id})\n"
        return string

    @property
    def parts(self):
        """
        Property to access the list of part objects of the setup.
        Returns:
            list: The list of Part objects.
        """
        if self._parts is None:
            self._get_parts()
        parts = self._parts
        return parts

    def _get_parts(self):
        '''
        Private
        '''
        parts = self._api._get_setup_parts(self.id).get(self.id).get('parts')
        self._parts = [tdo_parts.Part._new(_setup=self, id=part['id']) for part in parts]
        return None

    def _get_part(self, part_id):
        '''
        Private.
        '''
        part = self._api._get_part(part_id, self.id)
        return part

    def get(self,
            part_label: str,
            all: bool = False):
        """
        Returns the part object with the specified label.

        Args:
            part_label (str): The label of the part.
            all (bool): If True, returns a list of all parts with the specified label.

        Returns:
            Part (tdo.Part): The requested Part object if found, None otherwise.
        """
        if all:
            parts = []
            for part in self:
                if part.label == part_label:
                    parts.append(part)
            return parts

        for part in self:
            if part.label == part_label:
                return part

        return None

    def at(self, location: tuple):
        """
        Private.
        Returns the closest part object to the specified location in the global coordinate system.

        Args:
            location (tuple): The global coordinates (x, y, z) of the location.

        Returns:
            Part: The closest Part object.
        """

        distances = []

        for part in self:
            distance = mu._3d_distance(location, part._pose._position)
            distances.append(distance)

        min_value = min(distances)
        min_index = distances.index(min_value)
        min_part = self[min_index]
        print(f'Closest part is {min_part.label} at the location {min_part._pose}')
        return min_part

    def save(self, file_path: str):
        """
        Saves the object to a re-creatable pickle file with 'dill' package.

        Args:
            file_path (str): The path to save the pickle file.
        """
        with open(file_path, 'wb') as f:
            dill.dump(self, f)
        print(f"Setup saved to {file_path}.")

    @classmethod
    def load(cls, file_path: str, api):
        """
        Loads the object from the pickle\dill file path.

        Args:
            file_path (str): The path to the dill file.
            api (tdo.ThreedOptixAPI): The API instance.

        Returns:
         setup (tdo.Setup): The loaded Setup object.
        """
        with open(file_path, 'rb') as f:
            setup = dill.load(f)
        if api is not None:
            setup._api = api
        print(f"Setup loaded from {file_path}.")
        return setup

    def plot(self):
        """
        Private.
        Plots the setup to visualize its configuration.
        """
        raise NotImplementedError("This method is not implemented yet.")

    def restore(self, to_restore: Union[tdo_parts.Part, 'Setup']):
        '''
        Restores the setup/part to its original state, determined by to_restore.
        So, if a setup or a part are saved with self.copy() before any changes, those changes can be undone by restoring the setup.
        Args:
            to_restore (tdo.Part or tdo.Setup): The part or setup to restore.

        Returns:
            None
        '''

        if isinstance(to_restore, tdo_parts.Part):
            part = to_restore
            r = self.update_part(part)
            if not r[0]:
                raise Exception(r[1])

            current_part = self[part.id]
            current_part._data = part._data
            current_part._pose = part._pose
            return None

        elif isinstance(to_restore, Setup):
            setup = to_restore
            for part in setup:
                self.restore(part)
                return None
        raise ValueError(f"Invalid type {type(to_restore)} to restore: must be Part or Setup.")

    def update_part(self, part):
        '''
        Private
        '''
        return self._api.update_part(self.id, part)

    def copy(self):
        '''
        Returns a copy of the setup.
        '''
        return copy.deepcopy(self)

class Job:
    """
    Private.
    Contains information about a batch job.

    Attributes:
        _api (ThreedOptixAPI): The API pointer.
        _setup (Setup): The setup pointer.
        __base_url (str): The base URL for results.
        _prefix (str): The prefix of the results.
        __num_changes (int): Number of requested changes.
    """

    ##Magic methods and constructors
    def __init__(self):
        raise TypeError("Cannot directly create an instance of Job.")

    @classmethod
    def _from_json(cls, json_: dict, _api, _setup):
        """
        Creates the Job instance from the response JSON.

        Args:
            json (dict): The JSON response.

        Returns:
            Job: The created Job instance.
        """
        job = object.__new__(cls)
        job._url = json_['url'].replace('$', '')
        job._setup = _setup
        job._api = _api
        job._prefix = json_['simulation_file_prefix']
        job._num_changes = json_['number_of_changes']
        job.results = [tdo_analyses.RayTable._new(job._url.format(index = index), _setup) for index in range(job._num_changes)]
        return job

    def __str__(self):
        string = f'Job with {self._num_changes} changes and prefix {self._prefix} at {self._url}.\nBased on setup {self._setup.name} ({self._setup.id})'
        return string

    def __getitem__(self, index):
        """
        Gets the URL of the analysis at the specified location.

        Args:
            index: The index of the analysis.

        Returns:
            str: The URL of the analysis.
        """
        return self.results[index]

    def __len__(self) -> int:
        """
        Returns the number of changes.

        Returns:
            int: The number of changes.
        """
        return self._num_changes

    def __iter__(self):
        """
        Allows iterations over the URLs.

        Yields:
            str: The next URL.
        """
        return iter(self.results)

    ##Main 'Public' Methods
    def pull(self, index, filepath, **kwargs):
        """
        Gets the results of the analysis at the specified index.

        Args:
            index: The index of the analysis.

        Returns:
            dict: The results of the analysis.
        """
        result = self[index]
        result.to_csv(filepath, **kwargs)

    def status(self):
        """
        Returns a status report of the job.

        Returns:
            str: The status report.
        """
        raise NotImplementedError("This method is not implemented yet.")
