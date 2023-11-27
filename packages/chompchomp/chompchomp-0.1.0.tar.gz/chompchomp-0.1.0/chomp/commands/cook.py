from chomp.data_manager import (
    add_food_library_entry,
    get_food,
    FoodNotFoundException,
)


def cook(recipe_name, ingredient_name, weight=None, percent=1):
    new_recipe = False
    try:
        recipe = get_food(recipe_name)
    except FoodNotFoundException:
        print(f"Preparing new recipe for {recipe_name}!")
        new_recipe = True

    try:
        ingredient = get_food(ingredient_name)
    except FoodNotFoundException:
        print(f"Unable to find ingredient ({ingredient_name})")
        return

    if weight:
        ingredient_weight = ingredient.get_nutritional_fact("weight")
        percent = weight / ingredient_weight
        print(f"Adding {weight} grams of {ingredient_name} to {recipe_name} recipe")
    elif abs(percent - 1) > 0.001:
        print(
            f"Adding {100 * percent:.1f}% of {ingredient_name} to {recipe_name} recipe"
        )
    else:
        print(f"Adding {ingredient_name} to {recipe_name} recipe")

    ingredient *= percent

    if new_recipe:
        recipe = ingredient
    else:
        recipe += ingredient

    recipe.name = recipe_name
    recipe.brand = "(recipe)"

    # create or update recipe
    add_food_library_entry(recipe.to_dict(), replace=True)
