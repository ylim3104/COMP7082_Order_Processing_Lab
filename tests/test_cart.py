import pytest
from setup_db import initialize
from repository import StoreRepository
from cart import ShoppingCart

# Testing defect #1
def test_cart_add_existing_product_stock_validation(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    cart = ShoppingCart('student', StoreRepository(str(db)))
    sku = 'LAP-01'
    assert cart.add_item(sku, 2) is True
    assert cart.add_item(sku, 5) is False
    laptop = next((x for x in cart.lines if x.sku == sku), None)
    assert laptop.quantity == 2

# Testing defect #2
def test_apply_save15(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    cart = ShoppingCart('user', StoreRepository(str(db)))
    cart.add_item('USB-01', 8)
    assert cart.apply_discount('SAVE15')
    expected_amount = 8 * 9.99 - 15
    assert cart.discounted_total == pytest.approx(expected_amount)

# Testing defect #2
def test_apply_save15_to_less_than_15(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    cart = ShoppingCart('user', StoreRepository(str(db)))
    cart.add_item('USB-01', 1)
    assert cart.apply_discount('SAVE15')
    assert cart.discounted_total == 0

# Testing defect #3
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

# Testing defect #4
def test_add_item_update_discount(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    cart = ShoppingCart('customer', StoreRepository(str(db)))
    cart.add_item('LAP-01', 1)
    cart.apply_discount('WELCOME10')
    expected_total = 999.99 * 0.9
    assert cart.discounted_total == pytest.approx(expected_total)
    cart.add_item('USB-01', 2)
    expected_total = expected_total + (9.99 * 2 * 0.9)
    assert cart.discounted_total == pytest.approx(expected_total)

# Testing defect #4
def test_remove_item_update_discount(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    cart = ShoppingCart('student', StoreRepository(str(db)))
    cart.add_item('USB-01', 3)
    cart.apply_discount('STUDENT20')
    expected_total = 9.99 * 3 * 0.8 
    assert cart.discounted_total == pytest.approx(expected_total)
    cart.remove_item('USB-01', 2)
    expected_total = expected_total - (9.99 * 2 * 0.8)
    assert cart.discounted_total == pytest.approx(expected_total)

# Testing defect #4
def test_add_item_update_save15_discount(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    cart = ShoppingCart('customer', StoreRepository(str(db)))
    cart.add_item('MOU-01', 3)
    cart.apply_discount('SAVE15')
    expected_total = 29.95 * 3 - 15 
    assert cart.discounted_total == pytest.approx(expected_total)
    cart.add_item('LAP-01', 4)
    expected_total = expected_total + (999.99 * 4)
    assert cart.discounted_total == pytest.approx(expected_total)

# Testing defect #8
def test_add_item_invalid_quantity(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    cart = ShoppingCart('customer', StoreRepository(str(db)))
    assert cart.add_item('USB-01', 0) == False

# Testing defect #8
def test_remove_item_invalid_quantity(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    cart = ShoppingCart('customer', StoreRepository(str(db)))
    assert cart.add_item('LAP-01', 2)
    assert cart.remove_item('LAP-01', "hello") == False
    assert cart.lines[0].quantity == 2