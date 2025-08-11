#!/usr/bin/env python3
"""
Test script for the WhatsApp Finance Tracker Bot
"""

from message_parser import MessageParser

def test_message_parser():
    """Test the message parser with various input formats"""
    parser = MessageParser()
    
    test_cases = [
        # Basic cases
        ("makan siang pengeluaran 20ribu", {"nama": "makan siang", "tipe": "pengeluaran", "nominal": "20000"}),
        ("gaji pemasukan 5juta", {"nama": "gaji", "tipe": "pemasukan", "nominal": "5000000"}),
        ("transport pengeluaran 15k", {"nama": "transport", "tipe": "pengeluaran", "nominal": "15000"}),
        
        # Different amount formats
        ("belanja bulanan pengeluaran 500000", {"nama": "belanja bulanan", "tipe": "pengeluaran", "nominal": "500000"}),
        ("bonus pemasukan 2.5juta", {"nama": "bonus", "tipe": "pemasukan", "nominal": "2500000"}),
        ("kopi pengeluaran 25ribu", {"nama": "kopi", "tipe": "pengeluaran", "nominal": "25000"}),
        
        # Edge cases
        ("bensin pengeluaran 50rb", {"nama": "bensin", "tipe": "pengeluaran", "nominal": "50000"}),
        ("freelance pemasukan 1.2m", {"nama": "freelance", "tipe": "pemasukan", "nominal": "1200000"}),
        
        # Should fail
        ("makan siang 20ribu", None),  # No transaction type
        ("pengeluaran 20ribu", None),  # No name
        ("makan siang pengeluaran", None),  # No amount
        ("", None),  # Empty string
    ]
    
    # Add date test cases
    date_test_cases = [
        # With dates - just check if parsing succeeds and has date field
        ("makan siang pengeluaran 20ribu kemarin", {"has_date": True}),
        ("gaji pemasukan 5juta 15/07/2025", {"has_date": True}),
        ("transport pengeluaran 15k besok", {"has_date": True}),
        ("belanja pengeluaran 100k 3 hari lalu", {"has_date": True}),
    ]
    
    print("[TEST] Testing Message Parser...")
    print("=" * 50)
    
    passed = 0
    total = len(test_cases)
    
    for i, (message, expected) in enumerate(test_cases, 1):
        result = parser.parse_message(message)
        
        # Compare results
        success = (result == expected)
        if success:
            passed += 1
            status = "[PASS]"
        else:
            status = "[FAIL]"
        
        print(f"{i:2d}. {status}")
        print(f"    Input: '{message}'")
        print(f"    Expected: {expected}")
        print(f"    Got:      {result}")
        print()
    
    print("=" * 50)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    return passed == total

def test_amount_parsing():
    """Test amount parsing specifically"""
    parser = MessageParser()
    
    test_amounts = [
        ("20ribu", 20000),
        ("5juta", 5000000),
        ("15k", 15000),
        ("500000", 500000),
        ("2.5juta", 2500000),
        ("1.2m", 1200000),
        ("50rb", 50000),
        ("10000", 10000),
    ]
    
    print("\n[TEST] Testing Amount Parsing...")
    print("=" * 50)
    
    for amount_text, expected in test_amounts:
        test_message = f"test pengeluaran {amount_text}"
        result = parser.parse_message(test_message)
        
        if result and result['nominal'] == str(int(expected)):
            print(f"[PASS] '{amount_text}' -> {int(expected):,}")
        else:
            actual = result['nominal'] if result else "None"
            print(f"[FAIL] '{amount_text}' -> Expected: {int(expected):,}, Got: {actual}")

if __name__ == "__main__":
    print("[TEST] WhatsApp Finance Tracker Bot - Test Suite")
    print("=" * 50)
    
    # Run tests
    parser_success = test_message_parser()
    test_amount_parsing()
    
    print("\n" + "=" * 50)
    if parser_success:
        print("[SUCCESS] All tests passed! Your bot parser is ready.")
    else:
        print("[WARNING] Some tests failed. Please check the implementation.")
    
    print("\n[INFO] Usage Examples:")
    print("  • makan siang pengeluaran 20ribu")
    print("  • gaji pemasukan 5juta") 
    print("  • transport pengeluaran 15k")
    print("  • belanja bulanan pengeluaran 500000")
