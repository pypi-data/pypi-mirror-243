# BlockPayments.py
BlockPayments python api wrapper


# Examples:
```python
"""This example will use sincronous requests."""
from BlockPayments import BlockPayments
blockpayments = BlockPaymets("my_api_key")


# Get a payment url
print(blockpayments.get_payment_url(
    user_id=123 # replace with your telegram user id
    amount=0.001 # replace with the amount of the currency you want to receive
    currency="BTC" # replace with the currency you want to receive (BTC, ETH, LTC or BSC)
))
```


```python
"""This example will use asincronous requests."""
from BlockPayments import AsyncBlockPayments
import asyncio
blockpayments = AsyncBlockPaymets("my_api_key")

async def main():
    # Get a payment url
    print(await blockpayments.get_payment_url(
        user_id=123 # replace with your telegram user id
        amount=0.001 # replace with the amount of the currency you want to receive
        currency="BTC" # replace with the currency you want to receive (BTC, ETH, LTC or BSC)
    ))

asyncio.run(main())
```
