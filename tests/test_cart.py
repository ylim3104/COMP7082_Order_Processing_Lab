import sqlite3
from setup_db import initialize
from repository import StoreRepository
from cart import ShoppingCart

def test_cart_add_existing_product_stock_validation(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    cart = ShoppingCart('student', StoreRepository(str(db)))
    sku = 'LAP-01'
    assert cart.add_item(sku, 2) is True
    assert cart.add_item(sku, 5) is False
    laptop = next((x for x in cart.lines if x.sku == sku), None)
    assert laptop.quantity == 2
