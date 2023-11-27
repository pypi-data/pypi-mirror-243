#!/usr/bin/env python3

import argparse

from chomp.commands import eat, cook, measure, stats, today, weight, lookup_food


def main():
    parser = argparse.ArgumentParser(prog="chomp")
    subparsers = parser.add_subparsers(help="sub-command help")

    # eat subparser
    parser_eat = subparsers.add_parser("eat", help="adds a meal to your food diary")
    parser_eat.add_argument("food", type=str, help="food that you ate")
    parser_eat.add_argument(
        "--percent",
        type=float,
        default=1.0,
        help="(optional) specify portion (where 1.0 is a std portion)",
    )
    parser_eat.add_argument(
        "--weight", type=float, default=None, help="(optional) specify weight"
    )
    parser_eat.set_defaults(func=eat)

    # measure subparser
    parser_eat = subparsers.add_parser(
        "measure", help="determines how much food will yield a given amount of calories"
    )
    parser_eat.add_argument("food", type=str, help="food that you would like to eat")
    parser_eat.add_argument(
        "--calories",
        type=float,
        default=100,
        required=False,
        help="(optional) specify desired number of calories (default: 100)",
    )
    parser_eat.set_defaults(func=measure)

    # cook subparser
    parser_cook = subparsers.add_parser(
        "cook", help="adds an ingredient to a recipe (starting a new recipe if needed)"
    )
    parser_cook.add_argument("recipe", type=str, help="name of recipe")
    parser_cook.add_argument(
        "ingredient", type=str, help="ingredient name (must exist in food library)"
    )
    parser_cook.add_argument(
        "--percent",
        type=float,
        default=1.0,
        help="(optional) specify portion of ingredient (where 1.0 is a std portion)",
    )
    parser_cook.add_argument(
        "--weight",
        type=float,
        default=None,
        help="(optional) specify weight of ingredient",
    )
    parser_cook.set_defaults(func=cook)

    # today subparser
    parser_today = subparsers.add_parser("today", help="get report of food eaten today")
    parser_today.set_defaults(func=today)

    # weight subparser
    parser_weight = subparsers.add_parser("weight", help="add today's weight")
    parser_weight.add_argument("weight", type=float, help="today's weight")
    parser_weight.set_defaults(func=weight)

    # stats subparser
    parser_stats = subparsers.add_parser(
        "stats", help="show statistics (currently limited to weight)"
    )
    parser_stats.add_argument(
        "--days",
        type=int,
        default=30,
        help="(optional) number of days of history to include in report",
    )
    parser_stats.add_argument(
        "--plotwidth", type=int, default=60, help="(optional) width of plot"
    )
    parser_stats.add_argument(
        "--interactive",
        action="store_true",
        help="(optional) whether plot should be interactive",
    )
    parser_stats.add_argument(
        "--num-days-to-average",
        type=int,
        default=7,
        help="(optional) number of days to average in moving average plot of weight",
    )
    parser_stats.set_defaults(func=stats)

    # food lookup subparser
    parser_food_lookup = subparsers.add_parser(
        "list_foods", help="get list of foods matching name or description"
    )
    parser_food_lookup.add_argument(
        "food", type=str, help="name or description of food"
    )
    parser_food_lookup.set_defaults(func=lookup_food)

    args = parser.parse_args()
    if "func" not in args:
        parser.print_help()
    else:
        # TODO: There's got to be a better way to map arguments received to the command functions
        if args.func == eat:
            eat(args.food, args.weight, args.percent)
            print()
            today(short=True)
        elif args.func == measure:
            measure(args.food, args.calories)
        elif args.func == today:
            today()
        elif args.func == weight:
            weight(args.weight)
            print()
            stats()
        elif args.func == stats:
            stats(args.days, args.plotwidth, args.interactive, args.num_days_to_average)
        elif args.func == lookup_food:
            lookup_food(args.food)
        elif args.func == cook:
            cook(args.recipe, args.ingredient, args.weight, args.percent)
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
