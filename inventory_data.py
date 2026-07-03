"""
Mock in-memory 'database' for the Inventory Management System.
Each item is a dict with a unique integer id.
"""

inventory = [
    {
        "id": 1,
        "product_name": "Organic Almond Milk",
        "brand": "Silk",
        "ingredients": "Filtered water, almonds, cane sugar",
        "price": 3.99,
        "stock": 20,
    },
    {
        "id": 2,
        "product_name": "Whole Wheat Bread",
        "brand": "Dave's Killer Bread",
        "ingredients": "Whole wheat flour, water, honey, yeast",
        "price": 4.49,
        "stock": 15,
    },
]


def get_next_id():
    """Return the next available unique id for a new inventory item."""
    if not inventory:
        return 1
    return max(item["id"] for item in inventory) + 1