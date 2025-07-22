# WhatsApp Finance Tracker Bot

This is a WhatsApp bot that tracks your finances and automatically logs transactions to Google Sheets.

## Features

- Parse WhatsApp messages for financial transactions
- Support for income (pemasukan) and expense (pengeluaran) tracking
- Automatic data entry to Google Sheets
- Flexible amount parsing (supports "20ribu", "20k", "20000", etc.)

## Setup Instructions

### 1. Twilio WhatsApp Setup

1. Create a Twilio account at https://www.twilio.com/
2. Get your Twilio WhatsApp Sandbox credentials
3. Note down your Account SID, Auth Token, and WhatsApp number

### 2. Google Sheets API Setup

1. Go to https://console.developers.google.com/
2. Create a new project or select existing one
3. Enable Google Sheets API
4. Create credentials (Service Account)
5. Download the JSON key file and rename it to `credentials.json`
6. Place it in the project root directory
7. Create a Google Sheet and share it with the service account email

### 3. Environment Variables

Create a `.env` file with the following:

```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
GOOGLE_SHEET_ID=your_google_sheet_id
GOOGLE_SHEET_NAME=Sheet1
```

### 4. Installation

```bash
pip install -r requirements.txt
```

### 5. Run the Bot

```bash
python app.py
```

### 6. Expose to Internet (for Twilio webhook)

Use ngrok to expose your local server:
```bash
ngrok http 5000
```

Then set the webhook URL in Twilio console to: `https://your-ngrok-url.ngrok.io/webhook`

## Usage

Send WhatsApp messages in this format:
- `makan siang pengeluaran 20ribu`
- `gaji pemasukan 5juta`
- `transport pengeluaran 15k`

The bot will parse and add entries to your Google Sheet with columns: Nama, Tipe, Nominal.

## Message Format

- **Name**: Description of the transaction (e.g., "makan siang", "gaji")
- **Type**: Either "pemasukan" (income) or "pengeluaran" (expense)
- **Amount**: Flexible formats like "20ribu", "20k", "20000", "5juta", etc.
