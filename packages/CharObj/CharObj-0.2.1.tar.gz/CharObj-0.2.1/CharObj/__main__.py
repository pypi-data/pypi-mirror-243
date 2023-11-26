from colorama import Fore
from argparse import ArgumentParser, Action
import sys

from CharObj._dicts import *

R = Fore.RESET
r = Fore.RED
g = Fore.GREEN
b = Fore.BLUE
y = Fore.YELLOW

ALL_FIELDS = ['item_name', 'slot', 'weight', 'material', 'mundane', 'description', 'quality', 'value', 'binding', 'quest_item', 'relic', 'armor_class', 'damage', 'damage_type', 'range', 'set_name']
ARMOR_FIELDS = ['item_name', 'slot', 'weight', 'material', 'mundane', 'description', 'quality', 'value', 'binding', 'quest_item', 'relic', 'armor_class', 'set_name']
WEAPON_FIELDS = ['item_name', 'slot', 'weight', 'material', 'mundane', 'description', 'quality', 'value', 'damage', 'damage_type', 'proficiency', 'range', 'properties', 'binding', 'quest_item', 'relic']
TRADE_FIELDS = ['item_name', 'category', 'weight', 'material', 'mundane', 'description', 'quality', 'value', 'binding', 'quest_item', 'relic']
OTHER_FIELDS = ['item_name', 'weight', 'material', 'mundane', 'description', 'quality', 'value', 'binding', 'quest_item', 'relic']
FIELDS = {'Armor': ARMOR_FIELDS, 'Weapon': WEAPON_FIELDS, 'General': OTHER_FIELDS, 'Trade': TRADE_FIELDS, 'Tool': OTHER_FIELDS}
FUNCS = {'Armor': create_new_armor_entry, 'Weapon': create_new_weapon_entry, 'General': create_new_general_item_entry, 'Trade': create_new_trade_item_entry, 'Tool': create_new_tool_entry}


def comma_or_space_split(value):
    # Split the value by comma or space
    return value.replace(',', ' ').split()

class SplitValues(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        # Split the values by comma or space
        setattr(namespace, self.dest, comma_or_space_split(values))

def interactive_info(category: str):
    if category == 'a':
        fields = _extracted_from_interactive_info_3('Armor')
    elif category == 'w':
        fields = _extracted_from_interactive_info_3('Weapon')
    elif category in {'g', 't', 'T'}:
        cat = 'General' if category == 'g' else 'Trade' if category == 't' else 'Tool'
        fields = _extracted_from_interactive_info_3(cat)
    for field in fields:
        print(f'{b}{field}{R}: {g}')
    print('Fields left blank may be automatically filled.')
    for _ in range(len(fields) + 1):
        sys.stdout.write('\033[F')
    sys.stdout.write('\r')
    info = {}
    for field in fields:
        print(f'{b}{field}{R}: {g}', end=' ')
        i = input()
        if i == '':
            i = None
        if field == 'weight':
            i = i.split(' ')
            i0 = float(i[0])
            i1 = i[1]
            info['weight'] = (i0, i1)
        elif field in ['mundane', 'binding', 'quest_item', 'relic']:
            i = i.lower() in {'true', 't', 'yes', 'y'}
            info[field] = i
        elif field == 'value':
            i = i.split(' ')
            i0 = int(i[0])
            i1 = i[1]
            info['value'] = (i0, i1)
        elif field == 'damage':
            i = i.split(' ')
            i0 = int(i[0])
            i1 = int(i[1])
            info['damage'] = [i0, i1]
        elif field == 'range':
            i = i.split(' ')
            i0 = int(i[0])
            i1 = i[1]
            info['weapon_range'] = [i0, i1]
        elif field == 'properties':
            i = i.split(' ')
            info['weapon_properties'] = i
        else:
            info[field] = i
    info['key'] = info['item_name'].title()
    return info


# TODO Rename this here and in `interactive_info`
def _extracted_from_interactive_info_3(category):
    result = FIELDS[category]
    print(f'Creating {category} item.')
    return result
        


argparser = ArgumentParser(prog='CharObj')
subparsers = argparser.add_subparsers(title='Commands', dest='command')

getparser = subparsers.add_parser('Get', help='Gather information about an item by name or id')
makeparser = subparsers.add_parser('Make', help='Create an item')

makeparser.add_argument('--interactive', '-i', dest='interactive', action='store_true', help='Create an item interactively')

submakeparser = makeparser.add_subparsers(title='Item Categories', dest='category')

armorparser = submakeparser.add_parser('Armor', help='Create an armor item')
weaponparser = submakeparser.add_parser('Weapon', help='Create a weapon item')
generalparser = submakeparser.add_parser('General', help='Create a general item')
tradeparser = submakeparser.add_parser('Trade', help='Create a trade item')
toolparser = submakeparser.add_parser('Tool', help='Create a tool item')

for parser in [armorparser, weaponparser, generalparser, tradeparser, toolparser]:
    if parser == armorparser:
        fields = ARMOR_FIELDS
    elif parser == weaponparser:
        fields = WEAPON_FIELDS
    elif parser in {generalparser, tradeparser, toolparser}:
        fields = OTHER_FIELDS
    for field in fields:
        if field in ['weight', 'value', 'damage', 'range', 'properties']:
            getattr(parser, 'add_argument')(f'--{field}', action=SplitValues)
        else:
            getattr(parser, 'add_argument')(f'--{field}')

getparser.add_argument('--category', '-c', action='store_true', help='Return all items in a given category')
getparser.add_argument(dest='TERM', type=str, nargs='?', help='The term related to the search. If no flag is \
present the term will be treated as either an item name or id.')


args = argparser.parse_args()


if __name__ == '__main__':
    from CharObj import get_item, get_category
    if args.command == 'Get':
        if args.category:
            get_category(args.TERM)
        elif args.TERM.isdigit():
            get_item(int(args.TERM))
        else:
            get_item(args.TERM)
    elif args.command == 'Make':
        from CharObj import Item as _Item
        from CharObj._dicts import *
        if args.interactive:
            print('Create an item?')
            print(f'Press {g}enter{R} to continue. Press {r}Ctrl+C{R} to cancel.', end='\r')
            try:
                input()
            except KeyboardInterrupt:
                print('Cancelled.')
            print('What category of item would you like to create?')
            cat = input(f'Options: ({y}a{R})rmor, ({y}w{R})eapon, ({y}g{R})eneral, ({y}t{R})rade, ({y}T{R})ool')
            info = interactive_info(cat)        
            item: _Item = _Item(**info)
            if cat == 'a':
                create_new_armor_entry(**info)
            elif cat == 'w':
                create_new_weapon_entry(**info)
            elif cat == 'g':
                create_new_general_item_entry(**info)
            elif cat == 't':
                create_new_trade_item_entry(**info)
            elif cat == 'T':
                create_new_tool_entry(**info)
        elif args.category in {'Armor', 'Weapon', 'General', 'Trade', 'Tool'}:
            info = {field: getattr(args, field) for field in FIELDS[args.category]}
            info['weight'] = (float(info['weight'][0]), info['weight'][1])
            info['value'] = (int(info['value'][0]), info['value'][1])
            if args.category == 'Weapon':
                info['damage'] = [int(info['damage'][0]), info['damage'][1]]
                info['weapon_range'] = [int(info['range'][0]), info['range'][1]]
                del info['range']
                info['weapon_properties'] = info['properties']
                del info['properties']
            info['key'] = info['item_name'].title()
            FUNCS[args.category](**info)
        else:
            raise ValueError('Invalid command')