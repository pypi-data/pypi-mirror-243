import os
import json

def load_json(path):
    """Load a JSON file from the given path."""
    with open(path, 'r') as f:
        return json.load(f)
    
# Desc: Loads dicts from JSON files
_dicts = [d[:-5] for d in os.listdir(os.path.abspath(os.path.dirname(__file__))) if d.endswith('.json') and d != '__init__.py']


def load_dict(name):
    if name in _dicts:
        return load_json(f'{os.path.join(os.path.dirname(__file__), name)}.json')
    else:
        raise ValueError(f'No such dict: {name}')
    
def save_dict(name, data):
    if name not in _dicts:
        raise ValueError(f'No such dict: {name}. If you wish to create a new dict, use save_new_dict()')
    with open(f'{os.path.join(os.path.dirname(__file__), name)}.json', 'w') as f:
        json.dump(data, f, indent=4)

def save_new_dict(name, data):
    if name in _dicts:
        raise ValueError(f'Dict {name} already exists. If you wish to overwrite it, use save_dict()')
    with open(f'{os.path.join(os.path.dirname(__file__), name)}.json', 'w') as f:
        json.dump(data, f, indent=4)
    
def load_all_dicts():
    return {d: load_dict(d) for d in _dicts}

# Desc: Loads lists from text files
_lists = [d[:-9] for d in os.listdir(os.path.dirname(__file__)) if d.endswith('_list.txt') and d != '__init__.py']

def load_list(name):
    if name not in _lists:
        raise ValueError(f'No such list: {name}')
    with open(f'{os.path.join(os.path.dirname(__file__), name)}_list.txt', 'r') as f:
        return [l.strip() for l in f.readlines()]

def _set_ids(MASTER_CATALOGUE):
    _ITEM_ID = 0
    for I, catalogue in enumerate(_MASTER_CATALOGUE):
        if I != 0:
            _ITEM_ID += len(_MASTER_CATALOGUE.copy()[catalogue])
        for name, info in _MASTER_CATALOGUE[catalogue].copy().items():
            _MASTER_CATALOGUE[catalogue][name]['item_id'] = _ITEM_ID
            _ITEM_ID += 1
        
def _update_catalogues():
    _MASTER_CATALOGUE = load_all_dicts()
    _set_ids(_MASTER_CATALOGUE)
    _ARMOR_DICT = _MASTER_CATALOGUE['armor']
    _WEAPONS_DICT = _MASTER_CATALOGUE['weapons']
    _GENERAL_DICT = _MASTER_CATALOGUE['general_items']
    _TRADE_DICT = _MASTER_CATALOGUE['trade_items']
    _TOOLS_DICT = _MASTER_CATALOGUE['tools']
    
_MASTER_CATALOGUE = load_all_dicts()

_set_ids(_MASTER_CATALOGUE)

_ARMOR_DICT = _MASTER_CATALOGUE['armor']
_WEAPONS_DICT = _MASTER_CATALOGUE['weapons']
_GENERAL_DICT = _MASTER_CATALOGUE['general_items']
_TRADE_DICT = _MASTER_CATALOGUE['trade_items']
_TOOLS_DICT = _MASTER_CATALOGUE['tools']

