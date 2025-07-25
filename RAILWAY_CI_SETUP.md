# 🚄 Railway CI/CD Setup Guide

## 📋 Prerequisites
- GitHub repository with your WhatsApp bot code
- Railway account with deployed project
- Admin access to GitHub repository

## 🔑 Step 1: Get Railway Credentials

### 1.1 Get Railway Token
1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click on your profile (bottom left)
3. Go to "Account Settings"
4. Navigate to "Tokens"
5. Click "Create Token"
6. Copy the token (it starts with `railway_`)

### 1.2 Get Project ID
1. In Railway dashboard, open your project
2. Go to "Settings" tab
3. Copy the "Project ID" (format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

### 1.3 Get Service ID
1. In your Railway project, click on your service
2. Go to "Settings" tab
3. Copy the "Service ID" (format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`)

## 🔐 Step 2: Configure GitHub Secrets

1. Go to your GitHub repository
2. Click "Settings" → "Secrets and variables" → "Actions"
3. Click "New repository secret" and add these three secrets:

| Secret Name | Description | Example |
|------------|-------------|---------|
| `RAILWAY_TOKEN` | Your Railway API token | `railway_xxxxxxxxxxxxxxxxx` |
| `RAILWAY_PROJECT_ID` | Your Railway project ID | `12345678-1234-1234-1234-123456789012` |
| `RAILWAY_SERVICE_ID` | Your Railway service ID | `87654321-4321-4321-4321-210987654321` |

## 🚀 Step 3: Test the Workflow

1. Make any small change to your code
2. Commit and push to `main` branch:
   ```bash
   git add .
   git commit -m "🧪 Test auto deployment"
   git push origin main
   ```
3. Go to "Actions" tab in GitHub to see the deployment progress

## 📊 Workflow Features

✅ **Automatic Testing**: Runs tests before deployment  
✅ **Smart Deployment**: Only deploys from `main` branch  
✅ **Status Reporting**: Clear success/failure messages  
✅ **Pull Request Testing**: Tests PRs without deploying  

## 🔄 Workflow Behavior

| Event | Action |
|-------|--------|
| Push to `main` | Run tests → Deploy to Railway |
| Push to other branch | Run tests only |
| Pull Request | Run tests only |
| Test failure | Skip deployment |

## 🛠️ Troubleshooting

### Common Issues:

1. **"Invalid Railway token"**
   - Check if token is correct and not expired
   - Regenerate token if needed

2. **"Project/Service not found"**
   - Verify Project ID and Service ID are correct
   - Make sure the token has access to the project

3. **"Tests failing"**
   - Check test output in Actions tab
   - Fix code issues before deployment

4. **"Deployment stuck"**
   - Check Railway logs for deployment status
   - Verify environment variables are set in Railway

## 🎯 Next Steps

After setup:
1. Your bot will auto-deploy on every push to `main`
2. Monitor deployments in GitHub Actions
3. Check Railway dashboard for service status
4. Update Twilio webhook URL if Railway URL changes

## 📱 Update Twilio Webhook

When Railway redeploys, make sure your Twilio webhook URL is:
```
https://your-railway-app.railway.app/webhook
```

Happy coding! 🚀
