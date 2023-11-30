import zipfile
import requests
import random
import time
import json
import copy
import zipfile
import os

import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt

from io import BytesIO
from matplotlib.colors import LinearSegmentedColormap
from plotly.graph_objs.layout import Colorscale

import threed_optix.utils.api as au
import threed_optix.utils.general as gu
import threed_optix.utils.vars as v

class RayTable:
    """
    Contains information about simulation results.
    Properties:
        _url (str): The URL of the results file.
        _data (pd.DataFrame): The ray table data of the simulation results.
    """

    def __init__(self):
        '''
        Private.
        '''
        raise TypeError("Cannot directly create an instance of Result.")

    @classmethod
    def _new(cls, ray_table_url, maps_url, setup_object):
        """
        Private.
        Creates a new results object based on the results of ```api.run(setup)```.

        Args:
            url (str): The URL of the results file.

        Returns:
            Result: The created Result object.
        """
        ray_table = object.__new__(cls)
        ray_table._ray_table_url = ray_table_url
        ray_table._data = None
        ray_table._maps_url = maps_url
        ray_table.setup = setup_object
        return ray_table

    def __str__(self):
        '''
        Returns the setup name, setup id and the url of the results file.
        '''
        string = json.dumps(
            {
                "setup": self.setup.name,
                "setup id": self.setup.id,
                "data url": self._ray_table_url,
            },
            indent = 4,
        )
        return string

    @property
    def data(self):
        """
        The ray table data of the simulation results.
        Data is not fetched until this property is accessed.
        Returns:
            pd.DataFrame: The data of the simulation results.
        """
        return self._get_data()

    def _get_data(self):
        """
        Private.
        Shouldn't be accessed by the user.
        If data is not None, returns data.
        If data is None, fetches data and returns data.

        Returns:
            pd.DataFrame: The data of the simulation results.
        """
        if self._data is None:
            self._data = au._map_ray_table(self._ray_table_url, self._maps_url)
        return self._data

    def to_csv(self, path: str, **kwargs) -> None:
        """
        Saves the ray table data to a CSV file.

        Args:
            path (str): The path to save the CSV file.
        Returns:
            None
        """
        self.data.to_csv(path, **kwargs)
        return None

