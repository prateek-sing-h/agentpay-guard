import re


def parse_intent(text: str):

    text_lower = text.lower()

    # Quantity
    quantity_match = re.search(
        r'"quantity"\s*:\s*(\d+)',
        text_lower
    )

    quantity = int(quantity_match.group(1)) if quantity_match else 1

    # Amount / budget
    amount_match = re.search(
        r'(?:₹|rs\.?|inr)?\s*(\d+(?:,\d+)*)',
        text_lower
    )

    amount = None

    if amount_match:
        amount = float(
            amount_match.group(1).replace(",", "")
        )

    # Product detection
    if "headphone" in text_lower:
        product = "Wireless Headphones"
        category = "Electronics"

    elif "smart watch" in text_lower or "smartwatch" in text_lower:
        product = "Smart Watch"
        category = "Electronics"

    elif "running shoes" in text_lower:
        product = "Running Shoes"
        category = "Fashion"

    elif "backpack" in text_lower:
        product = "Backpack"
        category = "Fashion"

    else:
        product = "Unknown"
        category = "Unknown"

    return {
        "product": product,
        "category": category,
        "amount": amount,
        "quantity": quantity
    }