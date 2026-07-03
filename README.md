# flask-Food-API# Inventory Management System

A Flask REST API for managing store inventory, with real-time product data
enrichment from the [OpenFoodFacts API](https://world.openfoodfacts.org/data),
plus a `rich`-based CLI for interacting with it.

## Features

- Full CRUD REST API (`GET`, `POST`, `PATCH`, `DELETE`) for inventory items
- Product lookup by barcode or name via the OpenFoodFacts API
- Interactive command-line interface built with [rich](https://github.com/Textualize/rich)
- Pytest test suite covering every endpoint, with external API calls mocked

## Installation and Setup

1. Clone the repository and move into it:
   ```bash
   git clone <your-repo-url>
   cd flask-Food-API
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate         # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the Flask API (leave this running in its own terminal):
   ```bash
   python app.py
   ```
   The API will be available at `http://127.0.0.1:5000`.

5. In a **separate terminal** (with the venv activated), run the CLI:
   ```bash
   python cli.py
   ```

## API Endpoint Details

| Method | Endpoint | Description | Body |
|---|---|---|---|
| GET | `/inventory` | List all inventory items | — |
| GET | `/inventory/<id>` | Get a single item by id | — |
| POST | `/inventory` | Add a new item | `{"product_name": str, "brand": str, "ingredients": str, "price": float, "stock": int}` (`product_name` required) |
| PATCH | `/inventory/<id>` | Update one or more fields of an item | any subset of the fields above |
| DELETE | `/inventory/<id>` | Remove an item | — |
| GET | `/inventory/lookup/barcode/<barcode>` | Fetch product details from OpenFoodFacts by barcode | — |
| GET | `/inventory/lookup/name/<name>` | Search OpenFoodFacts by product name (up to 5 results) | — |

All responses are JSON. Errors return an appropriate HTTP status code
(`400`, `404`, or `502` for upstream API failures) with an `"error"` message.

### Example requests

```bash
# List inventory
curl http://127.0.0.1:5000/inventory

# Add an item
curl -X POST http://127.0.0.1:5000/inventory \
  -H "Content-Type: application/json" \
  -d '{"product_name": "Oat Milk", "brand": "Oatly", "price": 4.29, "stock": 12}'

# Update stock level
curl -X PATCH http://127.0.0.1:5000/inventory/1 \
  -H "Content-Type: application/json" \
  -d '{"stock": 30}'

# Delete an item
curl -X DELETE http://127.0.0.1:5000/inventory/1

# Look up a product by barcode
curl http://127.0.0.1:5000/inventory/lookup/barcode/3017620422003
```

## Example CLI Usage

```
Inventory Management CLI
1. View all inventory
2. View item details
3. Add new item
4. Update item
5. Delete item
6. Find item on API
7. Exit
Choose an option: 6
Search by [barcode/name] (name): name
Enter name: almond milk
[0] Organic Almond Milk — Silk
[1] Almond Breeze — Blue Diamond
Add one to inventory? Enter index or 'n' to skip: 0
Set price: 3.99
Set stock: 20
Added to inventory!
```

## Running Tests

```bash
pytest tests/ -v
```

The test suite uses Flask's test client for the API routes and
`unittest.mock` to simulate OpenFoodFacts responses, so tests run fully
offline and don't depend on the external API being reachable.

## Project Structure

```
flask-Food-API/
├── app.py               # Flask app and route definitions
├── inventory_data.py    # In-memory mock database
├── openfoodfacts.py     # OpenFoodFacts API integration
├── cli.py                # Rich-based CLI frontend
├── requirements.txt
├── tests/
│   └── test_app.py
└── README.md
```

## Notes

- Data is stored in-memory (a Python list) and resets whenever the Flask
  server restarts — this simulates a database for the purposes of this lab.
- The OpenFoodFacts API requires a descriptive `User-Agent` header, which is
  set in `openfoodfacts.py`.
