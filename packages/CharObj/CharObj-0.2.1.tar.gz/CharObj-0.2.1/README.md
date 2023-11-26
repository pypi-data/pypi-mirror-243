# CharObj
## Description
CharObj is a package to allow for the creation/management of items for use in a text-based RPG game. It is designed to be used with the [CharActor](https://github.com/primal-coder/CharActor) package, but can be used independently.

## Installation
To install CharObj, use the following command:

```bash
pip install CharObj
```

## Usage
CharObj can be used as a Python module or as a command-line tool.

### Module
To use CharObj as a module, import it into your Python script:

```python
import CharObj
```

### Command-Line
To use CharObj as a command-line tool, use the following command:

```bash
python -m CharObj -h
# usage: CharObj [-h] {Get,Make} ...

# options:
#   -h, --help  show this help message and exit

# Commands:
#   {Get,Make}
#     Get       Gather information about an item by name or id
#     Make      Create an item
```

## Examples

### Module

Each already existing item is stored in its respective json file in the 'dict' directory. Upon importing the module items are accessible through the 'CharObj.Goods' or 'CharObj.Armory' classes. A new instance of the item can be created by simply calling its name as a function.


```python
>>> import CharObj
# Create a new instance of an item
>>> gold_coin_1 = CharObj.Goods.goldcoin()
>>> gold_coin_2 = CharObj.Goods.goldcoin()
# Print the name of the item
>>> print(gold_coin_1.name)
Gold Coin
>>> print(gold_coin_2.name)
Gold Coin
# Check if the two items are the same
>>> print(gold_coin_1 == gold_coin_2)
False
```

### Command-Line

# Get
```bash
$ python -m CharObj Get 1
Gold Coin
{'binding': 'UNBOUND',
 'category': 'MISC',
 'description': 'A gold coin',
 'item_id': 1,
 'material': 'GOLD',
 'mundane': True,
 'name': 'Gold Coin',
 'quality': 'COMMON',
 'quest_item': False,
 'relic': False,
 'stackable': True,
 'value': [1, 'gp'],
 'weight': [0.01, 'kg']}
```

# Make

The Make command can be used to create a new item. `CharObj Make` can be followed by the item's category. Each category can be executed with the `-h` flag to see the required arguments. The following example creates a new item in the 'Weapon' category.

```bash
$ python -m CharObj Make Weapon --item_name 'Dragonbone Blade' --slot MAIN_HAND --weight '3.5 kg' --material DRAGONBONE --mundane True --description 'A sharpened blade crafted from the bones of a defeated dragon.' --quality RARE --value '100 gp' --binding False --quest_item False --relic False --damage '1 d12' --damage_type SLASHING --range '5 FEET' --properties 'FINESSE LIGHT VERSATILE' --proficiency MARTIAL
```

Once made an item can be accessed in the same way as a pre-existing item, using the CLI ...
    
    ```bash
    $ python -m CharObj Get 'Dragonbone_Blade'
    ```

Or the module ...

    ```python
    >>> import CharObj
    >>> dragonbone_blade = CharObj.Armory.dragonboneblade()
    >>> print(dragonbone_blade.name)
    ```

Make can also be used interactively. The following example creates a new item in the 'Trade' category.

    ```bash
    >>> python -m CharObj Make -i
    Create an item?
    Press enter to continue. Press Ctrl+C to cancel.
    What category of item would you like to create?
    Options: (a)rmor, (w)eapon, (g)eneral, (t)rade, (T)oolt
    Creating Trade item.
    item_name:  Brightsteel Ore
    category:  ORE
    weight:  0.5 kg
    material:  BRIGHTSTEEL
    mundane:  True
    description:  A chunk of brightsteel ore.
    quality:  COMMON
    value:  5 gp
    binding:  False
    quest_item:  False
    relic:  False
    ```