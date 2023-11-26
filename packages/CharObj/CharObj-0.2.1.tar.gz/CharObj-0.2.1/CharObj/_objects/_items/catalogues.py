from __future__ import annotations
from abc import ABC as _ABC
from typing import Optional as _Optional, Union as _Union, List as _List
from .item import _ItemFactory, _GENERAL_DICT, _TRADE_DICT, _TOOLS_DICT
from ._weapon import _WeaponFactory, _WEAPONS_DICT
from ._clothing import _ClothingFactory, _CLOTHING_DICT
from ._armor import ArmorFactory, _ARMOR_DICT
from pyglet.event import EventDispatcher
import grid_engine as ge

GridObject = ge.grid_object

MANIFESTS = ['weapons', 'clothing', 'armor', 'general', 'trade', 'tools']
DICTS = [_WEAPONS_DICT, _CLOTHING_DICT, _ARMOR_DICT, _GENERAL_DICT, _TRADE_DICT, _TOOLS_DICT]


class Cell(_ABC):
    pass


class QuietDict:
    def __init__(self, manifest_names: _Optional[_Union[list[str, ], str]], *args, **kwargs):
        self.items = {}
        self._manidict1 = None
        self._manidict2 = None
        self._manidict3 = None
        if isinstance(manifest_names, list):
            for i in range(len(manifest_names)):
                name = manifest_names[i]
                setattr(self, f'{name}_manifest', [])
                setattr(self, f'_manidict{i}', DICTS[MANIFESTS.index(name)])
        else:
            setattr(self, f'{manifest_names}_manifest', [])

    def __getitem__(self, key):
        key = key.replace(' ', '').replace(',','_')
        return self.items[key]()

    def __setitem__(self, key, value):
        self.items[key] = value

    def __delitem__(self, key):
        del self.items[key]

    def __iter__(self):
        return iter(self.items)

    def __contains__(self, key):
        return key.replace(' ', '') in self.items.keys()

    def __repr__(self):
        return repr(self.items)

    def update(self, other=None, **kwargs):
        if other:
            if hasattr(other, "keys"):
                for key in other.keys():
                    self[key] = other[key]
            else:
                for key, value in other:
                    self[key] = value
        for key, value in kwargs.items():
            self[key] = value


def _create_armor(armor_name: str):
    _armor_class = ArmorFactory.create_armor(armor_name)
    if _armor_class is not None:
        return _armor_class


def _create_weapon(weapon_name: str):
    _weapon_class = _WeaponFactory.create_weapon(weapon_name)
    if _weapon_class is not None:
        return _weapon_class


class _Armory(QuietDict):
    def __init__(self):
        super(_Armory, self).__init__(['armor', 'weapons'])
        self._dict = {**_ARMOR_DICT, **_WEAPONS_DICT}
        self.weapons_manifest = []
        self.armor_manifest = []
        self._weapon_classes = {}
        self._armor_classes = {}
        self._grid_instances = {}
        self._create_armor_classes()
        self._create_weapon_classes()

    def _create_armor_classes(self):
        for _armor_name, _armor_attr in _ARMOR_DICT.items():
            _armor_class = _create_armor(_armor_name.replace(" ", "").replace(",", "_"))
            if _armor_class is not None:
                setattr(_armor_class, '_entry', _armor_attr)
                self._armor_classes[_armor_name.replace(" ", "").replace(",", "_")] = _armor_class
                setattr(self, _armor_name.replace(" ", "").replace(",", "_").lower(), _armor_class)
                self.armor_manifest.append(_ARMOR_DICT[_armor_name]['name'])
        self.update(self._armor_classes)

    def _create_weapon_classes(self):
        for _weapon_name, _weapon_attr in _WEAPONS_DICT.items():
            _weapon_class = _create_weapon(_weapon_name.replace(" ", "").replace(",", "_"))
            if _weapon_class is not None:
                setattr(_weapon_class, '_entry', _weapon_attr)
                # _weapon_instance = _weapon_class(**_WEAPONS_DICT[_weapon_name])
                # _weapon_instances[_weapon_instance.name] = _weapon_instance
                self._weapon_classes[_weapon_name.replace(" ", "").replace(",", "_").replace("-", "")] = _weapon_class
                setattr(self, _weapon_name.replace(" ", "").replace(",", "_").replace("-", "").lower(), _weapon_class)
                self.weapons_manifest.append(_WEAPONS_DICT[_weapon_name]['name'])
        self.update(self._weapon_classes)

    def _get_class(self, item_name: str):
        if item_name in self.items:
            return self.items[item_name]

    def get(self, item_name: str, grid: object = None, cell: object = None):
        item_name = item_name.title()
        if grid or cell:
            item = self._create_grid_item(item_name, grid, cell)
            setattr(item, 'tile_color', (255, 0, 0, 255))
            cell = grid[cell] if cell is not None and isinstance(cell, str) else cell
            cell.add_object(item)
            return item
        item_class = self._get_class(item_name)
        return item_class()

    def _create_grid_item(self, item_name, grid: any = None, cell: _Union[str, type(Cell)] = None):
        item_class = self._get_class(item_name)
        cell = grid[cell] if cell is not None and isinstance(cell, str) else cell
        grid_item_instance = GridObject.GridItem(grid, item_name, cell)
        if self._grid_instances.get(item_name, None) is not None:
            item_count = 1 + sum(
                    bool(key.startswith(item_name))
                    for key in list(self._grid_instances.keys())
                    )
            self._grid_instances[f'{item_name}{item_count}'] = grid_item_instance
        else:
            self._grid_instances[item_name] = grid_item_instance
        return grid_item_instance


