import openfoodfacts


def lookup_food(food):
    search_results = openfoodfacts.products.search(food)
    products = search_results["products"]

    product_search_normalized = {}
    max_product_length = 1
    max_generic_length = 1
    for i, prod in enumerate(products):
        product_name = prod.get("product_name", "").strip()
        generic_name = prod.get("generic_name", "").strip()
        if len(product_name) > max_product_length:
            max_product_length = len(product_name)
        if len(generic_name) > max_generic_length:
            max_generic_length = len(generic_name)

        product_search_normalized[i] = {
            "generic_name": generic_name,
            "product_name": product_name,
        }

    print("Results")
    for index, prod in product_search_normalized.items():
        info_line = f"{index:3}    {prod['product_name']:{max_product_length}}   {prod['generic_name']:{max_generic_length}}"
        print(info_line)
