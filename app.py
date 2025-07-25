import os
from flask import Flask, request
from dotenv import load_dotenv
from message_parser import MessageParser
from google_sheets_manager import GoogleSheetsManager
from whatsapp_bot import WhatsAppBot

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize components
parser = MessageParser()
sheets_manager = None
whatsapp_bot = None

def initialize_components():
    """Initialize Google Sheets and WhatsApp bot components"""
    global sheets_manager, whatsapp_bot
    
    try:
        # Initialize Google Sheets manager
        sheets_manager = GoogleSheetsManager()
        sheets_manager.setup_sheet_headers()
        
        # Initialize WhatsApp bot
        whatsapp_bot = WhatsAppBot()
        
        print("✅ All components initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing components: {str(e)}")
        return False

# Initialize components immediately when module loads (for production)
print("🚀 Initializing WhatsApp Finance Tracker Bot components...")
if not initialize_components():
    print("❌ Warning: Some components failed to initialize")

@app.route('/')
def home():
    """Home endpoint"""
    return "WhatsApp Finance Tracker Bot is running! 🤖💰"

@app.route('/health')
def health():
    """Health check endpoint for Railway"""
    try:
        status = {
            "status": "healthy",
            "timestamp": "2025-07-25",
            "components": {
                "parser": parser is not None,
                "sheets_manager": sheets_manager is not None,
                "whatsapp_bot": whatsapp_bot is not None
            }
        }
        
        # If components aren't initialized, try to initialize them
        if not all(status["components"].values()):
            print("🔄 Some components not initialized, attempting initialization...")
            if initialize_components():
                status["components"]["sheets_manager"] = sheets_manager is not None
                status["components"]["whatsapp_bot"] = whatsapp_bot is not None
                status["initialization"] = "success"
            else:
                status["initialization"] = "failed"
        
        return status, 200
        
    except Exception as e:
        return {"status": "error", "error": str(e)}, 500

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages"""
    try:
        # Check if components are initialized
        if not whatsapp_bot or not sheets_manager:
            print("❌ Components not initialized, attempting to initialize...")
            if not initialize_components():
                return "Components initialization failed", 500
        
        # Get message data from Twilio
        incoming_msg = request.values.get('Body', '').strip()
        from_number = request.values.get('From', '')
        
        # Get family member name
        family_member = whatsapp_bot.get_family_member(from_number)
        
        print(f"Received message from {family_member} ({from_number}): {incoming_msg}")
        
        # Handle help command
        if incoming_msg.lower() in ['help', 'bantuan', 'panduan']:
            response_msg = whatsapp_bot.format_help_message()
            return whatsapp_bot.create_response(response_msg)
        
        # Handle report command
        elif incoming_msg.lower() in ['laporan', 'report', 'ringkasan']:
            summary = sheets_manager.get_monthly_summary()
            response_msg = whatsapp_bot.format_report_message(summary)
            return whatsapp_bot.create_response(response_msg)
        
        # Handle balance command
        elif incoming_msg.lower() in ['saldo', 'balance']:
            balance = sheets_manager.get_current_balance()
            response_msg = f"💰 *{whatsapp_bot.bot_name}*\n\nSaldo {whatsapp_bot.family_name}: Rp {balance:,}"
            return whatsapp_bot.create_response(response_msg)
        
        # Parse the message
        transaction = parser.parse_message(incoming_msg)
        
        if not transaction or not parser.validate_transaction(transaction):
            response_msg = whatsapp_bot.format_error_message("parsing")
            return whatsapp_bot.create_response(response_msg)
        
        # Add family member to transaction
        transaction['member'] = family_member
        
        # Add transaction to Google Sheets
        if sheets_manager.add_transaction(transaction):
            response_msg = whatsapp_bot.format_success_message(transaction)
        else:
            response_msg = whatsapp_bot.format_error_message("sheets")
        
        return whatsapp_bot.create_response(response_msg)
        
    except Exception as e:
        print(f"Error in webhook: {str(e)}")
        error_msg = whatsapp_bot.format_error_message("general") if whatsapp_bot else "Terjadi kesalahan sistem."
        return whatsapp_bot.create_response(error_msg) if whatsapp_bot else error_msg

@app.route('/test')
def test_connections():
    """Test endpoint to check all connections"""
    results = {}
    
    # Test Google Sheets connection
    if sheets_manager:
        results['google_sheets'] = sheets_manager.test_connection()
    else:
        results['google_sheets'] = False
    
    # Test message parsing
    test_messages = [
        "makan siang pengeluaran 20ribu",
        "gaji pemasukan 5juta",
        "transport pengeluaran 15k"
    ]
    
    parsing_results = []
    for msg in test_messages:
        parsed = parser.parse_message(msg)
        parsing_results.append({
            'message': msg,
            'parsed': parsed,
            'valid': parser.validate_transaction(parsed) if parsed else False
        })
    
    results['message_parsing'] = parsing_results
    
    return {
        'status': 'OK' if results['google_sheets'] else 'ERROR',
        'results': results
    }

@app.route('/recent')
def recent_transactions():
    """Get recent transactions from Google Sheets"""
    if not sheets_manager:
        return {'error': 'Google Sheets not initialized'}
    
    transactions = sheets_manager.get_recent_transactions(10)
    return {
        'count': len(transactions),
        'transactions': transactions
    }

if __name__ == '__main__':
    print("🚀 Starting WhatsApp Finance Tracker Bot...")
    
    # Initialize components
    if initialize_components():
        # Get port from environment variable for production deployment
        port = int(os.environ.get('PORT', 5000))
        print(f"📱 Starting Flask server on port {port}")
        print("🔗 Webhook URL: /webhook")
        print("🧪 Test URL: /test")
        
        # Production-safe settings
        app.run(debug=False, host='0.0.0.0', port=port)
    else:
        print("❌ Failed to initialize components. Please check your configuration.")
