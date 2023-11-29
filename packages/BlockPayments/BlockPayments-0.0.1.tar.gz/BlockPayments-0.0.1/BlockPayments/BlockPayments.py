import requests, aiohttp

class BlockPayments:
    """The BlockPayments class.
    This class is used to interact with the BlockPayments API.
    Attributes:
        api_key (str): Your BlockPayments API key.
        url (str): The BlockPayments API URL.
    """
    def __init__(self, api_key: str):
        """Initialize the BlockPayments class.
        Args:
            api_key (str): Your BlockPayments API key.
        """
        self.api_key = api_key
        self.url = f"https://www.blockpayments.top/api/{self.api_key}/"

    def get_payment_url(self, user_id: int, currency: str, amount: float) -> str:
        """Get a URL to get paid.
        Args:
            user_id (str): Your telegram user ID.
            currency (str): The currency to get paid with. (BTC, ETH, LTC or BSC)
            amount (float): The amount to pay.
        Returns:
            str: The payment URL.
        """
        r = requests.get(self.url + f"get_payment_url/{user_id}/{currency}/{amount}")
        return r.json()['payment_url']
    
    def get_balance(self, currency: str) -> float:
        """Get the balance of a currency.
        Args:
            currency (str): The currency to get the balance of. (BTC, ETH, LTC or BSC)
        Returns:
            float: The balance of the currency.
        """
        r = requests.get(self.url + f"get_balance/{currency}")
        return float(r.json()['balance'])
    
    def send(self, to_user_id: int, currency: str, amount: float) -> list:
        """Send coins to a user.
        Args:
            to_user_id (int): The user ID to send the coins to.
            currency (str): The currency to send. (BTC, ETH, LTC or BSC)
            amount (float): The amount to send.
        Returns:
            list: A list containing the success and error message.
        """
        r = requests.post(self.url + f"send_coins/{to_user_id}/{currency}/{amount}")
        r = r.json()
        try:
            tmp = r['success']
            return True, r['success']
        except:
            return False, r['error']
        

    def withdraw(self, currency: str, amount: float, address: str) -> list:
        """Withdraw coins to an address.
        Args:
            currency (str): The currency to withdraw. (BTC, ETH, LTC or BSC)
            amount (float): The amount to withdraw.
            address (str): The address to withdraw to.
        Returns:
            list: A list containing the success and error message.
        """
        r = requests.post(self.url + f"withdraw/{currency}/{amount}/{address}")
        r = r.json()
        try:
            tmp = r['success']
            return True, r['success']
        except:
            return False, r['error']



class AsyncBlockPayments:
    """The AsyncBlockPayments class.
    This class is used to interact with the BlockPayments API asynchronously.
    Attributes:
        api_key (str): Your BlockPayments API key.
        url (str): The BlockPayments API URL.
    """
    def __init__(self, api_key: str):
        """Initialize the AsyncBlockPayments class.
        Args:
            api_key (str): Your BlockPayments API key.
        """
        self.api_key = api_key
        self.url = f"https://www.blockpayments.top/api/{self.api_key}/"

    async def get_payment_url(self, user_id: int, currency: str, amount: float) -> str:
        """Get a URL to get paid.
        Args:
            user_id (str): Your telegram user ID.
            currency (str): The currency to get paid with. (BTC, ETH, LTC or BSC)
            amount (float): The amount to pay.
        Returns:
            str: The payment URL.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + f"get_payment_url/{user_id}/{currency}/{amount}") as r:
                return (await r.json())['payment_url']
    
    async def get_balance(self, currency: str) -> float:
        """Get the balance of a currency.
        Args:
            currency (str): The currency to get the balance of. (BTC, ETH, LTC or BSC)
        Returns:
            float: The balance of the currency.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + f"get_balance/{currency}") as r:
                return float((await r.json())['balance'])
    
    async def send(self, to_user_id: int, currency: str, amount: float) -> list:
        """Send coins to a user.
        Args:
            to_user_id (int): The user ID to send the coins to.
            currency (str): The currency to send. (BTC, ETH, LTC or BSC)
            amount (float): The amount to send.
        Returns:
            list: A list containing the success and error message.
        """
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url + f"send_coins/{to_user_id}/{currency}/{amount}") as r:
                r = await r.json()
                try:
                    tmp = r['success']
                    return True, r['success']
                except:
                    return False, r['error']