
def get_share_price(symbol: str) -> float:
    fixed_prices = {
        'AAPL': 170.00,
        'TSLA': 250.00,
        'GOOGL': 140.00
    }
    price = fixed_prices.get(symbol.upper())
    if price is None:
        raise ValueError(f'Share price for symbol '{symbol}' not found.')
    return price

class Account:
    def __init__(self, initial_deposit: float = 0.0):
        if initial_deposit < 0:
            raise ValueError("Initial deposit cannot be negative.")
        self._balance = initial_deposit
        self._holdings = {}
        self._transactions = []
    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if self._balance < amount:
            raise ValueError("Insufficient funds")
        self._balance -= amount
    def buy_shares(self, symbol: str, quantity: int) -> None:
        price_per_share = get_share_price(symbol)
        total_cost = price_per_share * quantity
        if self._balance < total_cost:
            raise ValueError("Insufficient funds")
        self._balance -= total_cost
        self._holdings[symbol] = self._holdings.get(symbol, 0) + quantity
    def sell_shares(self, symbol: str, quantity: int) -> None:
        price_per_share = get_share_price(symbol)
        total_proceeds = price_per_share * quantity
        if symbol not in self._holdings or self._holdings[symbol] < quantity:
            raise ValueError("Insufficient shares")
        self._balance += total_proceeds
        self._holdings[symbol] -= quantity
    def get_balance(self) -> float:
        return self._balance
    def get_holdings(self) -> dict[str, int]:
        return self._holdings.copy()
    def get_portfolio_value(self) -> float:
        portfolio_value = self._balance
        for symbol, quantity in self._holdings.items():
            try:
                price = get_share_price(symbol)
                portfolio_value += price * quantity
            except ValueError:
                pass
        return portfolio_value
    def get_profit_loss(self) -> float:
        return 0.0
    def get_transactions(self) -> list[dict]:
        return self._transactions[:]
