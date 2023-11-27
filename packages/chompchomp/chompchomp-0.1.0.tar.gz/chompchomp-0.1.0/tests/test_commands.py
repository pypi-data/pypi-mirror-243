import pytest

from unittest.mock import patch, call

from chomp.commands.eat import eat
from chomp.food import Food


class TestCommands:
    @patch("chomp.commands.eat.add_food_diary_entry")
    @patch("chomp.commands.eat.get_food")
    @patch("chomp.commands.eat.print")
    def test_eat(self, mock_print, mock_get_food, mock_add_food_diary_entry):
        # given
        food_name = "foo_food"
        food_data = {
            "brand": "foo brand",
            "name": food_name,
            "nutritional_facts": {"calories": 142},
        }
        food = Food.from_dict(food_data)

        mock_get_food.return_value = food

        # when
        eat(food_name)

        # then
        expected_calls = [
            call(f"You ate {food_name}"),
            call(f"You ate {food_data['nutritional_facts']['calories']} calories!!"),
        ]
        assert mock_print.mock_calls == expected_calls

        mock_add_food_diary_entry.assert_called_with(food_data)