def create_new_item_entry(
    dict_name: str = None,
    key: str = None,
    item_name: str = None,
    slot: str = None,
    category: str = None,
    weight: tuple[float, str] = None,
    material: str = None,
    mundane: bool = None,
    description: str = None,
    quality: str = None,
    value: tuple[int, str] = None,
    binding: bool = None,
    quest_item: bool = None,
    relic: bool = None,
    damage: list[int, int] = None,
    damage_type: str = None,
    proficiency: str = None,
    weapon_range: list[int, str] = None,
    weapon_properties: list[str] = None,
    armor_class: int = None,
    set_name: str = None,
    stackable: bool = None
):
    if dict_name is None:
        raise ValueError('No dict name provided')
    if key is None:
        raise ValueError('No key provided')
    if item_name is None:
        raise ValueError('No item name provided')
    if category is None:
        raise ValueError('No category provided')
    if category == 'ARMOR':
        if armor_class is None:
            raise ValueError('No armor class provided')
        if set_name is None:
            raise ValueError('No set name provided')
        entry = {
            'name': item_name,
            'slot': slot,
            'category': category,
            'weight': weight,
            'material': material,
            'mundane': mundane,
            'description': description,
            'quality': quality,
            'value': value,
            'armor_class': armor_class,
            'set_name': set_name,
            'binding': binding,
            'quest_item': quest_item,
            'relic': relic
        }
    elif category == 'WEAPON':
        if damage is None:
            raise ValueError('No damage provided')
        if damage_type is None:
            raise ValueError('No damage type provided')
        if proficiency is None:
            raise ValueError('No proficiency provided')
        if weapon_range is None:
            raise ValueError('No weapon range provided')
        if weapon_properties is None:
            raise ValueError('No weapon properties provided')
        entry = {
            'name': item_name,
            'slot': slot,
            'category': category,
            'weight': weight,
            'material': material,
            'mundane': mundane,
            'description': description,
            'quality': quality,
            'value': value,
            'damage': damage,
            'damage_type': damage_type,
            'proficiency': proficiency,
            'weapon_range': weapon_range,
            'weapon_properties': weapon_properties,
            'binding': binding,
            'quest_item': quest_item,
            'relic': relic
        }
    else:
        entry = {
            'name': item_name,
            'slot': slot,
            'category': category,
            'weight': weight,
            'material': material,
            'mundane': mundane,
            'description': description,
            'quality': quality,
            'value': value,
            'binding': binding,
            'quest_item': quest_item,
            'relic': relic
        }
    target_dict = load_dict(dict_name)
    target_dict[key] = entry
    save_dict(dict_name, target_dict)
    _update_catalogues()
    
def create_new_weapon_entry(
    key: str = None,
    item_name: str = None,
    slot: str = None,
    weight: tuple[float, str] = None,
    material: str = None,
    mundane: bool = None,
    description: str = None,
    quality: str = None,
    value: tuple[int, str] = None,
    damage: list[int, int] = None,
    damage_type: str = None,
    proficiency: str = None,
    weapon_range: list[int, str] = None,
    weapon_properties: list[str] = None,
    binding: bool = None,
    quest_item: bool = None,
    relic: bool = None
):
    return create_new_item_entry('weapons', key, item_name, slot, 'WEAPON', weight, material, mundane, description, quality, value, binding, quest_item, relic, damage, damage_type, proficiency, weapon_range, weapon_properties, None, None)

def create_new_armor_entry(
    key: str = None,
    item_name: str = None,
    slot: str = None,
    weight: tuple[float, str] = None,
    material: str = None,
    mundane: bool = None,
    description: str = None,
    quality: str = None,
    value: tuple[int, str] = None,
    armor_class: int = None,
    set_name: str = None,
    binding: bool = None,
    quest_item: bool = None,
    relic: bool = None
):
    return create_new_item_entry('armor', key, item_name, slot, 'ARMOR', weight, material, mundane, description, quality, value, armor_class, set_name, binding, quest_item, relic)

def create_new_general_item_entry(
    key: str = None,
    item_name: str = None,
    slot: str = None,
    weight: tuple[float, str] = None,
    material: str = None,
    mundane: bool = None,
    description: str = None,
    quality: str = None,
    value: tuple[int, str] = None,
    binding: bool = None,
    quest_item: bool = None,
    relic: bool = None
):
    return create_new_item_entry('general_items', key, item_name, slot, 'GENERAL', weight, material, mundane, description, quality, value, None, None, binding, quest_item, relic)

def create_new_trade_item_entry(
    key: str = None,
    item_name: str = None,
    slot: str = None,
    category: str = None,
    weight: tuple[float, str] = None,
    material: str = None,
    mundane: bool = None,
    description: str = None,
    quality: str = None,
    value: tuple[int, str] = None,
    binding: bool = None,
    quest_item: bool = None,
    relic: bool = None
):
    return create_new_item_entry('trade_items', key, item_name, slot, category, weight, material, mundane, description, quality, value, None, None, binding, quest_item, relic)

def create_new_tool_entry(
    key: str = None,
    item_name: str = None,
    slot: str = None,
    weight: tuple[float, str] = None,
    material: str = None,
    mundane: bool = None,
    description: str = None,
    quality: str = None,
    value: tuple[int, str] = None,
    binding: bool = None,
    quest_item: bool = None,
    relic: bool = None
):
    return create_new_item_entry('tools', key, item_name, slot, 'TOOL', weight, material, mundane, description, quality, value, None, None, binding, quest_item, relic)

