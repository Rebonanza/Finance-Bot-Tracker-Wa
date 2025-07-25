# 🚀 Railway Deployment Guide

Deploy your WhatsApp Finance Tracker Bot to Railway for FREE!

## 🎯 Two Deployment Methods

### **Method 1: GitHub Auto-Deploy (Recommended)**

This method automatically deploys whenever you push to GitHub.

### **Step 1: Connect to Railway**

1. Go to [Railway.app](https://railway.app) and sign up with GitHub
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `finance-tracker-bot-wa` repository
4. Railway will detect Python and start building automatically
5. **Wait for first deployment to complete** (2-3 minutes)
6. Go to Settings → Domains → Generate Domain
7. **Enable Auto-Deploy**: Toggle "Auto-Deploy" ON

### **Step 2: Configure Environment Variables**

Add these variables in Railway Dashboard → Variables:

```
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
GOOGLE_SHEET_ID=your_google_sheet_id_here
GOOGLE_SHEET_NAME=Sheet1
GOOGLE_APPLICATION_CREDENTIALS_JSON=your_base64_encoded_credentials_here
```

💡 **Get your actual values from:**
- Twilio Console for TWILIO_* variables
- Google Sheets URL for GOOGLE_SHEET_ID  
- Run `python3 encode_credentials.py` for GOOGLE_APPLICATION_CREDENTIALS_JSON

### **Step 3: Test Auto-Deployment**

1. Make any small change to your code (e.g., add a comment)
2. Push to GitHub: `git add . && git commit -m "test deploy" && git push`
3. Railway will automatically redeploy! ✨

---

### **Method 2: Railway CLI (Alternative)**

If you prefer command-line deployment:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Create new project
railway create finance-tracker-bot

# Set environment variables
railway variables set TWILIO_ACCOUNT_SID=your_account_sid
railway variables set TWILIO_AUTH_TOKEN=your_auth_token
railway variables set TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
railway variables set GOOGLE_SHEET_ID=your_sheet_id
railway variables set GOOGLE_SHEET_NAME=Sheet1
railway variables set GOOGLE_APPLICATION_CREDENTIALS_JSON=your_base64_credentials

# Deploy
railway up
```

## 📱 Configure Twilio Webhook

After deployment, update your Twilio WhatsApp webhook:

1. **Copy your Railway URL** (e.g., `https://your-app.railway.app`)
2. **Go to Twilio Console** → WhatsApp Sandbox
3. **Set webhook URL**: `https://your-app.railway.app/webhook`
4. **Save Configuration**

## ✅ Testing Deployment

Send a WhatsApp message to your bot:
```
beli nasi goreng 15ribu
```

You should see:
- ✅ Bot responds with confirmation
- ✅ Data appears in Google Sheets
- ✅ Railway logs show successful request

## 🔧 Troubleshooting

### **Common Issues:**

1. **"No start command found"**
   - ✅ Fixed by `Procfile` and `nixpacks.toml`

2. **"Google Sheets 403 error"**
   - Share your sheet with service account email
   - Check GOOGLE_APPLICATION_CREDENTIALS_JSON is valid base64

3. **"Twilio webhook fails"**
   - Verify webhook URL in Twilio Console
   - Check Railway domain is accessible

4. **"App crashes on startup"**
   - Check Railway logs for specific error
   - Verify all environment variables are set

### **View Logs:**
```bash
railway logs
```

## 🎉 Success!

Your WhatsApp Finance Bot is now live on Railway! 

**Benefits:**
- ✅ Free hosting
- ✅ Auto-deploy from GitHub
- ✅ HTTPS enabled
- ✅ 24/7 uptime
- ✅ Easy scaling

Share the bot with your family and start tracking finances! 💰📊
