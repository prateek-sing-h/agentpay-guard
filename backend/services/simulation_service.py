from random import choice, randint


PRODUCTS = [
    {
        "product": "Wireless Headphones",
        "category": "Electronics",
        "price": 6000
    },
    {
        "product": "Smart Watch",
        "category": "Electronics",
        "price": 8000
    },
    {
        "product": "Running Shoes",
        "category": "Fashion",
        "price": 4500
    },
    {
        "product": "Backpack",
        "category": "Fashion",
        "price": 2500
    }
]


def generate_transaction(agent_id: str):

    product = choice(PRODUCTS)

    quantity = randint(1, 3)

    amount = product["price"] * quantity

    return {
        "agent_id": agent_id,
        "product": product["product"],
        "category": product["category"],
        "amount": amount,
        "quantity": quantity
    }


