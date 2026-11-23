import pytest
from setup_db import initialize
from repository import StoreRepository
from cart import ShoppingCart
from payments import FakePaymentGateway
from checkout import CheckoutService

# Testing defect #5
def test_declined_checkout(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    repo = StoreRepository(str(db))
    uid = 'demo-user'
    cart = ShoppingCart(uid, repo)
    sku = 'MOU-01'
    quantity = 2
    cart.add_item(sku, quantity)
    cart.apply_discount('WELCOME10')
    cart.save()
    result = CheckoutService(repo, FakePaymentGateway(should_approve=False)).checkout(cart, 'TEST_TOKEN', 'demo-request-1')
    assert result.status == 'declined'
    assert len(cart.lines) == 1
    assert cart.lines[0].quantity == quantity
    expected_total = 29.95 * quantity * 0.9
    assert cart.discounted_total == pytest.approx(expected_total)
    saved_cart = cart.repository.get_saved_cart(uid)
    assert saved_cart == [(sku, quantity)]
    assert repo.get_product(sku).stock == 20

# Testing defect #7
def test_duplicate_checkout(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    repo = StoreRepository(str(db))
    uid = 'demo-user'
    cart = ShoppingCart(uid, repo)
    sku = 'MOU-01'
    quantity = 2
    cart.add_item(sku, quantity)
    cart.apply_discount('WELCOME10')
    cart.save()
    gateway = FakePaymentGateway()
    service = CheckoutService(repo, gateway)
    result = service.checkout(cart, 'TEST_TOKEN', 'demo-request-1')
    dup_result = service.checkout(cart, 'TEST_TOKEN', 'demo-request-1')
    assert result.order_id == dup_result.order_id
    assert result.status == dup_result.status
    assert result.total == dup_result.total
    assert len(gateway.calls) == 1
    assert repo.get_product(sku).stock == 18

# Testing defect #6
def test_checkout_insufficient_stock(tmp_path):
    db = tmp_path / 'test.db'
    initialize(str(db))
    repo = StoreRepository(str(db))
    uid = 'demo-user'
    cart = ShoppingCart(uid, repo)
    sku = 'LAP-01'
    cart.add_item(sku, 2)
    repo.update_stock(sku, 5)
    assert repo.get_product(sku).stock == 0
    gateway = FakePaymentGateway()
    result = CheckoutService(repo, gateway).checkout(cart, 'TEST_TOKEN', 'demo-request-1')
    assert result.status == "Laptop not enough stock"
    assert len(gateway.calls) == 0


