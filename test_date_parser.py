#!/usr/bin/env python3
"""
Test script for date parsing functionality
"""

from message_parser import MessageParser
from datetime import datetime, timedelta

def test_date_parsing():
    parser = MessageParser()
    
    # Test cases with various date formats
    test_messages = [
        # Basic transaction (no date)
        "makan siang pengeluaran 20ribu",
        
        # Specific dates
        "makan siang pengeluaran 20ribu 15/07/2025",
        "gaji pemasukan 5juta 15-07-2025",
        "belanja pengeluaran 100k 20/7",
        "transport pengeluaran 15ribu 5-8",
        
        # Relative dates
        "makan siang pengeluaran 20ribu kemarin",
        "gaji pemasukan 5juta besok",
        "belanja pengeluaran 100k lusa",
        "transport pengeluaran 15ribu 3 hari lalu",
        "snack pengeluaran 5ribu 2 hari lagi",
        
        # Invalid formats (should still work for basic parsing)
        "makan siang pengeluaran 20ribu 32/13/2025",  # Invalid date
        "makan siang pengeluaran 20ribu yesterday",   # English
    ]
    
    print("🧪 Testing Date Parsing Functionality\n")
    print("=" * 60)
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n{i}. Testing: '{message}'")
        
        result = parser.parse_message(message)
        
        if result:
            print(f"✅ Parsed successfully:")
            print(f"   • Nama: {result['nama']}")
            print(f"   • Tipe: {result['tipe']}")
            print(f"   • Nominal: {result['nominal']}")
            
            if 'tanggal' in result:
                try:
                    date_obj = datetime.strptime(result['tanggal'], '%Y-%m-%d %H:%M:%S')
                    print(f"   • Tanggal: {date_obj.strftime('%d/%m/%Y %H:%M')}")
                except:
                    print(f"   • Tanggal: {result['tanggal']}")
            else:
                print(f"   • Tanggal: Current time (default)")
                
            is_valid = parser.validate_transaction(result)
            print(f"   • Valid: {is_valid}")
        else:
            print("❌ Failed to parse")
        
        print("-" * 40)
    
    print("\n🎯 Summary:")
    print("The date parsing functionality supports:")
    print("• DD/MM/YYYY and DD-MM-YYYY formats")
    print("• DD/MM and DD-MM (current year)")
    print("• Relative dates: kemarin, besok, lusa")
    print("• Days ago/ahead: 'X hari lalu', 'X hari lagi'")
    print("• Default to current time if no date provided")
    print("• Graceful fallback for invalid dates")

if __name__ == "__main__":
    test_date_parsing()
