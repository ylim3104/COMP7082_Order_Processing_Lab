# Order-processing system — student starter

This application intentionally contains defects. Your assignment has three parts only:

1. Identify and correct at least 8 meaningful defects. 
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

## DEFECTS
1) In cart.py class ShoppingCart add_item is not checking the total quantity against the stock of the product before adding an existing product into the cart. This can result in adding items that has not enough stocks in the cart. I have added the stock validation logic of the total quantity for an existing product.
2) In ShoppingCart class when applying the 'SAVE15' discount, it doesn't check if the total amount is less than 15 dollars. This will result in having a negative total amount when ordering. I have set the amount to 0 if it is less than 15.
3) In ShoppingCart class apply_discount() used total(), which made users to apply multiple discounts on products. The ShoppingCart is only keeping track of one discount_code so I assumed that only one discount can be applied. I have replaced the calculation of amount in apply_discount() to subtotal().
4) In ShoppingCart class I have added apply_discount() in the add_item() and remove_item() if the discount has been applied previously. Before, when the discount is already applied and the user modifies the cart then the discount will not be updated. 
5) In the checkout.py CheckoutService class, it should not clear cart lines, reset discounted total or update and save cart when the checkout status is declined or payment_error. Otherwise, inventory can be updated incorrectly and the customer needs to put items to the cart again and apply the discount again. I have explicitly made those to happen when items have been paid.
6) In the CheckoutService class, checkout should check if there is enough stock for each product before the payment. Otherwise, customers can purchase products that are out of stock. I have returned not enough stock when the quantity of the item exceeds the stock.
7) In the CheckoutService class, checkout() does not check if it is a duplicate checkout. If the user requests the checkout with the same request id then the database will have orders with the same request id and may result in duplicated payments. I have added a new function get_existing_order() in the repository. If the order exists, OrderResult is returned without checking out. 
8) In the ShoppingCart class, it does not check if the quantity is valid when adding or removing items. When a user adds an invalid quantity then it might crash the program or subtracts when trying to add and vice versa. I have checked if the quantity is a positive integer. Invalid quantities are rejected by returning False without modifying the cart. 

## TESTS
- Implemented 14 unit tests including the smoke test. 
- All 14 has passed.
- Run test: `python -m pytest -q`