"""Analytics - Track your finances and business metrics."""

from loguru import logger
from datetime import datetime


class FinanceTracker:
    """Track income, expenses, and financial metrics."""
    
    def __init__(self):
        """Initialize the finance tracker."""
        logger.info("💰 Finance Tracker initializing...")
        # Start with some sample data for demo
        self.transactions = [
            {'date': '2024-01-01', 'type': 'income', 'amount': 5000, 'category': 'Salary'},
            {'date': '2024-01-05', 'type': 'expense', 'amount': 200, 'category': 'Groceries'},
            {'date': '2024-01-10', 'type': 'expense', 'amount': 500, 'category': 'Rent'},
        ]
        logger.info("✅ Finance Tracker ready!")
    
    def get_balance(self) -> dict:
        """Calculate total income, expenses, and balance.
        
        Returns:
            Dictionary with financial summary
        """
        logger.info("💵 Calculating balance...")
        
        total_income = 0
        total_expenses = 0
        
        # Add up all income and expenses
        for transaction in self.transactions:
            if transaction['type'] == 'income':
                total_income += transaction['amount']
            else:
                total_expenses += transaction['amount']
        
        balance = total_income - total_expenses
        
        result = {
            'income': total_income,
            'expenses': total_expenses,
            'balance': balance,
            'transactions': len(self.transactions)
        }
        
        logger.info(f"✅ Balance calculated: {result}")
        return result
    
    def add_transaction(self, amount: float, category: str, trans_type: str) -> bool:
        """Add a new transaction.
        
        Args:
            amount: How much money
            category: What it's for (Salary, Groceries, etc)
            trans_type: 'income' or 'expense'
            
        Returns:
            True if successful
        """
        try:
            transaction = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'type': trans_type,
                'amount': amount,
                'category': category
            }
            self.transactions.append(transaction)
            logger.info(f"✅ Added transaction: {category} - ${amount}")
            return True
        except Exception as e:
            logger.error(f"❌ Error adding transaction: {e}")
            return False


if __name__ == "__main__":
    tracker = FinanceTracker()
    balance = tracker.get_balance()
    print(f"Balance: {balance}")
