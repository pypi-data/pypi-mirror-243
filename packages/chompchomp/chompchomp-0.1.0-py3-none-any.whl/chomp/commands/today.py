from copy import copy
from datetime import datetime

from tabulate import tabulate

from chomp.config_manager import get_nutritional_targets
from chomp.food import Food
from chomp.data_manager import (
    get_food_diary,
)
from chomp.config_manager import get_nutritional_targets
from chomp.utils import get_beginning_of_day_timestamp


def today(short=False):
    food_diary = get_food_diary()
    start_of_day = get_beginning_of_day_timestamp()

    lines = [
        [
            "Time of Day",
            "Food",
            "Calories",
            "Fat",
            "Protein",
            "Carbs",
            "Cholesterol",
            "Caffeine",
        ]
    ]

    combined_intake = None
    for timestamp in food_diary:
        if int(timestamp) < start_of_day:
            continue

        entry = food_diary[timestamp]
        if "food" not in entry:
            print(" missing food diary data for entry.. skipping")
            continue

        time_of_day = datetime.fromtimestamp(int(timestamp))
        food = Food.from_dict(entry["food"])
        name = food.name
        calories = round(food.get_nutritional_fact("calories") or 0)
        fat = round(food.get_nutritional_fact("fat.total") or 0)
        protein = round(food.get_nutritional_fact("protein") or 0)
        carbs = round(food.get_nutritional_fact("carbohydrates.total") or 0)
        cholesterol = round(food.get_nutritional_fact("cholesterol") or 0, 3)
        caffeine = round(food.get_nutritional_fact("caffeine") or 0, 3)
        lines.append(
            [time_of_day, name, calories, fat, protein, carbs, cholesterol, caffeine]
        )

        if combined_intake is None:
            combined_intake = food
        else:
            combined_intake += food

    if combined_intake is None:
        print("No food recorded for today!")
        return

    if short:
        total_calories = int(combined_intake.get_nutritional_fact("calories"))
        target_calories = int(get_nutritional_targets().get("calories", 0))
        remaining_calories = target_calories - total_calories
        print(
            f"Total calories for today:      {int(combined_intake.get_nutritional_fact('calories')):4}"
        )
        if target_calories:
            if remaining_calories > 0:
                print(
                    f"Remaining calories for today:  {remaining_calories:4} (out of {target_calories})"
                )
            elif remaining_calories == 0:
                print(f"No more calories left today!")
            else:
                print(
                    f"Calories consumed beyond goal: {-1 * remaining_calories:4} (goal was {target_calories})"
                )
        return

    print(tabulate(lines, headers="firstrow", tablefmt="rounded_outline"))

    print()

    lines = [
        [
            "Total Calories",
            "Total Fat",
            "Total Protein",
            "Total Carbs",
            "Total Cholesterol",
            "Total Caffeine",
        ]
    ]
    lines.append(
        [
            round(combined_intake.get_nutritional_fact("calories") or 0),
            round(combined_intake.get_nutritional_fact("fat.total") or 0),
            round(combined_intake.get_nutritional_fact("protein") or 0),
            round(combined_intake.get_nutritional_fact("carbohydrates.total") or 0),
            round(combined_intake.get_nutritional_fact("cholesterol") or 0, 3),
            round(combined_intake.get_nutritional_fact("caffeine") or 0, 3),
        ]
    )
    print(tabulate(lines, headers="firstrow", tablefmt="rounded_outline"))

    targets = get_nutritional_targets()
    if targets:
        calories = targets.get("calories", 0)
        fat = targets.get("fat", 0)
        protein = targets.get("protein", 0)
        carbs = targets.get("carbs", 0)
        cholesterol = targets.get("cholesterol", 0)
        caffeine = targets.get("caffeine", 0)
        lines = [
            [
                "Daily Calories",
                "Daily Fat",
                "Daily Protein",
                "Daily Carbs",
                "Daily Cholesterol",
                "Daily Caffeine",
            ],
            [calories, fat, protein, carbs, cholesterol, caffeine],
        ]
        print(tabulate(lines, headers="firstrow", tablefmt="rounded_outline"))
