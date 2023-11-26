import datetime
import json
import os
import pathlib

import requests
import unidecode


def _call(point):
    class API_Call:
        def __init__(self, path):
            # Initialize API_Call with a specified path
            self.path = pathlib.Path(
                str(pathlib.Path(__file__).parent.parent.absolute()).replace('\\', '/') + '/.cache/' + path + ".json")
            self.url = f"https://tyradex.tech/api/v1/{path}"

            # Create necessary directories for cache if they don't exist
            parent = self.path.parent
            pile = []
            while not parent.exists():
                pile.insert(0, parent)
                parent = parent.parent
            for doss in pile:
                os.mkdir(doss)

        @property
        def json(self):
            try:
                # Try to load data from cache file
                cache = json.load(open(self.path))
                if datetime.datetime.now() < datetime.datetime.fromtimestamp(cache['expired']):
                    return cache['data']
                else:
                    raise FileNotFoundError
            except FileNotFoundError:
                # If cache is not available or expired, make a new API request
                response = requests.get(
                    self.url,
                    headers={
                        "User-Agent": "Tyradex Python API v0.1.0",
                        'Content-type': 'application/json'
                    }
                )

                if response.status_code == 200:
                    # If the request is successful, cache the data and return it
                    data = response.json()
                    if "status" in data:
                        raise RuntimeError("La requête a échoué avec le code d'état:", data['status'], ':',
                                           data['message'])
                    json.dump(
                        {
                            'expired': (datetime.datetime.now() + datetime.timedelta(weeks=4)).timestamp(),
                            'data': data
                        }, open(self.path, 'w'))
                    return data
                else:
                    # If the request is not successful, raise an error
                    raise RuntimeError("La requête a échoué avec le code d'état:", response.status_code)

    return API_Call(point).json


class Pokemon:
    def __init__(self, identifier: int | str | dict, region: str = ...):
        """ Get information about a specific Pokémon.

        :param identifier: Pokémon's identifier in the National Pokédex or its name.
        :param region: Pokémon's region for regional form information.
        """
        if isinstance(identifier, dict):
            self.__data = identifier
        else:
            self.__data = _call(f'pokemon/{identifier}' + ('' if region is ... else f'/{region}'))

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return self.pokedex_id

    @property
    def pokedex_id(self) -> int:
        return self.__data['pokedexId']

    @property
    def generation(self) -> int:
        return self.__data['generation']

    @property
    def category(self) -> str:
        return self.__data['category']

    @property
    def name(self):
        return Name(self.__data['name'])

    @property
    def sprites(self):
        return Sprites(self.__data['sprites'])

    @property
    def types(self):
        t = self.__data['types']
        if t is None:
            return VoidType()
        elif len(t) == 1:
            return Type(t[0]['name'])
        else:
            return Type(t[0]['name']).put_with(Type(t[1]['name']))

    @property
    def talents(self) -> list:
        return [Talent(data) for data in self.__data['talents']] if self.__data['talents'] is not None else []

    @property
    def stats(self):
        return Stats(self.__data['stats'])

    @property
    def resistances(self) -> list:
        return [Resistance(data) for data in self.__data['resistances']] if self.__data[
                                                                                'resistances'] is not None else []

    @property
    def evolution(self):
        return Evolutions(self.__data['evolution'])

    @property
    def height(self) -> float:
        return float(self.__data['height'].replace(',', '.').removesuffix('m')) if self.__data[
                                                                                       'height'] is not None else 0

    @property
    def weight(self) -> float:
        return float(self.__data['weight'].replace(',', '.').removesuffix('kg')) if self.__data[
                                                                                        'weight'] is not None else 0

    @property
    def egg_groups(self) -> list[str]:
        return self.__data['egg_groups'] if self.__data['egg_groups'] is not None else []

    @property
    def sexe(self):
        return Sexe(self.__data['sexe'])

    @property
    def catch_rate(self) -> int:
        return self.__data['catch_rate']

    @property
    def level_100(self) -> int:
        return self.__data['level_100']

    @property
    def forme(self) -> list:
        return [Forme(data, self.pokedex_id) for data in self.__data['forme']] if self.__data[
                                                                                      'forme'] is not None else []


