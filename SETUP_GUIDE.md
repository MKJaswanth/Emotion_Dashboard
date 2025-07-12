# 🚀 Emotion Analytics - Setup Guide

## 📋 **Quick Start (5 minutes)**

### 1. **Install Dependencies**
```bash
cd backend
pip install -r requirements.txt
```

### 2. **Start the Backend Server**
```bash
python app.py
```
Server will start on `http://localhost:5000`

### 3. **Test the API**
```bash
python test_api.py
```

### 4. **View the Dashboards**
- Open `frontend/index.html` - Main user interface
- Open `frontend/dashboard.html` - Basic analytics
- Open `frontend/advanced-analytics.html` - AI-powered insights
- Open `frontend/enterprise-dashboard.html` - Enterprise features

---

## 🔧 **Detailed Setup**

### **Backend Setup**

1. **Install Python Dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Environment Variables (Optional):**
   Create a `.env` file in the backend directory:
   ```env
   JWT_SECRET=your-super-secret-key-change-this
   DISCORD_WEBHOOK_URL=your-discord-webhook-url
   ```

3. **Start the Server:**
   ```bash
   python app.py
   ```

4. **Verify Installation:**
   ```bash
   python test_api.py
   ```

### **Frontend Setup**

1. **Start a Local Server:**
   ```bash
   cd frontend
   npx http-server -p 8000
   ```

2. **Access the Application:**
   - Main App: `http://localhost:8000/index.html`
   - Dashboard: `http://localhost:8000/dashboard.html`
   - Advanced Analytics: `http://localhost:8000/advanced-analytics.html`
   - Enterprise Dashboard: `http://localhost:8000/enterprise-dashboard.html`

---

## 🧪 **Testing the API**

### **Manual Testing with curl:**

1. **Health Check:**
   ```bash
   curl http://localhost:5000/health
   ```

2. **API Info:**
   ```bash
   curl http://localhost:5000/api/test
   ```

3. **Register a User:**
   ```bash
   curl -X POST http://localhost:5000/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"test123","name":"Test User"}'
   ```

4. **Login:**
   ```bash
   curl -X POST http://localhost:5000/api/auth/login \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","password":"test123"}'
   ```

5. **Submit Mood (with token):**
   ```bash
   curl -X POST http://localhost:5000/api/mood/submit \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer YOUR_TOKEN_HERE" \
     -d '{"mood_score":4,"text":"Feeling great today!"}'
   ```

6. **Text Analysis:**
   ```bash
   curl -X POST http://localhost:5000/analyze-text \
     -H "Content-Type: application/json" \
     -d '{"text":"I am feeling very happy and excited about the project!"}'
   ```

---

## 🔍 **Troubleshooting**

### **Common Issues:**

1. **JWT Import Error:**
   ```bash
   pip install PyJWT==2.8.0
   ```

2. **NLTK Data Missing:**
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

3. **Port Already in Use:**
   ```bash
   # Kill process on port 5000
   lsof -ti:5000 | xargs kill -9
   ```

4. **CORS Issues:**
   - Make sure the backend is running on port 5000
   - Check that CORS is enabled in app.py

### **Debug Mode:**
```bash
# Start with debug logging
python app.py --debug
```

---

## 📊 **API Endpoints Reference**

### **Authentication:**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user

### **Mood Tracking:**
- `POST /api/mood/submit` - Submit mood entry (requires auth)
- `GET /api/mood/history` - Get mood history (requires auth)

### **Analytics:**
- `POST /analyze-text` - Analyze single text entry
- `GET /analyze-team/<team>` - Team sentiment analysis
- `POST /nlp-insights` - Comprehensive NLP insights

### **System:**
- `GET /health` - Health check
- `GET /api/test` - API information
- `GET /test-nlp` - Test NLP functionality

---

## 🎯 **Next Steps**

### **For Development:**
1. **Connect to Real Database:**
   - Replace mock databases with PostgreSQL/MongoDB
   - Add proper user management

2. **Add Payment Processing:**
   - Integrate Stripe for subscriptions
   - Implement pricing tiers

3. **Mobile App:**
   - Use the API to build React Native/Flutter app
   - Add push notifications

### **For Production:**
1. **Deploy Backend:**
   ```bash
   # Heroku
   heroku create your-app-name
   git push heroku main
   
   # Docker
   docker build -t emotion-analytics .
   docker run -p 5000:5000 emotion-analytics
   ```

2. **Deploy Frontend:**
   ```bash
   # Firebase Hosting
   firebase deploy
   
   # Netlify
   netlify deploy
   ```

3. **Set Environment Variables:**
   - Production JWT secret
   - Database connection strings
   - API keys for integrations

---

## 🔒 **Security Considerations**

### **Production Checklist:**
- [ ] Change default JWT secret
- [ ] Enable HTTPS
- [ ] Set up proper CORS origins
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Set up monitoring and logging
- [ ] Regular security updates

### **Data Privacy:**
- [ ] GDPR compliance
- [ ] Data encryption at rest
- [ ] Secure data transmission
- [ ] User consent management
- [ ] Data retention policies

---

## 📞 **Support**

### **Getting Help:**
1. **Check the logs:** Look at console output for errors
2. **Run tests:** Use `python test_api.py` to verify functionality
3. **Check documentation:** Review README.md and API docs
4. **Common issues:** See troubleshooting section above

### **API Documentation:**
- Swagger/OpenAPI docs available at `/api/docs` (when implemented)
- Test endpoints at `/api/test`
- Health check at `/health`

---

**🎉 You're all set! Your Emotion Analytics platform is ready to use.**

*For enterprise features, custom integrations, or support, please refer to the business case and pricing strategy documents.* 