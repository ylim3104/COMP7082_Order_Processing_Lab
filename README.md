# Order-processing system — student starter

This application intentionally contains defects. Your assignment has three parts only:

1. Identify and correct at least 8 meaningful defects.
    1) In cart.py class ShoppingCart add_item is not checking the total quantity against the stock of the product before adding an existing product into the cart. This can result in adding items that has not enough stocks in the cart. I have added the stock validation logic of the total quantity for an existing product.
    2) In ShoppingCart class when applying the 'SAVE15' discount, it doesn't check if the total amount is less than 15 dollars. This will result in having a negative total amount when ordering. I have set the amount to 0 if it is less than 15.
2. Write at least 12 automated unit tests with `pytest`.
3. Add `.github/workflows/tests.yml` to run tests on pushes and pull requests.

## Application files

- `models.py`: domain objects
- `cart.py`: shopping cart and discounts
- `repository.py`: SQLite products, saved carts, inventory and orders
- `checkout.py`: checkout workflow
- `payments.py`: simulated payment gateway
- `setup_db.py` and `demo.py`: demo database and execution
- `tests/test_smoke.py`: minimal smoke tests (not a solution)

## Running locally

```bash
python -m pip install -r requirements.txt
python -m pytest -q
python setup_db.py
python demo.py
```

Use temporary databases and fake payment tokens for unit tests. No real payment credentials are required.
