import re


def extract_quantity(text, max_price=None):
    text = text.lower()

    number_words = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10
    }

    # 1. First check for quantity written in words (e.g., "three pizzas", "two burgers")
    for word, number in number_words.items():
        if re.search(rf"\b{word}\b", text):
            return number

    # 2. Check for numeric digits tied to items or distinct from price
    # Exclude price phrases like "under 1000", "₹500", "below 300", "budget 400"
    clean_text = re.sub(
        r"(?:under|below|less than|within|budget(?:\s*(?:is|of))?)\s*₹?\s*\d+",
        " ",
        text
    )
    clean_text = re.sub(r"₹\s*\d+", " ", clean_text)

    # If a max_price was detected, avoid picking that exact number as quantity
    numeric_matches = re.findall(r"\b(\d+)\b", clean_text)
    for num_str in numeric_matches:
        num = int(num_str)
        if max_price is not None and num == max_price:
            continue
        return num

    return None
def extract_max_price(text):
    text = text.lower()

    patterns = [
        # Under ₹500, below 300, less than 400
        r"(?:under|below|less than|within)\s*₹?\s*(\d+)",

        # ₹500 or ₹500 maximum
        r"₹\s*(\d+)\s*(?:or less|maximum|max)?",

        # Budget 500, budget is 400, or budget of ₹500
        r"budget\s*(?:is|of)?\s*₹?\s*(\d+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return int(match.group(1))

    return None
def extract_food(text: str, menu_items: list[str]) -> str | None:
    text = text.lower()

    # Match longer menu items before shorter ones.
    # This helps distinguish "paneer pizza" from "pizza".
    sorted_items = sorted(
        menu_items,
        key=len,
        reverse=True
    )

    for item in sorted_items:
        item_lower = item.lower()

        pattern = (
            r"(?<!\w)"
            + re.escape(item_lower)
            + r"(?:e?s)?(?!\w)"
        )

        if re.search(pattern, text):
            return item

    return None
def extract_entities(text, menu_items):
    max_price = extract_max_price(text)
    entities = {
        "food": extract_food(text, menu_items),
        "quantity": extract_quantity(text, max_price=max_price),
        "max_price": max_price
    }

    # Remove entities that were not detected.
    return {
        key: value
        for key, value in entities.items()
        if value is not None
    }



if __name__ == "__main__":

    test_sentences = [
        "I want 2 pizzas",
        "Give me three burgers",
        "I want one paneer pizza",
        "Show me the menu"
    ]

    for sentence in test_sentences:
        quantity = extract_quantity(sentence)

        print(f"Message: {sentence}")
        print(f"Quantity: {quantity}")
        print()
    print("\nPRICE EXTRACTION TESTS")

    price_test_sentences = [
        "Show me pizzas under 500",
        "Find dishes below ₹300",
        "My budget is 300",
        "What can I get for ₹250?",
        "Show me the menu"
    ]

    for sentence in price_test_sentences:
        price = extract_max_price(sentence)

        print(f"Message: {sentence}")
        print(f"Maximum price: {price}")
        print()
    menu_items = [
        "paneer pizza",
        "margherita pizza",
        "chicken burger",
        "veg burger",
        "paneer tikka",
        "chicken biryani"
    ]

    food_test_sentences = [
        "I want two paneer pizzas",
        "Can I get a margherita pizza?",
        "Give me a chicken burger",
        "I want some food"
    ]

    print("\nFOOD EXTRACTION TESTS")

    for sentence in food_test_sentences:
        food = extract_food(
            sentence,
            menu_items
        )

        print(f"Message: {sentence}")
        print(f"Food: {food}")
        print()

    print("\nCOMBINED ENTITY EXTRACTION")

    message = "I want 2 margherita pizzas under ₹500"

    entities = extract_entities(
        message,
        menu_items
    )

    print("Message:", message)
    print("Entities:", entities)