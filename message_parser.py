import re
from typing import Dict, Optional, Tuple

class MessageParser:
    """Parse WhatsApp messages for finance transactions"""
    
    def __init__(self):
        # Patterns for amount parsing
        self.amount_patterns = {
            r'(\d+(?:\.?\d+)?)\s*(?:ribu|rb|k)': lambda x: float(x) * 1000,
            r'(\d+(?:\.?\d+)?)\s*(?:juta|jt|m)': lambda x: float(x) * 1000000,
            r'(\d+(?:\.?\d+)?)': lambda x: float(x),
        }
        
        # Transaction types
        self.transaction_types = ['pemasukan', 'pengeluaran']
    
    def parse_message(self, message: str) -> Optional[Dict[str, str]]:
        """
        Parse a WhatsApp message for financial transaction
        
        Args:
            message: The message text to parse
            
        Returns:
            Dictionary with 'nama', 'tipe', 'nominal' or None if parsing fails
        """
        if not message or not isinstance(message, str):
            return None
            
        message = message.strip().lower()
        
        # Find transaction type
        transaction_type = None
        for t_type in self.transaction_types:
            if t_type in message:
                transaction_type = t_type
                break
        
        if not transaction_type:
            return None
        
        # Parse amount
        amount = self._parse_amount(message)
        if amount is None:
            return None
        
        # Extract name (everything before the transaction type)
        type_index = message.find(transaction_type)
        name_part = message[:type_index].strip()
        
        if not name_part:
            return None
        
        return {
            'nama': name_part,
            'tipe': transaction_type,
            'nominal': str(int(amount))
        }
    
    def _parse_amount(self, text: str) -> Optional[float]:
        """Extract and convert amount from text"""
        for pattern, converter in self.amount_patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    # Use the last match found (usually the amount)
                    return converter(matches[-1])
                except (ValueError, IndexError):
                    continue
        return None
    
    def validate_transaction(self, transaction: Dict[str, str]) -> bool:
        """Validate that the transaction has all required fields"""
        required_fields = ['nama', 'tipe', 'nominal']
        return all(field in transaction and transaction[field] for field in required_fields)
