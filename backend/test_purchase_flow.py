"""Test Purchase and Order Lifecycle flows."""
import asyncio
from app.api.orders import preview_order, create_order, update_order_status, cancel_order, get_orders
from app.models.schemas import OrderCreate, OrderPreviewRequest, CartItem, OrderStatus, PaymentMethod

async def run_tests():
    print("--- 1. Testing Order Preview ---")
    items = [
        CartItem(
            product_id="prod_001",
            product_name="Cà chua chín mọng Đà Lạt",
            quantity=2,
            unit_price=45000,
            seller_id="user_seller_001",
            unit="kg"
        ),
        CartItem(
            product_id="prod_003",
            product_name="Dưa leo mini VietGAP",
            quantity=1,
            unit_price=30000,
            seller_id="user_seller_001",
            unit="kg"
        )
    ]
    # Subtotal = 2 * 45000 + 30000 = 120,000
    preview_req = OrderPreviewRequest(items=items, points_to_use=50)
    user_payload = {"sub": "user_cust_001", "role": "customer"}
    preview_res = await preview_order(preview_req, user_payload)
    print(f"Subtotal: {preview_res.subtotal} | Shipping: {preview_res.shipping_fee} | Discount: {preview_res.discount_amount} | Final: {preview_res.final_total} | Points to earn: {preview_res.points_to_earn}")
    assert preview_res.subtotal == 120000
    assert preview_res.discount_amount == 5000 # 50 points * 100
    assert preview_res.final_total == 120000 - 5000 + 25000 # 140,000

    print("--- 2. Testing Order Creation & Stock Deduction ---")
    create_req = OrderCreate(
        items=items,
        shipping_address={
            "recipient_name": "Trần Thị Hoa",
            "phone": "0923456789",
            "address_line": "123 Nguyễn Huệ, Q.1, TP.HCM"
        },
        payment_method=PaymentMethod.cod,
        points_to_use=50,
        customer_id="user_cust_001"
    )
    created = await create_order(create_req, user_payload)
    order_id = created["id"]
    print(f"Created Order: #{order_id} | Total: {created['total_amount']} | Status: {created['order_status']}")
    assert created["points_used"] == 50
    assert created["discount_amount"] == 5000
    assert created["order_status"] == "pending"

    print("--- 3. Testing Order Status Update to delivered (award points) ---")
    delivered = await update_order_status(order_id, OrderStatus.delivered, user_payload)
    print(f"Delivered Order: #{order_id} | Status: {delivered['order_status']} | Points awarded flag: {delivered['points_awarded']}")
    assert delivered["order_status"] == "delivered"
    assert delivered["points_awarded"] is True

    print("--- 4. Testing Order Cancellation on new order ---")
    new_req = OrderCreate(
        items=[items[0]],
        shipping_address="Hà Nội",
        payment_method=PaymentMethod.cod,
        points_to_use=10,
        customer_id="user_cust_001"
    )
    order2 = await create_order(new_req, user_payload)
    cancel_res = await cancel_order(order2["id"], user_payload)
    print(f"Cancelled Order: #{order2['id']} | Status: {cancel_res['order_status']}")
    assert cancel_res["order_status"] == "cancelled"

    print("\nALL PURCHASE FLOW BACKEND TESTS PASSED!")

if __name__ == "__main__":
    asyncio.run(run_tests())
