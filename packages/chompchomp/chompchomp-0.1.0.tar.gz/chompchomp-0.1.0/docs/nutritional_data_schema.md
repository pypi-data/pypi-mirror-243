# Nutritional Data Schema

The nutritional facts schema for `Chomp` follows the structure used by
Nutritional Facts labels in the United States.

Here is a sample food entry in the `Chomp` nutritional data database:

```yaml
---
- name: Peanut Butter Snickasnack
  brand: Foo Bars, Inc.
  nutritional_facts:
    calories: 200
    carbohydrates:
      dietary_fiber: 5g
      sugars:
        added_sugars: 1g
        total: 2g
        sugar_alcohol: 1g
      total: 7g
    cholesterol: 5mg
    fat:
      monounsaturated: 0g
      polyunsaturated: 0g
      saturated: 1.5g
      total: 4g
      trans: 0g
    micronutrients:
      biotin: 3mcg
      calcium: 250mg
      chloride: 2mcg
      choline: 500mg
      chromium: 3mcg
      copper: 0.1mg
      iodine: 20mcg
      iron: 6mcg
      folate: 100 mcg
      magnesium: 20mg
      manganese: 0.2mg
      molybdenum: 5mcg
      niacin: 1mcg
      pantothenic_acid: 1mg
      phosphorus: 200mg
      potassium: 200mg
      riboflavin: 2mcg
      selenium: 5mcg
      thiamin: 0mcg
      vitamin_a: 1mcg
      vitamin_b: 1mcg
      vitamin_c: 2mcg
      vitamin_d: 5mcg
      vitamin_e: 5mcg
      vitamin_k: 2mcg
      zinc: 1mg
    protein: 11g
    sodium: 400mg
    weight: 300g
```