class _Goods(QuietDict):
    def __init__(self):
        super(_Goods, self).__init__(['general', 'trade', 'tools'])
        self._goods_classes = {}
        self._grid_instances = {}
        self._create_item_classes()

    def _create_item(self, item_name: str):
        if item_name in list(_GENERAL_DICT.keys())+list(_TRADE_DICT.keys())+list(_TOOLS_DICT.keys()):
            _item_class = _ItemFactory.create_item(item_name)
        return _item_class

    def _get_class(self, item_name: str):
        if item_name in self.items and (
                item_name in self.general_manifest
                or item_name in self.trade_manifest
        ):
            return self.items[item_name]

    def _create_item_classes(self):
        for item_kind in ['general', 'trade', 'tools']:
            setattr(self, f'{item_kind}', type(f'{item_kind.capitalize()}', (QuietDict, ), {}))
        self.general = self.general('general')
        self.trade = self.trade('trade')
        self.tools = self.tools('tools')
        for _item_name, _item_attr in _GENERAL_DICT.items():
            _item_class = self._create_item(_item_name)
            if _item_class is not None:
                setattr(_item_class, '_entry', _item_attr)
                # _item_instance = _item_class(**_GENERAL_DICT[_item_name])
                # _goods_instances[_item_instance.name] = _item_instance
                self._goods_classes[_item_name.replace(" ", "").replace(",", "_").replace("-", "")] = _item_class
                setattr(
                    self.general, _item_name.replace(" ", "").replace(",", "_").replace("-", "").replace("'", "").lower(),
                    _item_class
                    )
                self.general_manifest.append(_item_name)
        for _item_name, _item_attr in _TRADE_DICT.items():
            _item_class = self._create_item(_item_name)
            if _item_class is not None:
                setattr(_item_class, '_entry', _item_attr)
                # _item_instance = _item_class(**_TRADE_DICT[_item_name])
                # _goods_instances[_item_instance.name] = _item_instance
                self._goods_classes[_item_name.replace(" ", "").replace(",", "_").replace("-", "")] = _item_class
                setattr(
                    self.trade, _item_name.replace(" ", "").replace(",", "_").replace("-", "").replace("'", '').lower(),
                    _item_class
                    )
                self.trade_manifest.append(_item_name)
        for _item_name, _item_attr in _TOOLS_DICT.items():
            _item_class = self._create_item(_item_name)
            if _item_class is not None:
                setattr(_item_class, '_entry', _item_attr)
                self._goods_classes[_item_name.replace(" ", "").replace(",", "_").replace("-", "")] = _item_class
                setattr(
                    self.tools, _item_name.replace(" ", "").replace(",", "_").replace("-", "").replace("'", '').lower(),
                    _item_class
                    )
                self.tools_manifest.append(_item_name)
        for _item_name, _item_attr in self._goods_classes.items():
            if _item_name in self.general_manifest:
                self.general.update({_item_name: _item_attr})
            elif _item_name in self.trade_manifest:
                self.trade.update({_item_name: _item_attr})
            elif _item_name in self.tools_manifest:
                self.tools.update({_item_name: _item_attr})
        self.update(self._goods_classes)

    def get(self, item_name: str, grid: object = None, cell: object = None):
        item_name = item_name.title()
        if grid or cell:
            item = self._create_griditem(item_name, grid, cell)
            setattr(item, 'tile_color', (0, 255, 255, 255))
            cell = grid[cell] if cell is not None and isinstance(cell, str) else cell
            cell.add_object(item)
            return item

        return self[item_name]

    def _create_griditem(self, item_name, grid, cell: _Union[str, type(Cell)]):
        item_class = self._get_class(item_name)
        item_meta = self._create_grid_meta(item_name, item_class)
        cell = grid[cell] if cell is not None and isinstance(cell, str) else cell
        griditem_instance = GridItem(grid, item_name, cell)
        if self._grid_instances.get(item_name, None) is not None:
            item_count = 1 + sum(
                    bool(key.startswith(item_name))
                    for key in list(self._grid_instances.keys())
                    )
            self._grid_instances[f'{item_name}{item_count}'] = griditem_instance
        else:
            self._grid_instances[item_name] = griditem_instance
        return griditem_instance


