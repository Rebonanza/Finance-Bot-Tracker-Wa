#!/usr/bin/env python3
"""
Setup script to help configure the WhatsApp Finance Tracker Bot
"""

import os
import json
from google_sheets_manager import GoogleSheetsManager
from dotenv import load_dotenv

def create_env_file():
    """Create .env file with user input"""
    print("🔧 Setting up environment variables...")
    
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Please edit it manually or delete it to run setup again.")
        return False
    
    print("\n📱 Twilio WhatsApp Configuration:")
    print("You need to sign up for Twilio and get your WhatsApp sandbox credentials.")
    print("Visit: https://www.twilio.com/console/sms/whatsapp/sandbox")
    
    account_sid = input("Enter your Twilio Account SID: ").strip()
    auth_token = input("Enter your Twilio Auth Token: ").strip()
    whatsapp_number = input("Enter your Twilio WhatsApp number (e.g., whatsapp:+14155238886): ").strip()
    
    print("\n📊 Google Sheets Configuration:")
    print("You need to create a Google Sheet and get its ID from the URL.")
    print("Example: https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit")
    
    sheet_id = input("Enter your Google Sheet ID: ").strip()
    sheet_name = input("Enter your sheet name (default: Sheet1): ").strip() or "Sheet1"
    
    # Create .env file
    env_content = f"""TWILIO_ACCOUNT_SID={account_sid}
TWILIO_AUTH_TOKEN={auth_token}
TWILIO_WHATSAPP_NUMBER={whatsapp_number}
GOOGLE_SHEET_ID={sheet_id}
GOOGLE_SHEET_NAME={sheet_name}
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    return True

def check_credentials_file():
    """Check if Google credentials file exists"""
    if not os.path.exists('credentials.json'):
        print("❌ credentials.json file not found!")
        print("\n📋 To create Google service account credentials:")
        print("1. Go to https://console.developers.google.com/")
        print("2. Create a new project or select existing one")
        print("3. Enable Google Sheets API")
        print("4. Create credentials (Service Account)")
        print("5. Download the JSON key file")
        print("6. Rename it to 'credentials.json' and place it in this directory")
        print("7. Share your Google Sheet with the service account email")
        return False
    
    print("✅ credentials.json found!")
    return True

def test_google_sheets():
    """Test Google Sheets connection"""
    if not check_credentials_file():
        return False
    
    try:
        load_dotenv()
        sheets_manager = GoogleSheetsManager()
        
        if sheets_manager.test_connection():
            print("✅ Google Sheets connection successful!")
            
            # Setup headers
            if sheets_manager.setup_sheet_headers():
                print("✅ Sheet headers configured!")
            
            return True
        else:
            print("❌ Google Sheets connection failed!")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Google Sheets: {str(e)}")
        return False

def check_service_account_email():
    """Show service account email for sharing the sheet"""
    try:
        with open('credentials.json', 'r') as f:
            creds = json.load(f)
            email = creds.get('client_email')
            if email:
                print(f"\n📧 Service Account Email: {email}")
                print("📝 Make sure to share your Google Sheet with this email address!")
                return True
    except Exception as e:
        print(f"Error reading credentials: {str(e)}")
    return False

def main():
    """Main setup function"""
    print("🤖 WhatsApp Finance Tracker Bot Setup")
    print("=" * 50)
    
    # Step 1: Create .env file
    if not os.path.exists('.env'):
        if not create_env_file():
            return
    else:
        print("✅ .env file already exists")
    
    # Step 2: Check credentials
    if not check_credentials_file():
        print("\n⏳ Please complete the Google credentials setup and run this script again.")
        return
    
    # Step 3: Show service account email
    check_service_account_email()
    
    # Step 4: Test Google Sheets
    print("\n🧪 Testing Google Sheets connection...")
    if not test_google_sheets():
        print("\n⚠️  Please check your Google Sheets configuration.")
        return
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Install ngrok: https://ngrok.com/")
    print("2. Run the bot: python app.py")
    print("3. In another terminal, run: ngrok http 5000")
    print("4. Copy the ngrok URL and set it as webhook in Twilio console")
    print("5. Add '/webhook' to the end of the URL")
    print("6. Start chatting with your WhatsApp bot!")
    
    print("\n💬 Example messages to try:")
    print("  • makan siang pengeluaran 20ribu")
    print("  • gaji pemasukan 5juta")
    print("  • help")

if __name__ == "__main__":
    main()
