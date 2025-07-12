#!/bin/bash

echo "🚀 Emotion Tracker Deployment Script"
echo "====================================="

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found. Please initialize git first:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

# Check if remote is set
if ! git remote get-url origin > /dev/null 2>&1; then
    echo "❌ No remote repository found. Please add your GitHub repository:"
    echo "   git remote add origin https://github.com/yourusername/your-repo.git"
    exit 1
fi

echo "✅ Git repository found"

# Push to GitHub
echo "📤 Pushing to GitHub..."
git add .
git commit -m "Deploy emotion tracker $(date)"
git push origin main

echo "✅ Code pushed to GitHub"
echo ""
echo "🌐 Next Steps:"
echo "1. Go to https://render.com"
echo "2. Sign up and connect your GitHub repository"
echo "3. Create a new Web Service for backend"
echo "4. Create a new Static Site for frontend"
echo "5. Deploy both services"
echo ""
echo "📋 Backend Settings:"
echo "   Build Command: pip install -r requirements.txt"
echo "   Start Command: gunicorn app:app"
echo "   Environment: Python 3"
echo ""
echo "📋 Frontend Settings:"
echo "   Build Command: (leave empty)"
echo "   Publish Directory: frontend"
echo ""
echo "🔗 After deployment, update frontend URLs with your backend URL"