class Type:
    class Fusion:
        def __init__(self, type_1: int | str, type_2):
            """ Get information about a specific type combination.

            :param type_1: Identifier, English, or French name of the first type.
            :param type_2: Second desired type for combination, used to get Pokémon with this dual type.
            """
            self.__data = _call(f'types/{type_1}/{type_2}')

        def __str__(self):
            return str(self.name)

        def __repr__(self):
            return str(self.name)

        @property
        def id(self) -> list[int]:
            return self.__data['id']

        @property
        def name(self):
            return Name(self.__data['name'])

        @property
        def sprites(self) -> list[str]:
            return self.__data['sprites']

        @property
        def resistances(self):
            return [Resistance(data) for data in self.__data['resistances']]

        @property
        def pokemons(self):
            class Pokemons:
                def __init__(self, ids):
                    self.ids = ids

                def get(self):
                    return [Pokemon(pokedex_id) for pokedex_id in self.ids]

            return Pokemons([pok['pokedexId'] for pok in self.__data['pokemons']])

    def __init__(self, identifier: int | str | dict):
        """ Get information about a specific Pokémon type.

        :param identifier: Identifier, English, or French name of the type.
        """
        if isinstance(identifier, dict):
            self.__data = identifier
        else:
            self.__data = _call(f'types/{unidecode.unidecode(identifier)}')

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return repr(self.name)

    @property
    def id(self) -> int:
        try:
            return self.__data['id']
        except KeyError as err:
            print(self.__data.keys())
            raise err

    @property
    def name(self):
        return Name(self.__data['name'])

    @property
    def sprites(self) -> str:
        return self.__data['sprites']

    @property
    def resistances(self):
        return [Resistance(data) for data in self.__data['resistances']]

    @property
    def pokemons(self):
        class Pokemons:
            def __init__(self, ids):
                self.ids = ids

            def get(self):
                return [Pokemon(pokedex_id) for pokedex_id in self.ids]

        return Pokemons([pok['pokedexId'] for pok in self.__data['pokemons']])

    def put_with(self, other):
        return self.Fusion(self.id, other.id)


class Generations:
    class Gen:
        def __init__(self, generation):
            """ Obtain information about a specific generation.

            :param generation: Represents the generation number.
            """
            self.generation = generation
            # Fetch data for Pokémon in the specified generation and sort based on Pokédex ID
            self._data = [Pokemon(pok['pokedexId']) for pok in _call(f'gen/{generation}')]
            self._data.sort(key=lambda p: p.pokedex_id)

        def __str__(self):
            return f"Generation {self.generation}"

        def __repr__(self):
            return f"Gen{self.generation}"

        def __getitem__(self, pokedex_id):
            # Get a Pokémon from the generation by its Pokédex ID
            return self._data[pokedex_id - 1]

        def __iter__(self):
            # Initialize iteration over the Pokémon in the generation
            self.index = 1
            return self

        def __next__(self):
            try:
                # Get the next Pokémon in the generation
                obj = self[self.index]
            except IndexError:
                # Stop iteration if all Pokémon have been visited
                raise StopIteration
            self.index += 1
            return obj

    def __init__(self):
        """ Obtain the list of different generations."""
        # Fetch data for all generations and sort based on generation number
        self._data = [self.Gen(gen['generation']) for gen in _call(f'gen')]
        self._data.sort(key=lambda x: x.generation)

    def __str__(self):
        return str(self._data)

    def __repr__(self):
        return repr(self._data)

    def __getitem__(self, gen):
        # Get a specific generation by its index
        return self._data[gen - 1]

    def __iter__(self):
        # Initialize iteration over the generations
        self.index = 1
        return self

    def __next__(self):
        try:
            # Get the next generation
            obj = self[self.index]
        except IndexError:
            # Stop iteration if all generations have been visited
            raise StopIteration
        self.index += 1
        return obj


