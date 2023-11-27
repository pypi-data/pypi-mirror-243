from chomp.data_manager import (
    add_food_diary_entry,
    get_food,
    FoodNotFoundException,
)


def eat(food_name, weight=None, percent=1):
    if abs(percent - 1) < 0.001:
        print(f"You ate {food_name}")
    else:
        print(f"You ate {100 * percent:.1f}% of {food_name}")

    try:
        food = get_food(food_name)
        if weight:
            food_weight = food.get_nutritional_fact("weight")
            percent = weight / food_weight
        food = food * percent
        cal = round(food.get_nutritional_fact("calories"))
        print(f"You ate {cal} calories!!")
        add_food_diary_entry(food.to_dict())
    except FoodNotFoundException:
        print(f"Cannot find {food_name}!")
