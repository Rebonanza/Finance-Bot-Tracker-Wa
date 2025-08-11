import re
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta

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
        
        # Date patterns for parsing user input dates
        self.date_patterns = [
            # DD/MM/YYYY or DD-MM-YYYY
            r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})',
            # DD/MM or DD-MM (current year)
            r'(\d{1,2})[\/\-](\d{1,2})(?![\/\-]\d)',
            # Relative dates in Indonesian
            r'(kemarin|yesterday)',
            r'(lusa|besok|tomorrow)',
            r'(\d+)\s*hari\s*(?:yang\s*)?lalu',
            r'(\d+)\s*hari\s*lagi',
        ]
    
    def parse_message(self, message: str) -> Optional[Dict[str, str]]:
        """
        Parse a WhatsApp message for financial transaction
        
        Args:
            message: The message text to parse
            
        Returns:
            Dictionary with 'nama', 'tipe', 'nominal', 'tanggal' or None if parsing fails
        """
        if not message or not isinstance(message, str):
            return None
            
        original_message = message.strip()
        message = message.strip().lower()
        
        # Parse date first (if provided)
        parsed_date = self._parse_date(message)
        
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
        
        # Extract name (everything before the transaction type, excluding date)
        type_index = message.find(transaction_type)
        name_part = message[:type_index].strip()
        
        # Remove date from name if it was parsed
        if parsed_date and parsed_date != datetime.now().strftime('%Y-%m-%d %H:%M:%S'):
            name_part = self._remove_date_from_text(name_part, original_message)
        
        if not name_part:
            return None
        
        transaction = {
            'nama': name_part,
            'tipe': transaction_type,
            'nominal': str(int(amount))
        }
        
        # Add date if parsed
        if parsed_date:
            transaction['tanggal'] = parsed_date
        
        return transaction
    
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
    
    def _parse_date(self, text: str) -> Optional[str]:
        """Parse date from text and return formatted date string"""
        try:
            # Check for explicit date patterns
            for pattern in self.date_patterns:
                matches = re.search(pattern, text, re.IGNORECASE)
                if matches:
                    return self._convert_date_match(matches, pattern)
            
            # If no date found, return current datetime
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
        except Exception as e:
            print(f"Error parsing date: {e}")
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def _convert_date_match(self, match, pattern: str) -> str:
        """Convert regex match to formatted date string"""
        try:
            groups = match.groups()
            
            # DD/MM/YYYY or DD-MM-YYYY
            if r'(\d{4})' in pattern:
                day, month, year = int(groups[0]), int(groups[1]), int(groups[2])
                date_obj = datetime(year, month, day)
            
            # DD/MM or DD-MM (current year)
            elif len(groups) == 2 and groups[0].isdigit():
                day, month = int(groups[0]), int(groups[1])
                current_year = datetime.now().year
                date_obj = datetime(current_year, month, day)
            
            # Relative dates
            elif 'kemarin' in groups[0] or 'yesterday' in groups[0]:
                date_obj = datetime.now() - timedelta(days=1)
            
            elif 'lusa' in groups[0] or 'besok' in groups[0] or 'tomorrow' in groups[0]:
                date_obj = datetime.now() + timedelta(days=1)
            
            elif 'hari' in pattern and 'lalu' in pattern:
                days_ago = int(groups[0])
                date_obj = datetime.now() - timedelta(days=days_ago)
            
            elif 'hari' in pattern and 'lagi' in pattern:
                days_ahead = int(groups[0])
                date_obj = datetime.now() + timedelta(days=days_ahead)
            
            else:
                return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Keep current time but use parsed date
            current_time = datetime.now().time()
            final_datetime = datetime.combine(date_obj.date(), current_time)
            
            return final_datetime.strftime('%Y-%m-%d %H:%M:%S')
            
        except (ValueError, IndexError) as e:
            print(f"Error converting date: {e}")
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def _remove_date_from_text(self, text: str, original_text: str) -> str:
        """Remove date patterns from transaction name"""
        cleaned_text = text
        
        # Remove common date patterns from the text
        date_removal_patterns = [
            r'\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4}',
            r'\d{1,2}[\/\-]\d{1,2}(?![\/\-]\d)',
            r'kemarin|yesterday',
            r'lusa|besok|tomorrow',
            r'\d+\s*hari\s*(?:yang\s*)?lalu',
            r'\d+\s*hari\s*lagi',
        ]
        
        for pattern in date_removal_patterns:
            cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.IGNORECASE).strip()
        
        # Clean up extra spaces
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        
        return cleaned_text if cleaned_text else text
    
    def validate_transaction(self, transaction: Dict[str, str]) -> bool:
        """Validate that the transaction has all required fields"""
        required_fields = ['nama', 'tipe', 'nominal']
        return all(field in transaction and transaction[field] for field in required_fields)
