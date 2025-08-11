import os
from typing import Optional
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from family_config import FAMILY_CONFIG, get_family_member, get_bot_name, get_family_name

class WhatsAppBot:
    """Handle WhatsApp bot operations using Twilio"""
    
    def __init__(self):
        """Initialize WhatsApp bot with Twilio credentials"""
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
        
        # Custom bot configuration for family use
        self.bot_name = get_bot_name()
        self.family_name = get_family_name()
        
        # Family member mapping from config file
        self.family_members = FAMILY_CONFIG['family_members']
        
        if not all([self.account_sid, self.auth_token, self.whatsapp_number]):
            raise ValueError("Missing required Twilio environment variables")
        
        self.client = Client(self.account_sid, self.auth_token)
    
    def send_message(self, to_number: str, message: str) -> bool:
        """
        Send a WhatsApp message
        
        Args:
            to_number: Recipient's WhatsApp number (format: whatsapp:+1234567890)
            message: Message text to send
            
        Returns:
            True if message sent successfully, False otherwise
        """
        try:
            message = self.client.messages.create(
                body=message,
                from_=self.whatsapp_number,
                to=to_number
            )
            print(f"Message sent successfully. SID: {message.sid}")
            return True
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            return False
    
    def create_response(self, message: str) -> str:
        """
        Create a TwiML response for webhook
        
        Args:
            message: Response message text
            
        Returns:
            TwiML response as string
        """
        response = MessagingResponse()
        response.message(message)
        return str(response)
    
    def format_success_message(self, transaction: dict) -> str:
        """Format success message for transaction"""
        member_name = transaction.get('member', 'Family Member')
        
        # Format date for display
        date_display = ""
        if 'tanggal' in transaction and transaction['tanggal']:
            try:
                from datetime import datetime
                date_obj = datetime.strptime(transaction['tanggal'], '%Y-%m-%d %H:%M:%S')
                date_display = f"\n• Tanggal: {date_obj.strftime('%d/%m/%Y %H:%M')}"
            except:
                pass
        
        return f"""[SUCCESS] *{self.bot_name}*

Transaksi berhasil dicatat untuk {self.family_name}!

*Detail:*
• Member: {member_name}
• Nama: {transaction['nama']}
• Tipe: {transaction['tipe']}
• Nominal: Rp {int(transaction['nominal']):,}{date_display}

Data tersimpan di Google Sheets
Ketik 'laporan' untuk ringkasan"""
    
    def format_error_message(self, error_type: str = "parsing") -> str:
        """Format error message"""
        if error_type == "parsing":
            return f"""[ERROR] *{self.bot_name}*

Format pesan tidak valid!

*Contoh yang benar:*
• makan siang pengeluaran 20ribu
• gaji pemasukan 5juta kemarin
• transport pengeluaran 15k 15/07

Format: [nama] [pemasukan/pengeluaran] [nominal] [tanggal (opsional)]
Ketik 'help' untuk bantuan lengkap"""
        elif error_type == "sheets":
            return f"""[ERROR] *{self.bot_name}*

Gagal menyimpan ke Google Sheets
Silakan coba lagi dalam beberapa saat"""
        else:
            return f"""[ERROR] *{self.bot_name}*

Terjadi kesalahan sistem
Silakan coba lagi"""
    
    def format_help_message(self) -> str:
        """Format help message"""
        return f"""[HELP] *{self.bot_name}*
*Bot Keuangan {self.family_name}*

*Cara Pakai:*
Kirim pesan dengan format:
`[nama] [tipe] [nominal] [tanggal (opsional)]`

*Contoh Pemasukan:*
• gaji pemasukan 5juta
• bonus pemasukan 500ribu kemarin
• freelance pemasukan 2jt 15/07/2025

*Contoh Pengeluaran:*
• makan siang pengeluaran 20ribu
• bensin pengeluaran 50rb kemarin
• belanja pengeluaran 100k 20/7

*Format Tanggal:*
• 15/07/2025 atau 15-07-2025
• 15/07 atau 15-7 (tahun sekarang)
• kemarin, besok, lusa
• 3 hari lalu, 2 hari lagi
• (kosong = hari ini)

*Format Nominal:*
• 20ribu, 20rb, 20k = 20,000
• 5juta, 5jt, 5m = 5,000,000
• 500000 = angka langsung

*Perintah Lain:*
• `help` - Tampilkan bantuan ini
• `laporan` - Ringkasan keuangan
• `saldo` - Cek saldo terkini

*Semua data tersimpan di Google Sheets untuk akses keluarga!*"""
    
    def get_family_member(self, phone_number: str) -> str:
        """Get family member name from phone number"""
        return get_family_member(phone_number)
    
    def format_report_message(self, summary: dict) -> str:
        """Format financial report message"""
        return f"""[REPORT] *{self.bot_name}*
*Laporan Keuangan {self.family_name}*

*Ringkasan Bulan Ini:*
• Total Pemasukan: Rp {summary.get('total_pemasukan', 0):,}
• Total Pengeluaran: Rp {summary.get('total_pengeluaran', 0):,}
• Saldo: Rp {summary.get('saldo', 0):,}

*Transaksi Terakhir:*
{self._format_recent_transactions(summary.get('recent', []))}

Lihat detail lengkap di Google Sheets"""
    
    def _format_recent_transactions(self, transactions: list) -> str:
        """Format recent transactions for display"""
        if not transactions:
            return "• Belum ada transaksi"
        
        formatted = []
        for i, tx in enumerate(transactions[:5], 1):
            icon = "[IN]" if tx.get('tipe') == 'pemasukan' else "[OUT]"
            member = tx.get('member', 'Unknown')
            formatted.append(f"{i}. {icon} {tx['nama']} - Rp {int(tx['nominal']):,} ({member})")
        
        return "\n".join(formatted)