# =-=-=-=-=-=-=-=-=-=-=-=-=


class VoidType:
    def __init__(self):
        """Constructor called when a Pokémon has no type."""
        # Placeholder for Fusion attribute (not utilized in this class)
        self.Fusion = object

    def __str__(self):
        # String representation of the VoidType (returns its name)
        return self.name.fr

    def __repr__(self):
        # String representation of the VoidType (returns its name)
        return self.name.fr

    @property
    def id(self) -> int:
        # The ID of VoidType is always 0
        return 0

    @property
    def name(self):
        # The name property returns a Name object with translations for different languages
        return Name({'fr': 'Vide', 'en': 'Void', 'jp': '空の'})

    @property
    def sprites(self) -> str:
        # The sprites property returns an empty string for VoidType
        return ''

    @property
    def resistances(self):
        # VoidType has no resistances, so an empty list is returned
        return []

    @property
    def pokemons(self):
        class Pokemons:
            def __init__(self, ids):
                # Pokémon class is a container for Pokémon IDs with a get method
                self.ids = ids

            def get(self):
                # Get a list of Pokémon objects based on the stored IDs
                return [Pokemon(pokedex_id) for pokedex_id in self.ids]

        # Return an instance of the Pokémon class with an empty list of IDs
        return Pokemons([])

    @classmethod
    def put_with(cls, other):
        # Class method that returns the other type (used in type fusion)
        return other


class Name:
    def __init__(self, __data: dict):
        """Initialize a Name object with language-specific names.

        :param __data: A dictionary containing names in different languages
        (e.g., {'fr': 'French', 'en': 'English', 'jp': 'Japanese'}).
        """
        self.fr: str | list[str] = __data["fr"]  # French name or list of names
        self.en: str | list[str] = __data["en"]  # English name or list of names
        self.jp: str | list[str] = __data["jp"]  # Japanese name or list of names

    def __str__(self):
        """Return a string representation of the Name object.

        If the French name is a single string, it is returned. Otherwise,
        a comma-separated string of French names is returned.
        """
        if isinstance(self.fr, str):
            return self.fr
        else:
            return ', '.join(self.fr)

    def __repr__(self):
        """Return a string representation of the Name object.

        This method calls the __str__ method to provide a concise representation.
        """
        return str(self)


class Talent:
    def __init__(self, __data):
        """Initialize a Talent object with data from a talent.

        :param __data: Dictionary containing talent information, including name and talent_cache.
        """
        self.name: str = __data['name']  # Talent name
        self.talent_cache: bool = __data['tc']  # Talent cache information

    def __str__(self):
        """Return a string representation of the Talent object.

        This method returns the name of the talent.
        """
        return self.name

    def __repr__(self):
        """Return a string representation of the Talent object.

        This method returns the name of the talent and is used for a concise representation.
        """
        return self.name


class Sprites:
    def __init__(self, __data):
        """Initialize a Sprites object with sprite data.

        :param __data: Dictionary containing sprite information, including regular, shiny, and gmax sprites.
        """
        self.regular: str = __data['regular']  # Regular sprite URL
        self.shiny: str = __data['shiny']  # Shiny sprite URL
        self.gmax: Sprites2 = Sprites2(__data['gmax'])  # Gmax sprites information

    def __str__(self):
        """Return a string representation of the Sprites object.

        This method returns the regular sprite URL.
        """
        return self.regular

    def __repr__(self):
        """Return a string representation of the Sprites object.

        This method returns the last part of the regular sprite URL.
        """
        return self.regular.split('/')[-1]


