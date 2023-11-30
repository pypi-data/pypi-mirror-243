import threed_optix.analyses as an
import threed_optix.utils.math as mu
import copy
import json

class Part:

    def __init__(self):
        '''
        Private
        '''
        raise TypeError("Cannot directly create an instance of Part.")

    @classmethod
    def _new(cls, _setup, id):
        """
        Private
        Creates a new part from the opt_part at the specified index within the setup.

        Args:
            _setup (Setup): The setup object.
            _index (int): The index of the part within the setup.

        Returns:
            Part: The newly created Part object.
        """

        part = object.__new__(cls)
        part._setup = _setup
        part.id = id
        part._pose = _Pose._new(part)
        part._data = None
        part._surfaces = None

        return part

    def __str__(self) -> str:
        '''
        Returns a string representation of the part: label, id, position, and rotation.
        '''
        string = json.dumps(
            {
                "label": self.label,
                "id": self.id,
                "position": self.pose.vector[:3],
                "rotation": self.pose.vector[3:],
            },
            indent = 4
            )
        return string

    def __iter__(self):
        """
        Allows iterating through the surfaces of the part.

        Yields:
            Surface: The next Surface object.
        """
        return iter(self.surfaces)

    def __getitem__(self, key: str):
        """
        Allows getting surfaces by surface id.

        Args:
            key: The id of the surface.

        Returns:
            surface (tdo.Surface): The requested Surface object.

        Raises:
            KeyError: If the surface with the specified id is not found in the part.
            TypeError: If the key is not str.
        """
        # if isinstance(key, int):
        #     return self.surfaces[key]
        if isinstance(key, str):
            for surface in self:
                if surface.id == key:
                    return surface
            raise KeyError(f"Surface with id {key} not found in the part.")
        raise TypeError(f"Invalid key type {type(key)}. Must be surface id.")

    @property
    def data(self):
        '''
        Data is a dictionary containing the part's detailed data.
        '''
        if self._data is None:
            self._data = self._setup._get_part(self.id).get(self.id)
        data = self._data
        return data

    @property
    def pose(self):
        '''
        Part's pose is a dictionary containing the part's pose object.
        '''
        return self._pose

    @property
    def label(self):
        '''
        returns the part's label.
        '''
        return self.data['label']

    @property
    def material(self):
        '''
        Returns the part's material.
        '''
        return self.data['material']

    @property
    def surfaces(self):
        '''
        Returns a list of the part's surfaces as tdo.Surface objects.
        '''
        if self._surfaces is None:
            self._surfaces = [Surface._new(self, surface) for surface in self.data.get('surfaces', []) if 'name' in surface]
        return self._surfaces

    def get(self, name):
        """
        Returns the surface object with the specified name.

        Args:
            name (str): The name of the surface.

        Returns:
            surface (tdo.Surface): The requested Surface object. If the surface is not found, returns None.
        """
        for surface in self:
            if surface.name == name:
                return surface
        return None

    def change_pose(self, vector, radians = False):
        '''
        Most important method of the Part class. Changes the part's pose.
        Args:
            vector (list): A list of length 6 containing the part's new pose vector. Pose vector can be accessed through part.pose.vector.
            radians (bool): If True, the rotation values are assumed to be in radians. If False, the rotation values are assumed to be in degrees. Default to False.

        Returns:
            None

        Raises:
            AssertionError: If the length of the vector is not 6.
        '''

        assert len(vector) == 6, "Pose vector must be of length 6."

        if radians:
            vector[3:] = [mu.rad_to_deg(x) for x in vector[3:]]

        if self._data is None:
            self._data = self._setup._get_part(self.id).get(self.id)

        self.backup_pose = copy.deepcopy(self._data['pose'])

        self._data['pose']['rotation'] = vector[3:]
        self._data['pose']['position'] = vector[:3]

        self.sync()

        return None

    def sync(self):
        '''
        Private.
        '''
        r = self._setup.update_part(self)
        if not r[0]:
            self._data['pose'] = self.backup_pose
            raise Exception(f"Error updating part: {r[1]}")

        for part in self._setup:
            if part._data is not None and part != self:
                part._data = None

    def copy(self):
        '''
        Returns a copy of the part, used for backup purposes when changing part's properties.
        '''
        return copy.deepcopy(self)

class Detector(Part):
    '''
    Private
    '''

    def __init__(self):
        raise TypeError("Cannot directly create an instance of Detector.")

    @property
    def size(self):
        if self._size is None:
            self._size = self._data['size']
        return self._size

    def change_size(self, size):
        if self._data is None:
            self._data = self._setup._get_part(self.id).get(self.id)
        self._data['size'] = size
        self.sync()

class LightSource(Part):
    '''
    Private
    '''
    _light_source = None

    def __init__(self):
        raise TypeError("Cannot directly create an instance of LightSource.")

    @property
    def _light_source(self):
        if self._light_source is None:
            self._light_source = self.data['light_source']
        return self._light_source

class Surface:
    def __init__(self):
        '''
        Private
        '''
        raise TypeError("Cannot directly create an instance of Surface.")

    @classmethod
    def _new(cls, _part, _data):
        '''
        Private
        '''
        surface = object.__new__(cls)
        surface.name = _data['name']
        surface.id = _data['id']
        surface._part = _part
        surface.analyses = [an.Analysis._new(surface = surface, **analysis) for analysis in _data['analyses']]
        return surface

    def __str__(self):
        '''
        Returns a string representation of the surface: name, id, part id, and part label.
        '''
        string = json.dumps(
            {
            "name": self.name,
            "id": self.id,
            "part id": self._part.id,
            "part label": self._part.label
            },
            indent = 4
            )
        return string

class _Pose:
    def __init__(self):
        '''
        Private
        '''
        raise TypeError("Cannot directly create an instance of _Pose.")

    @classmethod
    def _new(cls, _part):
        '''
        Private
        '''
        pose = object.__new__(cls)
        pose._part = _part
        return pose



    @property
    def vector(self):
        '''
        Returns the part's pose vector, which is a list of length 6 containing the part's position and rotation.
        '''
        return self._part._data['pose']['position'] + self._part._data['pose']['rotation']

    def __str__(self):
        '''
        Returns a string representation of the pose: position, rotation, part id, and part label.
        '''
        string = json.dumps(
            {
                "position": self.vector[:3],
                "rotation": self.vector[3:],
                "part id": self._part.id,
                "part label": self._part.label
            },
            indent = 4
        )
        return string

    def __getitem__(self, key):
        '''
        Returns the value of the pose vector at the specified index.
        '''
        return self.vector[key]
