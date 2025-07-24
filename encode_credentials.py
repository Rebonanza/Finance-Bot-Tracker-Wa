#!/usr/bin/env python3
"""
Helper script to prepare credentials for production deployment
"""

import base64
import json
import os

def encode_credentials():
    """Encode credentials.json to base64 for production environment variable"""
    try:
        with open('credentials.json', 'r') as f:
            content = f.read()
        
        # Encode to base64
        encoded = base64.b64encode(content.encode()).decode()
        
        print("🔐 Encoded Google Credentials for Production")
        print("=" * 60)
        print("Copy this value and add it as GOOGLE_APPLICATION_CREDENTIALS_JSON")
        print("environment variable in Railway:")
        print()
        print(encoded)
        print()
        print("📋 Steps for Railway:")
        print("1. Go to Railway dashboard")
        print("2. Select your project")
        print("3. Go to Variables tab")
        print("4. Add new variable:")
        print("   Name: GOOGLE_APPLICATION_CREDENTIALS_JSON")
        print("   Value: [paste the encoded string above]")
        
        return encoded
        
    except FileNotFoundError:
        print("❌ credentials.json not found!")
        print("Make sure credentials.json exists in the current directory")
        return None
    except Exception as e:
        print(f"❌ Error encoding credentials: {str(e)}")
        return None

def show_environment_variables():
    """Show all environment variables needed for production"""
    
    env_vars = {
        'TWILIO_ACCOUNT_SID': 'Your Twilio Account SID',
        'TWILIO_AUTH_TOKEN': 'Your Twilio Auth Token',
        'TWILIO_WHATSAPP_NUMBER': 'whatsapp:+14155238886',
        'GOOGLE_SHEET_ID': 'Your Google Sheet ID',
        'GOOGLE_SHEET_NAME': 'Sheet1',
        'GOOGLE_APPLICATION_CREDENTIALS_JSON': 'Base64 encoded credentials.json (see above)'
    }
    
    print("\n📝 All Environment Variables Needed for Railway:")
    print("=" * 60)
    
    for key, description in env_vars.items():
        print(f"{key} = {description}")
    
    print("\n💡 Copy these from your .env file to Railway dashboard")

if __name__ == "__main__":
    print("🚀 Production Deployment Helper")
    print("=" * 60)
    
    encoded = encode_credentials()
    
    if encoded:
        show_environment_variables()
        print("\n✅ Ready for Railway deployment!")
    else:
        print("\n❌ Please fix the credentials issue first")