class Sprites2:
    def __init__(self, __data):
        """Initialize a Sprites2 object with additional sprite data.

        :param __data: Dictionary containing additional sprite information, including regular and shiny sprites.
        """
        self.regular: str = __data['regular'] if __data is not None else ''  # Regular sprite URL or empty string
        self.shiny: str = __data['shiny'] if __data is not None else ''  # Shiny sprite URL or empty string

    def __str__(self):
        """Return a string representation of the Sprites2 object.

        This method returns the regular sprite URL.
        """
        return self.regular

    def __repr__(self):
        """Return a string representation of the Sprites2 object.

        This method returns the last part of the regular sprite URL.
        """
        return self.regular.split('/')[-1]


class Stats:
    def __init__(self, __data):
        """Initialize a Stats object with Pokémon stat data.

        :param __data: Dictionary containing Pokémon stat information,
        including HP, ATK, DEF, SPE_ATK, SPE_DEF, and VIT.
        """
        if __data is None:
            # If no stat data is provided, set all stats to 0
            self.hp_: int = 0
            self.atk_: int = 0
            self.def_: int = 0
            self.spe_atk_: int = 0
            self.spe_def_: int = 0
            self.vit_: int = 0
        else:
            # Assign stat values from the provided data
            self.hp_: int = __data["hp"]
            self.atk_: int = __data["atk"]
            self.def_: int = __data["def"]
            self.spe_atk_: int = __data["spe_atk"]
            self.spe_def_: int = __data["spe_def"]
            self.vit_: int = __data["vit"]

    def __str__(self):
        """Return a string representation of the Stats object.

        This method returns a formatted string containing the Pokémon's stats.
        """
        return "{" + (f"HP: {self.hp_}, ATK: {self.atk_}, DEF: {self.def_}, "
                      f"SPE ATK: {self.spe_atk_}, SPE DEF: {self.spe_def_}, VIT: {self.vit_}") + "}"

    def __repr__(self):
        """Return a string representation of the Stats object.

        This method returns a concise string representation of the Pokémon's stats.
        """
        return "{" + f"{self.hp_}, {self.atk_}, {self.def_}, {self.spe_atk_}, {self.spe_def_}, {self.vit_}" + "}"


class Resistance:
    def __init__(self, __data):
        """Initialize a Resistance object with resistance data.

        :param __data: Dictionary containing resistance information, including name and multiplier.
        """
        self.name: str = __data['name']  # Resistance name
        self.multiplier: float = __data['multiplier']  # Resistance multiplier

    def __str__(self):
        """Return a string representation of the Resistance object.

        This method returns the name of the resistance.
        """
        return self.name

    def __repr__(self):
        """Return a string representation of the Resistance object.

        This method returns the name of the resistance and is used for a concise representation.
        """
        return self.name


class Evolutions:
    def __init__(self, __data):
        """Initialize an Evolutions object with evolution data.

        :param __data: Dictionary containing evolution information,
        including pre-evolutions, next-evolutions, and mega-evolutions.
        """
        if __data is not None:
            # If evolution data is provided, create lists for pre-evolutions, next-evolutions, and mega-evolutions
            self.pre: list = [Evolution(data) for data in __data['pre']] if 'pre' in __data and __data[
                'pre'] is not None else []  # List of pre-evolutions
            self.next: list = [Evolution(data) for data in __data['next']] if 'next' in __data and __data[
                'next'] is not None else []  # List of next-evolutions
            self.mega: list = [Mega(data) for data in __data['mega']] if 'mega' in __data and __data[
                'mega'] is not None else []  # List of mega-evolutions
        else:
            # If no evolution data is provided, set all lists to empty
            self.pre: list = []  # List of pre-evolutions
            self.next: list = []  # List of next-evolutions
            self.mega: list = []  # List of mega-evolutions

    def __str__(self):
        """Return a string representation of the Evolutions object.

        This method returns a string concatenation of pre-evolutions, next-evolutions, and mega-evolutions.
        """
        return str(self.pre + self.next + self.mega)

    def __repr__(self):
        """Return a string representation of the Evolutions object.

        This method returns a concise representation of pre-evolutions, next-evolutions, and mega-evolutions.
        """
        return repr(self.pre + self.next + self.mega)