class Analysis:

    def __init__(self,
                 surface,
                 resolution,
                 rays,
                 name,
                 fast=False):
        """
        Initializes a new instance of the Analysis class.

        Args:
            surface (Surface): The surface of the analysis.
            resolution (tuple): The resolution of the analysis surface in the form (x, y).
            rays (dict): A dictionary of lasers and the number of rays for each laser.
            name (str): The name of the analysis.
            fast (bool, optional): Specifies if the analysis is fast or advanced. Defaults to False.

        Returns:
            tdo.Analysis: The created Analysis object.

        Raises:
            AssertionError: If the name or rays are not valid for 'fast' choice.
        """

        self._added = False
        self._urls = []
        self._fail_message = None
        self._raw_results = {}
        self.results = {}
        self.surface = surface
        self.name = name
        self.rays = {laser.id: num_rays for laser, num_rays in rays.items()}
        self.resolution = {'x': resolution[0], 'y': resolution[1]}
        self.id = Analysis._generate_id()
        self.fast = fast
        num_rays = self.rays.values()
        Analysis._assert_analysis_params(fast=fast, name=name, num_rays=num_rays)

    @classmethod
    def _assert_analysis_params(cls, fast, name, num_rays):
        '''
        Private.
        '''
        #Get the valid names for fast analysis
        fast_valid_names = v.FAST_ANALYSIS_NAMES

        #Get the valid names for advanced analysis
        advanced_valid_names = v.ANALYSIS_NAMES

        if fast:
            #Check if the name of the analysis is valid for fast analysis
            assert name in fast_valid_names, f"Valid names for fast analysis are {fast_valid_names}"
            assert all([num <= 200 for num in num_rays]), f'Number of rays must be less than 200 for fast analysis'
        else:
            #Check if the name of the analysis is valid for advanced analysis
            assert name in advanced_valid_names, f"Valid names for advanced analysis are {advanced_valid_names}"

    @classmethod
    def _new(cls, surface, resolution, num_rays, name, type, id):
        '''
        Private.
        Past analysis are stored within the setup.
        When the setup is fetched, the past analysis are created using this method.
        '''
        analysis = object.__new__(cls)
        analysis.surface = surface
        analysis.resolution = resolution
        analysis.rays = num_rays
        analysis.name = name
        analysis.fast = False if type == '1' else True
        analysis.id = id
        analysis._added = True
        analysis._urls = []
        analysis._fail_message = None
        analysis._raw_results = {}
        analysis.results = {}

        return analysis

    @property
    def wls(self):
        '''
        Returns a sorted list of the analysis wavelengths.
        '''
        return self._analysis_wls()

    @classmethod
    def _generate_id(cls):
        '''
        Private
        Generates a unique id for the analysis.
        '''
        int_time = int(time.time())
        enc_36_time = np.base_repr(int_time, 36)
        randint = np.base_repr(random.randint(0, 36**5), 36)[2:5]
        id_ = enc_36_time + randint
        return id_

    def _analysis_wls(self):
        '''
        Private.
        Returns a sorted list of the wavelengths of the analysis
        '''
        analysis_wls = []
        setup = self.surface._part._setup
        lasers_ids = self.rays.keys()
        laser_objects = [setup[laser] for laser in lasers_ids]
        for laser in laser_objects:
            wls_dicts = laser.data['light_source']['wavelengths_data']
            wls = [wls_dict['wavelength'] for wls_dict in wls_dicts]
            analysis_wls += wls
        analysis_wls = sorted(list(set(analysis_wls)))
        return analysis_wls

    def _extract_file(self,url, destination):
        ''''
        Private.
        Extracts a zip file from a url to a destination folder
        '''
        response = requests.get(url)
        if response.status_code == 200:
            zip_data = BytesIO(response.content)
            with zipfile.ZipFile(zip_data, 'r') as zip_ref:
                zip_ref.extractall(destination)

        file_name = url.split('/')[-1].replace(f'{self.id}_', '').replace('.zip', '')
        file_path = f'{destination}/{file_name}'
        return file_path

    def _unpack(self):
        '''
        Private.
        Unpacks the results of the analysis to a folder
        '''
        setup = self.surface._part._setup.id
        destination_path = f'.analysis-files/{setup}/{self.surface.id}/{self.id}'
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)
        for url in self._urls:
            self._extract_file(url, destination_path)

        return destination_path

    def _read_file(self, file_path):
        '''
        Private.
        Reads the results of the analysis from a file
        '''
        with open(file_path, 'rb') as f:
            content = f.read()
        header_format = v.ANALYSIS_HEADER_DTYPES
        header = np.frombuffer(content[:v.HEADER_BYTES], dtype=header_format)
        data = np.frombuffer(content[v.HEADER_BYTES:], dtype=v.ANALYSIS_MATRIX_DTYPES)
        return header, data

    def _process_results(self):
        '''
        Private.
        Processes the results of the analysis
        '''
        directory = self._unpack()
        for file in os.listdir(directory):
            file_results = {}
            file_path = f'{directory}/{file}'
            headers_nums, data = self._read_file(file_path)
            headers = gu.process_headers(headers_nums)
            file_results['metadata'] = headers
            data_matrices = data.reshape(len(self.wls), self.resolution['x'], self.resolution['y'])
            file_results['data'] = {}
            for i, wl in enumerate(self.wls):
                matrix = data_matrices[i]
                file_results['data'][wl] = matrix
            file_name = file.split('.')[0]
            self._raw_results[file_name] = file_results
        polarized_dict = gu.reorganize_analysis_results_dict(self._raw_results.values())
        self.results = polarized_dict
        return self.results

    def __str__(self):
        '''
        Returns a string representation of the analysis.
        '''
        string = json.dumps(
            {
                "name": self.name,
                "id": self.id,
                "resolution": self.resolution,
                "rays": self.rays,
                "surface": self.surface.id,
                "part": self.surface._part.id,
            },
            indent=4,
        )

        return string

    def __eq__(self, other):
        '''
        Equal analyses are analyses with the same parameters of rays, name, resolution and surface.
        '''
        if not isinstance(other, Analysis):
            return False

        is_rays_equal = self.rays == other.rays
        is_name_equal = self.name == other.name
        is_resolution_x_equal = self.resolution['x'] == other.resolution['x']
        is_resolution_y_equal = self.resolution['y'] == other.resolution['y']
        is_surface_equal = self.surface.id == other.surface.id

        if is_rays_equal and is_name_equal and is_surface_equal and is_resolution_x_equal and is_resolution_y_equal:
            return True

        return False

    def show(self, figsize = (20, 20), upscale = False):
        '''
        Shows a static figure of the analysis results.
        Args:
            figsize (tuple): The size of the figure.
            upscale (bool): If True, smoothes the pixels over, if the analysis resolution is lower than the figure resolution.

        Returns:
            None

        Shows:
            A figure of the analysis results.

        Raises:
            Exception: If the analysis was not run yet.
        '''

        #3DOptix color scale
        cmap = LinearSegmentedColormap.from_list('custom', v.COLOR_SCALE)

        #Check if the analysis was run
        if not self.results:
            raise Exception('Analysis was not run yet')

        #Get the number of polarizations and wavelengths of the analysis- polarizations are the rows and wavelengths are the columns of the presented figure
        num_polarizations = len(self.results)
        num_wavelengths = list(self.results.values())[0]['metadata']['num_wavelengths']
        fig = plt.figure(constrained_layout=True, figsize=figsize)
        subfigs = fig.subfigures(nrows=num_polarizations, ncols=1)

        if num_polarizations == 1:
            subfigs = [subfigs]

        for polarization, subfig in zip(self.results.keys(), subfigs):

            subfig.suptitle(f'Polarization {polarization}')
            axs = subfig.subplots(nrows=1, ncols=num_wavelengths)

            if num_wavelengths == 1:
                axs = [axs]

            for wavelength, ax in zip(self.results[polarization]['data'].keys(), axs):
                data = self.results[polarization]['data'][wavelength]
                if upscale:
                    dpi = plt.rcParams['figure.dpi']
                    data = gu.upscale(data, figsize[0]*dpi, figsize[1]*dpi)
                ax.imshow(data, cmap=cmap)

                ax.set_title(f'Wavelength {wavelength} nm')

        #Show the figure
        plt.show()
        return None

    def show_interactive(self, polarizations=None, wavelengths=None, height = 600, width = 600, upscale = False):
        '''
        Shows an interactive figure of the analysis results.
        Args:
            polarizations (list): The polarizations to present. If None, all polarizations are presented.
            wavelengths (list): The wavelengths to present. If None, all wavelengths are presented.
            height (int): The height of the each figure.
            width (int): The width of each figure.
            upscale (bool): If True, smoothes the pixels over, if the analysis resolution is lower than the figure resolution.
        Returns:
            None

        Shows:
            An interactive figure of the analysis results.

        Raises:
            Exception: If the analysis was not run yet.
        '''
        if not self.results:
            raise Exception('Analysis was not run yet')

        if not polarizations:
            polarizations = list(self.results.keys())
        if not wavelengths:
            wavelengths = list(self.results[polarizations[0]]['data'].keys())

        for polarization in polarizations:
            for wavelength in wavelengths:
                data = self.results[polarization]['data'][wavelength]
                if upscale:
                    data = gu.upscale(data, height, width)

                fig = px.imshow(data, title=f'Polarization {polarization} Wavelength {wavelength} nm', color_continuous_scale = v.COLOR_SCALE)
                fig.update_layout(height=height, width=width)
                fig.show()

    def copy(self):
        '''
        Copies the analysis to a different analysis object with a different id.
        Returns:
        tdo.Analysis: The copied analysis.
        '''
        copied = copy.deepcopy(self)
        copied.id = Analysis._generate_id()
        copied._added = False
        return copied
