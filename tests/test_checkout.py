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