class Evolution:
    def __init__(self, __data):
        """Initialize an Evolution object with evolution data.

        :param __data: Dictionary containing evolution information, including pokedex_id, name, and condition.
        """
        self.pokedex_id: int = __data['pokedexId']  # Pokédex ID of the evolved Pokémon
        self.name: str = __data['name']  # Name of the evolved Pokémon
        if self.pokedex_id in [252, 496]:
            self.condition: str = __data['condition:']  # Evolution condition for specific cases
        else:
            self.condition: str = __data['condition'] if 'condition' in __data else ''  # Evolution condition

    def __str__(self):
        """Return a string representation of the Evolution object.

        This method returns the name of the evolved Pokémon.
        """
        return self.name

    def __repr__(self):
        """Return a string representation of the Evolution object.

        This method returns the name of the evolved Pokémon.
        """
        return self.name

    def get(self):
        """Return a Pokémon object representing the evolved Pokémon.

        This method returns a Pokémon object based on the pokedex_id.
        """
        return Pokemon(self.pokedex_id)


class Mega:
    def __init__(self, __data):
        """Initialize a Mega object with Mega evolution data.

        :param __data: Dictionary containing Mega evolution information, including orbe and sprites.
        """
        self.orbe: str = __data['orbe']  # Orbe information for Mega evolution
        self.sprites = Sprites2(__data['sprites'])  # Sprites information for Mega evolution

    def __str__(self):
        """Return a string representation of the Mega object.

        This method returns the orbe information for Mega evolution.
        """
        return self.orbe

    def __repr__(self):
        """Return a string representation of the Mega object.

        This method returns the orbe information for Mega evolution.
        """
        return self.orbe


class Sexe:
    def __init__(self, __data):
        """Initialize a Sexe object with gender data.

        :param __data: Dictionary containing gender information, including male and female counts.
        """
        if __data is not None:
            self.male: int = __data['male']  # Number of male Pokémon
            self.female: int = __data['female']  # Number of female Pokémon
        else:
            self.male: int = 0  # Default to 0 if no gender data is provided
            self.female: int = 0  # Default to 0 if no gender data is provided

    def __str__(self):
        """Return a string representation of the Sexe object.

        This method returns a formatted string containing the counts of male and female Pokémon.
        """
        return f"<male: {self.male}/female: {self.female}>"

    def __repr__(self):
        """Return a string representation of the Sexe object.

        This method returns a concise representation of the counts of male and female Pokémon.
        """
        return f"<{self.male}/{self.female}>"


class Forme:
    def __init__(self, __data, pokedex_id):
        """Initialize a Forme object with form data.

        :param __data: Dictionary containing form information, including region and name.
        :param pokedex_id: Pokédex ID of the Pokémon associated with this form.
        """
        self.region = list(__data.keys())[0]  # Region information for the form
        self.name = list(__data.values())[0]  # Name of the form

        # Lambda function to get the Pokémon associated with this form
        self.get = lambda: Pokemon(pokedex_id, region=self.region)

    def __str__(self):
        """Return a string representation of the Forme object.

        This method returns the name of the form.
        """
        return self.name

    def __repr__(self):
        """Return a string representation of the Forme object.

        This method returns the name of the form.
        """
        return self.name


# =-=-=-=-=-=-=-=-=-=-=-=-=

def get_all_pokemons():
    """Get the list of all Pokémon.

    :return: A list containing instances of the Pokémon class for each Pokémon.
    """
    return [Pokemon(data) for data in _call('pokemon')]


def get_all_types():
    """Get the list of all Types.

    :return: A list containing instances of the Type class for each Type.
    """
    return [Type(data) for data in _call('types')]
