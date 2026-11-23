import sqlite3
import pytest
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

def test_apply_save15(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    cart = ShoppingCart('user', StoreRepository(str(db)))
    cart.add_item('USB-01', 8)
    assert cart.apply_discount('SAVE15')
    expected_amount = 8 * 9.99 - 15
    assert cart.discounted_total == pytest.approx(expected_amount)

def test_apply_save15_to_less_than_15(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    cart = ShoppingCart('user', StoreRepository(str(db)))
    cart.add_item('USB-01', 1)
    assert cart.apply_discount('SAVE15')
    assert cart.discounted_total == 0

def test_only_apply_one_discount(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    cart = ShoppingCart('student', StoreRepository(str(db)))
    cart.add_item('MOU-01', 1)
    assert cart.apply_discount('WELCOME10')
    assert cart.discount_code == 'WELCOME10'
    expected_total_welcome = 29.95 * 0.9 
    assert cart.discounted_total == expected_total_welcome

    assert cart.apply_discount('STUDENT20')
    assert cart.discount_code == 'STUDENT20'
    expected_total_student = 29.95 * 0.8 
    assert cart.discounted_total == expected_total_student
