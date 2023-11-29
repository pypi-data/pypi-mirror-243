# <a href="https://tyradex.tech/"><img src="https://tyradex.tech/assets/logo.png" alt="Logo Pokémon"/></a> Tyradex for Python
[![PyPI version](https://badge.fury.io/py/Tyradex.svg)](https://badge.fury.io/py/Tyradex)
[![Supported Versions](https://img.shields.io/pypi/pyversions/Tyradex.svg)](https://pypi.org/project/Tyradex)
[![Downloads](https://static.pepy.tech/badge/Tyradex/month)](https://pepy.tech/project/Tyradex)
[![Contributors](https://img.shields.io/github/contributors/LassaInora/Tyradex.svg)](https://github.com/LassaInora/Tyradex/graphs/contributors)

-> 🇫🇷 : [README_FRENCH.md](https://github.com/LassaInora/Tyradex/blob/main/README_FRENCH.md)

## Overview
This Python script interacts with the [Tyradex API](https://tyradex.tech/) to retrieve detailed information about Pokémon and Pokémon types. It is designed to provide easy access to details such as Pokédex ID, generation, category, statistics, etc., for individual Pokémon or types. The script is organized into classes representing different aspects of Pokémon data and includes functions to obtain lists of all Pokémon and types.

## Features
- ### Pokemon Class :
  - Retrieve detailed information about a specific Pokémon.
  - Access properties such as Pokédex ID, generation, category, statistics, etc.

- ### Type Class :

  - Get information about a specific Pokémon type.
  - Access properties such as type ID, resistances, and a list of Pokémon associated with that type.

- ### Generations Class :

  - Access Pokémon data grouped by different generations.

- ### Support Classes :

  - Various support classes to handle names, abilities, sprites, statistics, resistances, evolutions, gender, and forms.

- ### Functions :

  - `get_all_pokemons` : Retrieve a list of all Pokémon.
  - `get_all_types` : Retrieve a list of all Pokémon types.

## How to Use
1) ### Installation :

  - Make sure you have Python installed on your system.
  - Install the library with `pip install --upgrade Tyradex`.

2) ### Usage :

  - Import the script into your Python project or run it as a standalone script.
  - Instantiate relevant classes to interact with Pokémon or types.
  - Explore the provided functions to get lists of Pokémon and types.

```python
# Example Usage
from Tyradex import Pokemon, Type, Generations, get_all_pokemons, get_all_types

# Retrieve information about a specific Pokémon
charizard = Pokemon('charizard')
print(charizard.name)

# Retrieve information about a specific Pokémon type
fire_type = Type('fire')
print(fire_type.name)

# Retrieve all Pokémon of a specific generation
gen_6 = Generations.Gen(6)
print(gen_6[42])

# Retrieve a list of all Pokémon and types
all_pokemons = get_all_pokemons()
all_types = get_all_types()
```
## Dependencies
- `requests` : Requests is an HTTP library, written in Python, for human beings.
- `unidecode` : Transliterate Unicode text into plain 7-bit ASCII.

## API Reference
- The script interacts with the Pokémon API hosted at https://tyradex.tech/api/v1/.
- Refer to the [API documentation](https://tyradex.tech/docs) for more details on available endpoints and data structure.

## Contributors
- API created by:
  - [Yarkis](https://github.com/Yarkis01)
  - [Ashzuu](https://github.com/Ashzuu)
- Python adaptation by:
  - [LassaInora](https://github.com/LassaInora)

## License
This project is under the [MIT License](https://github.com/Yarkis01/PokeAPI/blob/main/LICENSE).
