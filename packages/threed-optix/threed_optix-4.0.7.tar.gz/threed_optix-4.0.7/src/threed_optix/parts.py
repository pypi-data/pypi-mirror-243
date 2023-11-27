import threed_optix.analyses as an
import threed_optix.utils.math as mu
import copy
import json

class Part:

    _data = None
    _surfaces = None
    ##Magic methods and constructors
    def __init__(self):
        raise TypeError("Cannot directly create an instance of Part.")

    @classmethod
    def _new(cls, _setup, id):
        """
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
        return part

    def __str__(self) -> str:
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

    def __getitem__(self, key):
        """
        Allows getting surfaces by index.

        Args:
            key: The index of the surface.

        Returns:
            Surface: The requested Surface object.
        """
        if isinstance(key, int):
            return self.surfaces[key]
        if isinstance(key, str):
            for surface in self:
                if surface.id == key:
                    return surface
            raise KeyError(f"Surface with id {key} not found in the part.")
        raise TypeError(f"Invalid key type {type(key)}. Must be surface index or id.")

    ##Properties
    @property
    def data(self):
        if self._data is None:
            self._data = self._setup._get_part(self.id).get(self.id)
        data = self._data
        return data

    @property
    def pose(self):
        return self._pose

    @property
    def label(self):
        return self.data['label']

    @property
    def material(self):
        return self.data['material']

    @property
    def surfaces(self):
        if self._surfaces is None:
            self._surfaces = [Surface._new(self, surface) for surface in self.data.get('surfaces', []) if 'name' in surface]
        return self._surfaces

    ##'Public' Utils
    def get(self, name):
        """
        Returns the surface object with the specified name.

        Args:
            name (str): The name of the surface.

        Returns:
            Surface: The requested Surface object.
        """
        for surface in self:
            if surface.name == name:
                return surface
        return None

    ##Main 'Public' Methods
    def change_pose(self, vector, radians = False):

        assert len(vector) == 6, "Pose vector must be of length 6."

        if radians:
            vector[3:] = [mu.rad_to_deg(x) for x in vector[3:]]

        if self._data is None:
            self._data = self._setup._get_part(self.id).get(self.id)

        self.backup_pose = copy.deepcopy(self._data['pose'])

        self._data['pose']['rotation'] = vector[3:]
        self._data['pose']['position'] = vector[:3]

        self.sync()

    def sync(self):
        r = self._setup.update_part(self)
        if not r[0]:
            self._data['pose'] = self.backup_pose
            raise Exception(f"Error updating part: {r[1]}")

        for part in self._setup:
            if part._data is not None and part != self:
                part._data = None

    def copy(self):
        return copy.deepcopy(self)

class Detector(Part):

    _size = None

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
        raise TypeError("Cannot directly create an instance of Surface.")

    @classmethod
    def _new(cls, _part, _data):
        surface = object.__new__(cls)
        surface.name = _data['name']
        surface.id = _data['id']
        surface._part = _part
        surface.analyses = [an.Analysis._new(surface = surface, **analysis) for analysis in _data['analyses']]
        return surface

    def __str__(self):
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

    vector = None
    ##Magic methods and constructors

    def __init__(self):
        raise TypeError("Cannot directly create an instance of _Pose.")

    @classmethod
    def _new(cls, _part):
        pose = object.__new__(cls)
        pose._part = _part
        return pose

    @property
    def vector(self):
        return self._part._data['pose']['position'] + self._part._data['pose']['rotation']

    def __str__(self):
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
        return self.vector[key]
