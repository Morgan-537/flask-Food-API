"""
Flask REST API for the Inventory Management System.

Endpoints:
    GET    /inventory                          -> list all items
    GET    /inventory/<id>                      -> get a single item
    POST   /inventory                           -> add a new item
    PATCH  /inventory/<id>                      -> update an item
    DELETE /inventory/<id>                      -> delete an item
    GET    /inventory/lookup/barcode/<barcode>  -> query OpenFoodFacts by barcode
    GET    /inventory/lookup/name/<name>        -> query OpenFoodFacts by name
"""

from flask import Flask, jsonify, request

from inventory_data import inventory, get_next_id
from openfoodfacts import fetch_by_barcode, fetch_by_name

app = Flask(__name__)


def find_item(item_id):
    return next((item for item in inventory if item["id"] == item_id), None)


@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory), 200


@app.route("/inventory/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    return jsonify(item), 200


@app.route("/inventory", methods=["POST"])
def add_item():
    data = request.get_json(silent=True) or {}
    if not data.get("product_name"):
        return jsonify({"error": "product_name is required"}), 400

    new_item = {
        "id": get_next_id(),
        "product_name": data.get("product_name"),
        "brand": data.get("brand", "Unknown"),
        "ingredients": data.get("ingredients", "N/A"),
        "price": data.get("price", 0.0),
        "stock": data.get("stock", 0),
    }
    inventory.append(new_item)
    return jsonify(new_item), 201


@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    data = request.get_json(silent=True) or {}
    for field in ("product_name", "brand", "ingredients", "price", "stock"):
        if field in data:
            item[field] = data[field]
    return jsonify(item), 200


@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = find_item(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404
    inventory.remove(item)
    return jsonify({"message": f"Item {item_id} deleted"}), 200


@app.route("/inventory/lookup/barcode/<barcode>", methods=["GET"])
def lookup_barcode(barcode):
    result = fetch_by_barcode(barcode)
    if result is None:
        return jsonify({"error": "Product not found"}), 404
    if "error" in result:
        return jsonify(result), 502
    return jsonify(result), 200


@app.route("/inventory/lookup/name/<name>", methods=["GET"])
def lookup_name(name):
    results = fetch_by_name(name)
    if isinstance(results, dict) and "error" in results:
        return jsonify(results), 502
    if not results:
        return jsonify({"error": "No products found"}), 404
    return jsonify(results), 200


if __name__ == "__main__":
    app.run(debug=True)