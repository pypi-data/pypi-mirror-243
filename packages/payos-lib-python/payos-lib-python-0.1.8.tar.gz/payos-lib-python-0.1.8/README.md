The payOS Node library provides convenient access to the payOS API from applications written in server-side Django.

## Documentation
See the [payOS API docs](https://payos.vn/docs/api/) for more infomation.

## Installation
Install the package with:
```bash
pip install payos-lib-python
```

## Usage
### Initialize
You need to initialize the PayOS object with the Client ID, Api Key and Checksum Key of the payment channel you created. 

* CommonPython
```python
from payos_lib_python import PayOS
import os

payOS = PayOS(client_id= os.environ.get('PAYOS_CLIENT_ID'), api_key=os.environ.get('PAYOS_API_KEY'), checksum_key=os.environ.get('PAYOS_CHECKSUM_KEY'))
```


### Methods included in the PayOS object

* **createPaymentLink**

Create a payment link for the order data

Syntax:
```python
payOS.createPaymentLink(requestData)
```
Parameter data type: 
```python
from payos_lib_python import PaymentData, ItemData

#PaymentData Type
{
  "orderCode": int; #required
  "amount": int; #required
  "description": str; #required
  "cancelUrl": str; #required
  "returnUrl": str; #required
  "signature": str = None;
  "items": list(ItemData);
  "buyerName": str = None;
  "buyerEmail": str = None;
  "buyerPhone": str = None;
  "buyerAddress": str = None;
  "expiredAt": int = None;
}
#ItemData Type

{
  "name": str;
  "quantity": int;
  "price": int;
}

```
Return data type:
```python
{
  "bin": str;
  "accountint": str;
  "accountName": str;
  "amount": int;
  "description": str;
  "orderCode": int;
  "paymentLinkId": str;
  "status": str;
  "checkoutUrl": str;
  "qrCode": str
}
```

Example:
```python
requestData = {
    "orderCode": 234234,
    "amount": 1000,
    "description": "Thanh toan don hang",
    "items": [
      {
        "name": "Mì tôm hảo hảo ly",
        "quantity": 1,
        "price": 1000,
      }
    ],
    "cancelUrl": "https://your-domain.com",
    "returnUrl": "https://your-domain.com",
}
paymentLinkData = payOS.createPaymentLink(requestData)
```

* **getPaymentLinkInfomation**

Get payment information of an order that has created a payment link.

Syntax:
```python
payOS.getPaymentLinkInfomation(id)
```

Parameters:
* `id`: Store order code (`orderCode`) or payOS payment link id (`paymentLinkId`). Type of `id` is str or int.


Return data type:
```py
{
  "id": str;
  "orderCode": int;
  "amount": int;
  "amountPaid": int;
  "amountRemaining": int;
  "status": str;
  "createdAt": str;
  "transactions": [dict]; #Transactions Type
  "cancellationReason": str | None;
  "canceledAt": str | None;
}
```

Transaction type:
```python
{
  "reference": str;
  "amount": int;
  "accountint": str;
  "description": str;
  "transactionDateTime": str;
  "virtualAccountName": str | None;
  "virtualAccountint": str | None;
  "counterAccountBankId": str | None;
  "counterAccountBankName": str | None;
  "counterAccountName": str | None;
  "counterAccountint": str | None
}
```
Example:
```py
paymentLinkInfo = payOS.getPaymentLinkInfomation(1234)
```

* **cancelPaymentLink**

Cancel the payment link of the order.

Syntax:
```python
payOS.cancelPaymentLink(orderCode, cancellationReason); 
```

Parameters:
* `id`: Store order code (`orderCode`) or payOS payment link id (`paymentLinkId`). Type of `id` is str or int.

* `cancellationReason`: Reason for canceling payment link (optional).

Return data type:
```py
{
  'id': str;
  'orderCode': int;
  'amount': int;
  'amountPaid': int;
  'amountRemaining': int;
  'status': str;
  'createdAt': str;
  'transactions': TransactionType[];
  'cancellationReason': str | None;
  'canceledAt': str | None;
}
```
Example:

```py
orderCode = 123
cancellationReason = "reason"

cancelledPaymentLinkInfo = payOS.cancelPaymentLink(orderCode, cancellationReason); 

// If you want to cancel the payment link without reason:
cancelledPaymentLinkInfo = payOS.cancelPaymentLink(orderCode); 
```


* **confirmWebhook**

Validate the Webhook URL of a payment channel and add or update the Webhook URL for that Payment Channel if successful.

Syntax:

```py
payOS.confirmWebhook("https://your-webhook-url/")
```

* **verifyPaymentWebhookData**

Verify data received via webhook after payment.

Syntax:

```py
webhookBody = req.data
paymentData = payOS.verifyPaymentWebhookData(webhookBody)
```

Return data type:
```py
{
  'orderCode': int;
  'amount': int;
  'description': str;
  'accountint': str;
  'reference': str;
  'transactionDateTime': str;
  'paymentLinkId': str;
  'code': str;
  'desc': str;
  'counterAccountBankId': str | None;
  'counterAccountBankName': str | None;
  'counterAccountName': str | None;
  'counterAccountint': str | None;
  'virtualAccountName': str | None;
  'virtualAccountint': str | None;
}
```

