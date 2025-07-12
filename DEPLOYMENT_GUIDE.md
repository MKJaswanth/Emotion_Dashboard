# 🚀 Emotion Tracker - Deployment Guide

## 📋 Prerequisites
- Python 3.11+
- Git
- Firebase project (already configured)

## 🌐 Hosting Options

### Option 1: Render (Recommended - Free)

#### Backend Deployment:
1. **Sign up** at [render.com](https://render.com)
2. **Connect your GitHub** repository
3. **Create a new Web Service**
4. **Configure settings:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Environment:** Python 3
5. **Deploy** and get your backend URL

#### Frontend Deployment:
1. **Create a new Static Site** on Render
2. **Connect your repository**
3. **Build Command:** Leave empty
4. **Publish Directory:** `frontend`
5. **Deploy** and get your frontend URL

### Option 2: Heroku (Paid)

#### Backend Deployment:
1. **Install Heroku CLI**
2. **Login:** `heroku login`
3. **Create app:** `heroku create your-app-name`
4. **Deploy:** `git push heroku main`
5. **Scale:** `heroku ps:scale web=1`

#### Frontend Deployment:
1. **Use Netlify** or **Vercel** for frontend
2. **Connect repository**
3. **Set build directory** to `frontend`

### Option 3: Railway (Free Tier)

1. **Sign up** at [railway.app](https://railway.app)
2. **Connect GitHub** repository
3. **Deploy** automatically
4. **Get URLs** for both services

## 🔧 Configuration

### Backend Environment Variables:
```bash
PORT=5000
FLASK_ENV=production
```

### Frontend Configuration:
Update Firebase config in all frontend files with your production URLs.

## 📁 File Structure for Deployment:
```
├── backend/
│   ├── app.py
│   ├── nlp_service.py
│   ├── requirements.txt
│   ├── Procfile
│   ├── runtime.txt
│   └── wsgi.py
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   ├── nlp-dashboard.html
│   ├── app.js
│   ├── dashboard.js
│   ├── nlp-dashboard.js
│   └── styles.css
└── DEPLOYMENT_GUIDE.md
```

## 🔗 Update Frontend URLs

After deploying backend, update these files:
- `frontend/nlp-dashboard.js` - Line with fetch URL
- `frontend/dashboard.js` - Any backend API calls

## 🚀 Quick Deploy Commands

### Render (Recommended):
```bash
# 1. Push to GitHub
git add .
git commit -m "Ready for deployment"
git push origin main

# 2. Deploy on Render
# - Go to render.com
# - Connect repository
# - Deploy backend first
# - Deploy frontend second
```

### Local Testing:
```bash
# Backend
cd backend
python app.py

# Frontend
# Open frontend/index.html in browser
```

## 🔒 Security Notes:
- Update Discord webhook URL for production
- Consider environment variables for sensitive data
- Enable HTTPS in production
- Set up proper CORS policies

## 📞 Support:
- Check logs in hosting platform dashboard
- Test endpoints with Postman/curl
- Verify Firebase configuration