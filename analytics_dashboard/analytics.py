"""Analytics Dashboard Module - Business analytics and financial tracking."""

import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from loguru import logger
import yaml

try:
    import pandas as pd
except ImportError:
    logger.warning("pandas not installed. Install with: pip install pandas")

try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    logger.warning("plotly not installed. Install with: pip install plotly")


class Analytics:
    """Business analytics and financial tracking."""
    
    def __init__(self, config_path: str = "config.yaml"):
        """Initialize Analytics.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)
        self.db_path = self.config['analytics']['database_path']
        self._init_database()
        logger.info("Analytics initialized")
    
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _init_database(self) -> None:
        """Initialize SQLite database."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                date TEXT,
                category TEXT,
                amount REAL,
                type TEXT,
                description TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY,
                category TEXT,
                limit REAL,
                month TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metrics (
                id INTEGER PRIMARY KEY,
                date TEXT,
                metric_name TEXT,
                value REAL
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"Database initialized at {self.db_path}")
    
    def add_transaction(self, date: str, category: str, amount: float, 
                       transaction_type: str, description: str = "") -> bool:
        """Add income or expense transaction.
        
        Args:
            date: Transaction date (YYYY-MM-DD)
            category: Transaction category
            amount: Amount in currency
            transaction_type: 'income' or 'expense'
            description: Optional description
            
        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO transactions (date, category, amount, type, description)
                VALUES (?, ?, ?, ?, ?)
            ''', (date, category, amount, transaction_type, description))
            conn.commit()
            conn.close()
            logger.info(f"Added {transaction_type}: ${amount} - {category}")
            return True
        except Exception as e:
            logger.error(f"Error adding transaction: {e}")
            return False
    
    def get_balance(self) -> Dict[str, float]:
        """Get current income vs expenses balance.
        
        Returns:
            Dictionary with total_income, total_expense, net_balance
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT SUM(amount) FROM transactions WHERE type='income'"
            )
            total_income = cursor.fetchone()[0] or 0
            
            cursor.execute(
                "SELECT SUM(amount) FROM transactions WHERE type='expense'"
            )
            total_expense = cursor.fetchone()[0] or 0
            
            conn.close()
            
            return {
                'total_income': total_income,
                'total_expense': total_expense,
                'net_balance': total_income - total_expense
            }
        except Exception as e:
            logger.error(f"Error calculating balance: {e}")
            return {}
    
    def get_monthly_summary(self, month: str) -> Dict[str, any]:
        """Get summary for a specific month.
        
        Args:
            month: Month in format YYYY-MM
            
        Returns:
            Dictionary with monthly summary
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    SUM(CASE WHEN type='income' THEN amount ELSE 0 END) as income,
                    SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) as expense
                FROM transactions
                WHERE date LIKE ?
            ''', (f"{month}%",))
            
            result = cursor.fetchone()
            income = result[0] or 0
            expense = result[1] or 0
            
            conn.close()
            
            return {
                'month': month,
                'income': income,
                'expense': expense,
                'net': income - expense
            }
        except Exception as e:
            logger.error(f"Error getting monthly summary: {e}")
            return {}
    
    def get_category_breakdown(self) -> Dict[str, float]:
        """Get breakdown of expenses by category.
        
        Returns:
            Dictionary with categories and their totals
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT category, SUM(amount) as total
                FROM transactions
                WHERE type='expense'
                GROUP BY category
                ORDER BY total DESC
            ''')
            
            results = cursor.fetchall()
            conn.close()
            
            return {category: amount for category, amount in results}
        except Exception as e:
            logger.error(f"Error getting category breakdown: {e}")
            return {}
    
    def create_expense_chart(self, output_path: str = "./charts/expenses.html") -> bool:
        """Create expense chart.
        
        Args:
            output_path: Path to save chart
            
        Returns:
            True if successful
        """
        try:
            breakdown = self.get_category_breakdown()
            fig = px.pie(
                values=list(breakdown.values()),
                names=list(breakdown.keys()),
                title="Expense Breakdown by Category"
            )
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            fig.write_html(output_path)
            logger.info(f"Expense chart saved to {output_path}")
            return True
        except Exception as e:
            logger.error(f"Error creating chart: {e}")
            return False
    
    def generate_report(self, start_date: str, end_date: str) -> Dict[str, any]:
        """Generate financial report for date range.
        
        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)
            
        Returns:
            Report dictionary
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT 
                    SUM(CASE WHEN type='income' THEN amount ELSE 0 END) as income,
                    SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) as expense,
                    COUNT(*) as transactions
                FROM transactions
                WHERE date BETWEEN ? AND ?
            ''', (start_date, end_date))
            
            result = cursor.fetchone()
            income = result[0] or 0
            expense = result[1] or 0
            count = result[2] or 0
            
            conn.close()
            
            return {
                'period': f"{start_date} to {end_date}",
                'total_income': income,
                'total_expense': expense,
                'net_balance': income - expense,
                'transaction_count': count,
                'average_transaction': (income + expense) / count if count > 0 else 0
            }
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return {}
    
    def track_metric(self, metric_name: str, value: float, date: Optional[str] = None) -> bool:
        """Track a business metric.
        
        Args:
            metric_name: Name of metric
            value: Metric value
            date: Optional date (defaults to today)
            
        Returns:
            True if successful
        """
        try:
            date = date or datetime.now().strftime('%Y-%m-%d')
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO metrics (date, metric_name, value)
                VALUES (?, ?, ?)
            ''', (date, metric_name, value))
            conn.commit()
            conn.close()
            logger.info(f"Tracked metric: {metric_name} = {value}")
            return True
        except Exception as e:
            logger.error(f"Error tracking metric: {e}")
            return False


if __name__ == "__main__":
    analytics = Analytics()
    
    # Example: Add transactions
    analytics.add_transaction(
        date="2024-01-15",
        category="Salary",
        amount=5000,
        transaction_type="income",
        description="Monthly salary"
    )
    
    analytics.add_transaction(
        date="2024-01-16",
        category="Groceries",
        amount=200,
        transaction_type="expense"
    )
    
    # Example: Get balance
    balance = analytics.get_balance()
    print(f"Balance: {balance}")
    
    # Example: Generate report
    report = analytics.generate_report("2024-01-01", "2024-01-31")
    print(f"Report: {report}")
