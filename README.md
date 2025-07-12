<<<<<<< HEAD
=======

>>>>>>> 9b41492cb2827bc779b6b21bca91f0884ce0581b
# 🎭 Emotion Tracker - Real-Time Mood Dashboard

A beautiful, modern web application for tracking team emotions and feelings in real-time. Built with HTML, CSS, JavaScript, and Firebase.

## ✨ Features

### 🌟 User Interface (`index.html`)
- **Welcome Section**: Beautiful landing page with animated elements
- **Mood Selection**: Interactive emoji cards for mood selection (1-5 scale)
- **Text Input**: Text area for sharing feelings and thoughts
- **Inspirational Quotes**: Random motivational quotes with refresh functionality
- **Smooth Scrolling**: Seamless navigation between sections
- **Responsive Design**: Works perfectly on desktop and mobile

### 📊 Analytics Dashboard (`dashboard.html`)
- **Real-time Charts**: Live mood distribution visualization
- **Quick Stats**: Total entries, average mood, text entries count
- **Recent Entries**: Display of recent text submissions
- **Low Morale Alerts**: Automatic Discord notifications when team morale is low
- **Modern UI**: Beautiful gradient backgrounds and glass-morphism effects

## 🚀 How to Use

### For Users (Team Members)
1. Open `index.html` in your web browser
2. Scroll through the welcome section
3. Select your current mood using the emoji cards
4. Click "Submit Mood" to save your mood
5. Scroll to the text section and share your feelings
6. Click "Share My Feelings" to submit your text
7. Enjoy the inspirational quote at the end!

### For Administrators (Team Leaders)
1. Open `dashboard.html` to view real-time analytics
2. Monitor mood distribution and trends
3. Read recent text entries from team members
4. Receive automatic alerts when team morale is low
5. Get Discord notifications for immediate action

## 🛠️ Technical Details

### Frontend Technologies
- **HTML5**: Semantic structure and accessibility
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript (ES6+)**: Interactive functionality and Firebase integration
- **Chart.js**: Beautiful data visualization
- **Google Fonts**: Poppins font family for modern typography

### Backend & Database
- **Firebase Realtime Database**: Real-time data storage and synchronization
- **Firebase Hosting**: Easy deployment (optional)

### Key Features
- **Real-time Updates**: All data updates instantly across all connected users
- **Offline Support**: Basic functionality works without internet
- **Mobile Responsive**: Optimized for all device sizes
- **Smooth Animations**: Engaging user experience with CSS animations
- **Error Handling**: Graceful error handling and user feedback

## 📁 File Structure

```
frontend/
├── index.html          # Main user interface
├── dashboard.html      # Analytics dashboard
├── styles.css          # Main stylesheet
├── app.js             # Main application logic
├── dashboard.js       # Dashboard analytics logic
└── script.js          # Legacy script (can be removed)
```

## 🔧 Setup Instructions

### Prerequisites
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Firebase project with Realtime Database enabled

### Installation
1. Clone or download this repository
2. Open `frontend/index.html` in your web browser
3. Start using the application!

### Firebase Configuration
The application is already configured with Firebase. If you want to use your own Firebase project:

1. Create a new Firebase project
2. Enable Realtime Database
3. Update the Firebase config in `app.js` and `dashboard.js`
4. Set up database rules for security

## 🎨 Customization

### Colors and Themes
- Edit `styles.css` to change colors, gradients, and overall theme
- Modify the CSS variables for easy color customization

### Quotes Database
- Add more quotes in the `quotes` array in `app.js`
- Each quote should have `text` and `author` properties

### Discord Integration
- Update the Discord webhook URL in `dashboard.js` for your own server
- Customize the alert messages and conditions

## 📊 Data Structure

### Mood Entries
```javascript
{
  mood: 1-5,           // Mood rating (1=Very Sad, 5=Very Happy)
  timestamp: 1234567890, // Unix timestamp
  date: "2024-01-01T00:00:00.000Z" // ISO date string
}
```

### Text Entries
```javascript
{
  text: "I'm feeling great today!", // User's text input
  timestamp: 1234567890,           // Unix timestamp
  date: "2024-01-01T00:00:00.000Z" // ISO date string
}
```

## 🔮 Future Enhancements

- **NLP Analysis**: Sentiment analysis of text entries
- **User Authentication**: Individual user accounts and profiles
- **Team Management**: Multiple teams and organizations
- **Advanced Analytics**: Trend analysis and predictions
- **Export Features**: Data export to CSV/PDF
- **Mobile App**: Native mobile application
- **API Integration**: Connect with other productivity tools

## 🤝 Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Improving the UI/UX
- Adding new functionality
- Optimizing performance

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Support

If you need help or have questions:
1. Check the browser console for error messages
2. Verify your Firebase configuration
3. Ensure all files are in the correct directory structure
4. Test with a different browser

---

**Made with ❤️ for better team mental health and emotional wellness!** 
=======
# Emotion_Dashboard
>>>>>>> ee865b00f7afd4343978156c585b341113780bc4