Armory = _Armory()
# _weapon_classes = {}

# for _weapon_name, _weapon_attr in _WEAPONS_DICT.items():
#     _weapon_class = _WeaponFactory.create_weapon(_weapon_name)
#     if _weapon_class is not None:
#         # _weapon_instance = _weapon_class(**_WEAPONS_DICT[_weapon_name])
#         # _weapon_instances[_weapon_instance.name] = _weapon_instance
#         _weapon_classes[_weapon_name.replace(" ", "").replace(",", "_").replace("-","")] = _weapon_class
#         setattr(Armory, _weapon_name.replace(" ", "").replace(",", "_").replace("-","").lower(), _weapon_class)
#         Armory.weapons_manifest.append(_WEAPONS_DICT[_weapon_name]['name'])
# Armory.update(_weapon_classes)

# _armor_classes = {}
# for _armor_name, _armor_attr in _ARMOR_DICT.items():
#     _armor_class = ArmorFactory.create_armor(_armor_name)
#     if _armor_class is not None:
#         # _armor_instance = _armor_class(**_ARMOR_DICT[_armor_name])
#         # _armor_instances[_armor_instance.name] = _armor_instance
#         _armor_classes[_armor_name.replace(" ", "").replace(",", "_").replace("-","")] = _armor_class
#         setattr(Armory, _armor_name.replace(" ", "").replace(",", "_").replace("-","").lower(), _armor_class)
#         Armory.armor_manifest.append(_armor_name)
# Armory.update(_armor_classes)

Goods = _Goods()

# _goods_classes = {}

# for _item_name, _item_attr in _GENERAL_DICT.items():
#     _item_class = _ItemFactory.create_general_item(_item_name)
#     if _item_class is not None:
#         # _item_instance = _item_class(**_GENERAL_DICT[_item_name])
#         # _goods_instances[_item_instance.name] = _item_instance
#         _goods_classes[_item_name.replace(" ", "").replace(",", "_").replace("-","")] = _item_class
#         setattr(Goods, _item_name.replace(" ", "").replace(",", "_").replace("-","").replace("'",'').lower(),
#         _item_class)
#         Goods.general_manifest.append(_item_name)
# for _item_name, _item_attr in _TRADE_DICT.items():
#     _item_class = _ItemFactory.create_trade_item(_item_name)
#     if _item_class is not None:
#         # _item_instance = _item_class(**_TRADE_DICT[_item_name])
#         # _goods_instances[_item_instance.name] = _item_instance
#         _goods_classes[_item_name.replace(" ", "").replace(",", "_").replace("-","")] = _item_class
#         setattr(Goods, _item_name.replace(" ", "").replace(",", "_").replace("-","").replace("'",'').lower(), _item_class)
#         Goods.trade_manifest.append(_item_name)
# Goods.update(_goods_classes)
