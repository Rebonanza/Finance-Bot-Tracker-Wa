import os
from typing import List, Dict, Optional
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleSheetsManager:
    """Manage Google Sheets operations for finance tracking"""
    
    def __init__(self, credentials_file: str = 'credentials.json'):
        """
        Initialize Google Sheets manager
        
        Args:
            credentials_file: Path to Google service account credentials JSON file
        """
        self.credentials_file = credentials_file
        self.sheet_id = os.getenv('GOOGLE_SHEET_ID')
        self.sheet_name = os.getenv('GOOGLE_SHEET_NAME', 'Sheet1')
        self.service = None
        
        if not self.sheet_id:
            raise ValueError("GOOGLE_SHEET_ID environment variable is required")
        
        self._authenticate()
    
    def _authenticate(self):
        """Authenticate with Google Sheets API"""
        try:
            # Define the scope
            scopes = ['https://www.googleapis.com/auth/spreadsheets']
            
            # Try to load credentials from environment variable first (for production)
            credentials_json = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_JSON')
            
            if credentials_json:
                # Production: load from environment variable
                import json
                import base64
                
                # Decode base64 credentials
                decoded_credentials = base64.b64decode(credentials_json).decode('utf-8')
                credentials_info = json.loads(decoded_credentials)
                
                credentials = Credentials.from_service_account_info(
                    credentials_info, scopes=scopes
                )
            elif os.path.exists(self.credentials_file):
                # Local development: load from file
                credentials = Credentials.from_service_account_file(
                    self.credentials_file, scopes=scopes
                )
            else:
                # No credentials available
                raise Exception("No Google credentials found. Set GOOGLE_APPLICATION_CREDENTIALS_JSON environment variable or provide credentials.json file")
            
            # Build the service
            self.service = build('sheets', 'v4', credentials=credentials)
            
        except Exception as e:
            raise Exception(f"Failed to authenticate with Google Sheets: {str(e)}")
    
    def setup_sheet_headers(self) -> bool:
        """
        Setup the sheet with proper headers if they don't exist
        
        Returns:
            True if headers were set up successfully, False otherwise
        """
        try:
            # Check if headers already exist
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=f'{self.sheet_name}!A1:E1'
            ).execute()
            
            values = result.get('values', [])
            
            # Updated headers to include family member and timestamp
            expected_headers = ['Tanggal', 'Member', 'Nama', 'Tipe', 'Nominal']
            
            # If no headers or incorrect headers, set them up
            if not values or values[0] != expected_headers:
                headers = [expected_headers]
                
                self.service.spreadsheets().values().update(
                    spreadsheetId=self.sheet_id,
                    range=f'{self.sheet_name}!A1:E1',
                    valueInputOption='RAW',
                    body={'values': headers}
                ).execute()
                
                print("Headers set up successfully with family member tracking")
            
            return True
            
        except HttpError as e:
            print(f"Error setting up headers: {str(e)}")
            return False
    
    def add_transaction(self, transaction: Dict[str, str]) -> bool:
        """
        Add a transaction to the Google Sheet
        
        Args:
            transaction: Dictionary with 'nama', 'tipe', 'nominal', 'member' keys
            
        Returns:
            True if transaction was added successfully, False otherwise
        """
        try:
            from datetime import datetime
            
            # Prepare the data with timestamp and family member
            transaction_data = [[
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                transaction.get('member', 'Unknown'),
                transaction['nama'],
                transaction['tipe'],
                transaction['nominal']
            ]]
            
            # Add the transaction using append (easier than finding next row)
            self.service.spreadsheets().values().append(
                spreadsheetId=self.sheet_id,
                range=f'{self.sheet_name}!A:E',
                valueInputOption='RAW',
                body={'values': transaction_data}
            ).execute()
            
            print(f"Transaction added successfully: {transaction['nama']} - {transaction['tipe']} - {transaction['nominal']} ({transaction.get('member', 'Unknown')})")
            return True
            
        except HttpError as e:
            print(f"Error adding transaction: {str(e)}")
            return False
    
    def get_recent_transactions(self, limit: int = 10) -> List[Dict[str, str]]:
        """
        Get recent transactions from the sheet
        
        Args:
            limit: Maximum number of transactions to return
            
        Returns:
            List of transaction dictionaries
        """
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=f'{self.sheet_name}!A:E'
            ).execute()
            
            values = result.get('values', [])
            
            if not values or len(values) <= 1:
                return []
            
            # Skip header row and get recent transactions
            recent_values = values[1:][-limit:]
            
            transactions = []
            for row in recent_values:
                if len(row) >= 5:
                    transactions.append({
                        'tanggal': row[0],
                        'member': row[1],
                        'nama': row[2],
                        'tipe': row[3],
                        'nominal': row[4]
                    })
                elif len(row) >= 3:  # Support old format
                    transactions.append({
                        'tanggal': 'N/A',
                        'member': 'Unknown',
                        'nama': row[0],
                        'tipe': row[1],
                        'nominal': row[2]
                    })
            
            return transactions
            
        except HttpError as e:
            print(f"Error getting recent transactions: {str(e)}")
            return []
    
    def test_connection(self) -> bool:
        """Test the connection to Google Sheets"""
        try:
            # Try to get sheet metadata
            self.service.spreadsheets().get(spreadsheetId=self.sheet_id).execute()
            print("Google Sheets connection successful")
            return True
        except HttpError as e:
            print(f"Google Sheets connection failed: {str(e)}")
            return False
    
    def get_monthly_summary(self) -> Dict:
        """Get monthly financial summary for family"""
        try:
            from datetime import datetime
            current_month = datetime.now().strftime('%Y-%m')
            
            # Get all data
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range=f'{self.sheet_name}!A:E'
            ).execute()
            
            values = result.get('values', [])
            if len(values) <= 1:  # Only headers or empty
                return {'total_pemasukan': 0, 'total_pengeluaran': 0, 'saldo': 0, 'recent': []}
            
            total_pemasukan = 0
            total_pengeluaran = 0
            recent_transactions = []
            
            # Process data (skip header)
            for row in values[1:]:
                if len(row) >= 5:
                    date_str = row[0]
                    member = row[1]
                    nama = row[2]
                    tipe = row[3]
                    nominal = int(row[4])
                    
                    # Check if transaction is from current month
                    if current_month in date_str:
                        if tipe == 'pemasukan':
                            total_pemasukan += nominal
                        else:
                            total_pengeluaran += nominal
                    
                    # Add to recent transactions
                    recent_transactions.append({
                        'tanggal': date_str,
                        'member': member,
                        'nama': nama,
                        'tipe': tipe,
                        'nominal': nominal
                    })
                elif len(row) >= 3:  # Support old format
                    nama = row[0]
                    tipe = row[1]
                    nominal = int(row[2])
                    
                    if tipe == 'pemasukan':
                        total_pemasukan += nominal
                    else:
                        total_pengeluaran += nominal
                    
                    recent_transactions.append({
                        'tanggal': 'N/A',
                        'member': 'Unknown',
                        'nama': nama,
                        'tipe': tipe,
                        'nominal': nominal
                    })
            
            # Get 5 most recent
            recent_transactions = recent_transactions[-5:]
            
            return {
                'total_pemasukan': total_pemasukan,
                'total_pengeluaran': total_pengeluaran,
                'saldo': total_pemasukan - total_pengeluaran,
                'recent': recent_transactions
            }
            
        except Exception as e:
            print(f"❌ Error getting summary: {str(e)}")
            return {'total_pemasukan': 0, 'total_pengeluaran': 0, 'saldo': 0, 'recent': []}
    
    def get_current_balance(self) -> int:
        """Get current balance"""
        summary = self.get_monthly_summary()
        return summary.get('saldo', 0)
