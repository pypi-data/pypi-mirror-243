class MissingNutritionalData(Exception):
    pass


class Food:
    def __init__(self, name, brand, nutritional_facts):
        self.name = name
        self.brand = brand
        self.nutritional_facts = nutritional_facts

    @classmethod
    def from_dict(cls, d):
        if "name" not in d:
            raise MissingNutritionalData(f"'name' not provided for food entry: {d}")
        if "brand" not in d:
            raise MissingNutritionalData(f"'brand' not provided for food entry: {d}")
        if "nutritional_facts" not in d:
            raise MissingNutritionalData(
                f"'nutritional_facts' section missing for food entry: {d}"
            )

        name = d["name"]
        brand = d["brand"]
        nutritional_facts = d["nutritional_facts"]

        return Food(name, brand, nutritional_facts)

    def to_dict(self):
        return {
            "name": self.name,
            "brand": self.brand,
            "nutritional_facts": self.nutritional_facts,
        }

    def get_nutritional_fact(self, fact):
        """Traverses nutritional data tree to find food fact.

        `food.get_nutritional_fact('foo.bar')` will attempt to
        locate a node called `foo` which points to a sub-tree
        containing `bar` and return the value associated with `bar`.

        Given the following tree:
        ```
        'foo':
          'biz': 1
          'bar': 2
        ```
        `food.get_nutritional_fact('foo.bar')` would return `2`.
        """

        def _get_nutritional_facts(fact, tree):
            subfact = ""
            if "." in fact:
                fact, subfact = fact.split(".", maxsplit=1)
            for key, value in tree.items():
                if key != fact:
                    continue
                if subfact != "":
                    if type(value) != dict:
                        return None
                    return _get_nutritional_facts(subfact, value)
                if type(value) is dict:
                    return None
                return value

        return _get_nutritional_facts(fact, self.nutritional_facts)

    def __mul__(self, scale):
        """Scale nutritional data"""

        def _scale_nutritional_facts(facts, scale):
            scaled_facts = dict()

            for key, value in facts.items():
                if type(value) is dict:
                    scaled_facts[key] = _scale_nutritional_facts(value, scale)
                else:
                    scaled_facts[key] = value * scale
            return scaled_facts

        scaled_facts = _scale_nutritional_facts(self.nutritional_facts, scale)
        return Food(self.name, self.brand, scaled_facts)

    def __rmul__(self, *args, **kwargs):
        return self.__mul__(*args, **kwargs)

    def __add__(self, other):
        if type(other) != Food:
            raise Exception("Cannot add Food item with non-Food item")

        def _merge_nutritional_facts(first_fact_set, second_fact_set):
            # copy all entries from first_fact_set except nested dictionaries
            combined_facts = {
                k: v for (k, v) in first_fact_set.items() if type(k) is not dict
            }

            # merge in entries from second_fact_set, ignoring nested dictionaries
            for key, value in second_fact_set.items():
                if type(value) is dict:
                    continue

                if key not in combined_facts:
                    combined_facts[key] = value
                else:
                    combined_facts[key] += value

            # handle nested dictionaries
            for key, value in first_fact_set.items():
                if type(value) is not dict:
                    continue
                # determine if merge is required
                if key in second_fact_set:
                    other_value = second_fact_set[key]
                    combined_facts[key] = _merge_nutritional_facts(value, other_value)
                else:
                    combined_facts[key] = value

            for key, value in second_fact_set.items():
                if type(value) is not dict:
                    continue
                # at this point, only need to handle cases where
                # key is not in first_fact_set
                if key not in first_fact_set:
                    combined_facts[key] = value

            return combined_facts

        merged_nutritional_facts = _merge_nutritional_facts(
            self.nutritional_facts, other.nutritional_facts
        )
        return Food("Combined Foods", "", merged_nutritional_facts)
