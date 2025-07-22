# Family Configuration for WhatsApp Finance Bot
"""
This file contains configuration for your family finance bot.
Update the values below to customize the bot for your family.
"""

# Family Configuration
FAMILY_CONFIG = {
    # Customize these names for your family
    'family_name': 'Finance Tracker',  # Change this to your family name
    'bot_name': 'Finance Tracker Bot',
    'currency': 'Rp',
    
    # Map phone numbers to family member names
    # IMPORTANT: Update these with your family's actual WhatsApp numbers
    'family_members': {
        # Format: 'whatsapp:+country_code_phone_number': 'Display_Name'
        # Examples (replace with real numbers):
        'whatsapp:+6289541178980': 'Cece',       # Your number (example)
        'whatsapp:+6285183276425': 'Given',        # Sister's number (example)
        'whatsapp:+6289612524288': 'Mama',        # Mom's number (example)
        'whatsapp:+62895396408060': 'Papa',        # Dad's number (example)
        
        # Add more family members as needed
        # 'whatsapp:+6281234567894': 'Paman',
        # 'whatsapp:+6281234567895': 'Tante',
    },
    
    # Custom messages
    'welcome_message': 'Welcome back gais! 👨‍👩‍👧‍👦',
    'success_emoji': '🎉',
    'error_emoji': '❌',
    'currency_symbol': 'Rp',
    
    # Transaction categories (optional for future features)
    'expense_categories': ['makan', 'transport', 'belanja', 'tagihan', 'hiburan', 'kesehatan'],
    'income_categories': ['gaji', 'bonus', 'freelance', 'bisnis', 'hadiah']
}

def get_family_member(phone_number: str) -> str:
    """Get family member name from phone number"""
    return FAMILY_CONFIG['family_members'].get(phone_number, 'Family Member')

def get_bot_name() -> str:
    """Get bot display name"""
    return FAMILY_CONFIG['bot_name']

def get_family_name() -> str:
    """Get family name"""
    return FAMILY_CONFIG['family_name']

def get_all_family_members() -> dict:
    """Get all family members mapping"""
    return FAMILY_CONFIG['family_members']

# Instructions for setup:
"""
HOW TO SETUP FOR YOUR FAMILY:

1. UPDATE FAMILY NAMES:
   - Change 'family_name' to your actual family name
   - Update 'bot_name' if you want a different bot name

2. GET REAL PHONE NUMBERS:
   - Ask each family member for their WhatsApp number
   - Include country code (e.g., +62 for Indonesia, +1 for US)
   - Format: whatsapp:+country_code_number

3. UPDATE FAMILY_MEMBERS MAPPING:
   - Replace the example numbers with real ones
   - Use meaningful names (Mama, Papa, Kakak, Adik, etc.)

4. TWILIO SANDBOX SETUP:
   - Each family member needs to join your Twilio sandbox
   - Send them the join code from your Twilio console
   - They send: "join [your-code]" to +1 415 523 8886

5. GOOGLE SHEETS ACCESS:
   - Share your Google Sheet with family members (optional)
   - They can view transactions but only the bot can write

EXAMPLE OF REAL SETUP:
{
    'whatsapp:+6281234567890': 'Sarah (Kakak)',
    'whatsapp:+6287654321098': 'Maya (Adik)', 
    'whatsapp:+6281122334455': 'Mama',
    'whatsapp:+6285566778899': 'Papa',
}
"""
