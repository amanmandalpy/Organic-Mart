# Razorpay Payment Gateway Guide

This guide explains how to add Razorpay payments to OrganicMart before accepting
real online payments.

OrganicMart already has checkout pages, cart totals, environment variables, and
order-success flow. The next step is to add a real `Order` model and connect it
to Razorpay order creation and webhook confirmation.

## 1. Create Razorpay Account

1. Go to `https://razorpay.com/`.
2. Create a merchant account.
3. Complete KYC.
4. Open `Dashboard > Account & Settings > API Keys`.
5. Generate test keys first.

You will receive:

- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET`

For webhooks, create:

- `RAZORPAY_WEBHOOK_SECRET`

## 2. Add Environment Variables

Update `.env`:

```env
RAZORPAY_KEY_ID=rzp_test_xxxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=your-test-secret
RAZORPAY_WEBHOOK_SECRET=your-webhook-secret
```

Never commit real Razorpay secrets to Git.

## 3. Install Razorpay Python SDK

Add this to `requirements.in`:

```text
razorpay>=1.4,<2
```

Then install:

```powershell
.\.venv\Scripts\python.exe -m pip install razorpay
```

For a locked production requirements file, regenerate `requirements.txt` using
your dependency workflow.

## 4. Recommended Order Model

Create an `orders` app with models like:

```python
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        PAID = "PAID", "Paid"
        FAILED = "FAILED", "Failed"
        CANCELLED = "CANCELLED", "Cancelled"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_signature = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
```

Also create `OrderItem` for product, price, quantity, and line total.

## 5. Create Razorpay Order From Django

Example service:

```python
import razorpay
from django.conf import settings


def create_razorpay_order(order):
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )
    amount_paise = int(order.total * 100)
    return client.order.create(
        {
            "amount": amount_paise,
            "currency": "INR",
            "receipt": str(order.pk),
            "payment_capture": 1,
        }
    )
```

Store the returned `id` in `order.razorpay_order_id`.

## 6. Add Razorpay Checkout Script

On the checkout page:

```html
<script src="https://checkout.razorpay.com/v1/checkout.js"></script>
<script>
const options = {
    key: "{{ razorpay_key_id }}",
    amount: "{{ amount_paise }}",
    currency: "INR",
    name: "OrganicMart",
    description: "Organic products order",
    order_id: "{{ razorpay_order_id }}",
    callback_url: "{{ callback_url }}",
    prefill: {
        name: "{{ request.user.get_full_name }}",
        email: "{{ request.user.email }}"
    },
    theme: {
        color: "#214e34"
    }
};

const paymentObject = new Razorpay(options);
paymentObject.open();
</script>
```

## 7. Verify Payment Signature

After Razorpay redirects/calls back, verify the signature server-side:

```python
client.utility.verify_payment_signature(
    {
        "razorpay_order_id": razorpay_order_id,
        "razorpay_payment_id": razorpay_payment_id,
        "razorpay_signature": razorpay_signature,
    }
)
```

Only mark the order as `PAID` after signature verification succeeds.

## 8. Add Webhook Verification

Create webhook endpoint:

```text
https://yourdomain.com/payments/razorpay/webhook/
```

Verify webhook signature:

```python
import hmac
import hashlib


def verify_webhook_signature(payload, signature, secret):
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(expected, signature)
```

Handle important events:

- `payment.captured`
- `payment.failed`
- `order.paid`
- `refund.processed`

## 9. Security Rules

- Never trust payment status from frontend JavaScript.
- Always verify signature on backend.
- Store Razorpay IDs on the order.
- Make webhook processing idempotent.
- Do not expose `RAZORPAY_KEY_SECRET` in templates or JavaScript.
- Use HTTPS before going live.
- Keep test mode and live mode keys separate.

## 10. Test Cards And UPI

Use Razorpay test mode first. Test:

- Successful card payment
- Failed card payment
- UPI success
- UPI failure
- User closes payment popup
- Duplicate webhook event
- Refresh after payment

## 11. Go-Live Checklist

Before live payments:

1. Complete Razorpay KYC.
2. Switch from test keys to live keys.
3. Add live webhook URL.
4. Verify HTTPS certificate.
5. Test one small real payment.
6. Confirm order status changes to paid.
7. Confirm email notification works.
8. Confirm failed payment does not clear cart.
9. Confirm admin can see payment IDs.
10. Confirm refund process is documented.
