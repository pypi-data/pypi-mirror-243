from chomp.data_manager import (
    add_weight_diary_entry,
)


def weight(weight):
    print(f"You weigh {weight} pounds!")
    add_weight_diary_entry(weight)
