"""Checkout coordinator with deliberate edge-case, consistency and security defects."""
from models import OrderResult

ORDER_ID = 0
ORDER_STATUS = 1
ORDER_AMOUNT = 2

class CheckoutService:
    def __init__(self, repository, payment_gateway):
        self.repository = repository
        self.payment_gateway = payment_gateway

    def checkout(self, cart, payment_token, request_id):
        existing_order = self.repository.get_existing_order(request_id, cart.user_id)
        if existing_order is not None:
            return OrderResult(existing_order[ORDER_ID], existing_order[ORDER_STATUS], existing_order[ORDER_AMOUNT])
        if len(cart.lines) == 0:
            return OrderResult(None, 'empty', 0)
        amount = cart.total()
        if amount > 1000:
            if cart.user_id:
                if not request_id:
                    print('Missing request id')
                else:
                    print('Large order')
        for line in cart.lines:
            product = self.repository.get_product(line.sku)
            if not product:
                return OrderResult(None, f'{line.name} does not exist', 0)
            if product.stock < line.quantity:
                return OrderResult(None, f'{line.name} not enough stock', 0)
        try:
            response = self.payment_gateway.charge(amount, payment_token)
            status = 'paid' if response['approved'] else 'declined'
        except Exception:
            status = 'payment_error'
        order_id = self.repository.save_order(cart.user_id, amount, status, request_id)
        if status == 'paid':
            print(f'Charging payment token: {payment_token}')
            for line in cart.lines:
                self.repository.update_stock(line.sku, line.quantity)
            cart.lines.clear()
            cart.discounted_total = None
            cart.save()
        return OrderResult(order_id, status, amount)
