#!/usr/bin/env python3
"""
Railway project setup helper
"""

def get_railway_project_info():
    """Get Railway project information for GitHub Actions"""
    
    print("🚄 Railway Project Setup for GitHub Actions")
    print("=" * 60)
    print()
    print("📋 To get your Railway project information:")
    print()
    print("1. 🌐 Go to Railway Dashboard: https://railway.app/dashboard")
    print("2. 🎯 Select your WhatsApp Finance Bot project")
    print("3. ⚙️  Click on Settings tab")
    print("4. 📊 Copy the following information:")
    print()
    print("   • Project ID: Found in Settings → General")
    print("   • Service ID: Found in Settings → Service")
    print("   • API Token: Account Settings → API Tokens → Create")
    print()
    print("🔐 Add these as GitHub Secrets:")
    print("   Repository → Settings → Secrets and variables → Actions")
    print()
    print("   RAILWAY_TOKEN=your_api_token")
    print("   RAILWAY_PROJECT_ID=your_project_id")
    print("   RAILWAY_SERVICE_ID=your_service_id")
    print()
    print("🎯 GitHub Actions will then auto-deploy on push to main!")

def show_webhook_info():
    """Show webhook setup information"""
    
    print("\n📱 Twilio Webhook Configuration")
    print("=" * 60)
    print()
    print("After Railway deployment:")
    print("1. 🌐 Get your Railway URL from dashboard")
    print("2. 📞 Go to Twilio Console → WhatsApp Sandbox")
    print("3. 🔗 Set Webhook URL: https://your-app.railway.app/webhook")
    print("4. 💾 Save configuration")
    print("5. 🧪 Test with WhatsApp message!")

if __name__ == "__main__":
    get_railway_project_info()
    show_webhook_info()
    print("\n🎉 Your auto-deployment setup is complete!")
    print("🚀 Push to main branch to trigger deployment!")
