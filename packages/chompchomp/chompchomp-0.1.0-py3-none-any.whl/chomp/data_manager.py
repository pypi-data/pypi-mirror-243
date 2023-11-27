from yaml import load, dump, Loader, Dumper

from os.path import expanduser

from chomp.utils import get_current_time_key
from chomp.food import Food

DEFAULT_FOOD_LIBRARY = expanduser("~/.chomp/food_library.yml")
DEFAULT_FOOD_DIARY = expanduser("~/.chomp/food_diary.yml")
DEFAULT_WEIGHT_DIARY = expanduser("~/.chomp/weight_diary.yml")

# food library


def get_food_library(library_file=DEFAULT_FOOD_LIBRARY):
    with open(library_file, "r") as f:
        items = load(f, Loader)
    library = {}
    for item in items:
        if "name" not in item:
            continue
        library[item["name"]] = Food.from_dict(item)
    return library


def add_food_library_entry(food, replace=True, library_file=DEFAULT_FOOD_LIBRARY):
    with open(library_file, "r") as f:
        library = load(f, Loader)
    if replace:
        food_name = food.get("name", "")
        library = [i for i in library if i.get("name", "") != food_name]
    library.append(food)

    with open(library_file, "w") as f:
        yaml_library = dump(library, Dumper=Dumper)
        f.write(yaml_library)


class FoodNotFoundException(Exception):
    pass


def get_food(name, library_file=DEFAULT_FOOD_LIBRARY):
    food_lib = get_food_library()
    if name in food_lib:
        return food_lib[name]
    raise FoodNotFoundException


# food diary


def add_food_diary_entry(food):
    """Reads in current food diary and adds a new time-stamped entry that includes
    the food's nutritional data
    """
    food_diary = get_food_diary()
    time_key = get_current_time_key()
    diary_entry = {"food": food}
    food_diary[time_key] = diary_entry
    write_food_diary(food_diary)


def get_food_diary():
    with open(DEFAULT_FOOD_DIARY, "r") as f:
        data = load(f, Loader=Loader)
    if data is None:
        data = {}
    return data


def write_food_diary(data, library_file=DEFAULT_FOOD_DIARY):
    yaml_diary = dump(data, Dumper=Dumper)
    with open(library_file, "w") as f:
        f.write(yaml_diary)


# weight diary


def add_weight_diary_entry(weight):
    weight_diary = get_weight_diary()

    time_key = get_current_time_key()
    diary_entry = {"weight": weight}
    weight_diary[time_key] = diary_entry
    write_weight_diary(weight_diary)


def get_weight_diary():
    with open(DEFAULT_WEIGHT_DIARY, "r") as f:
        data = load(f, Loader=Loader)
    if data is None:
        data = {}
    return data


def write_weight_diary(data):
    yaml_diary = dump(data, Dumper=Dumper)
    with open(DEFAULT_WEIGHT_DIARY, "w") as f:
        f.write(yaml_diary)
