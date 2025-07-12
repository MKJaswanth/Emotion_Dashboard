// Firebase Config
const firebaseConfig = {
    apiKey: "AIzaSyC639yfUtTgHbCmnqUp_J7uZ3RrFUbR5PU",
    authDomain: "emotion-dashboard-d31ca.firebaseapp.com",
    databaseURL: "https://emotion-dashboard-d31ca-default-rtdb.firebaseio.com",
    projectId: "emotion-dashboard-d31ca",
    storageBucket: "emotion-dashboard-d31ca.firebasestorage.app",
    messagingSenderId: "191620106192",
    appId: "1:191620106192:web:68fe5b79d2ee42ecd71bd5",
    measurementId: "G-6DJ6ZF946J"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const db = firebase.database();
const auth = firebase.auth();

// Check authentication status
auth.onAuthStateChanged(function(user) {
    if (user) {
        // User is signed in
        localStorage.setItem('userRole', 'user');
        localStorage.setItem('isLoggedIn', 'true');
        updateNavigation();
    } else {
        // User is signed out
        localStorage.removeItem('userRole');
        localStorage.removeItem('isLoggedIn');
        updateNavigation();
    }
});

// Global variables
let selectedMood = null;
let quotes = [
    {
        text: "Every day is a new beginning. Take a deep breath and start again.",
        author: "Anonymous"
    },
    {
        text: "The only way to do great work is to love what you do.",
        author: "Steve Jobs"
    },
    {
        text: "Happiness is not something ready-made. It comes from your own actions.",
        author: "Dalai Lama"
    },
    {
        text: "Life is 10% what happens to you and 90% how you react to it.",
        author: "Charles R. Swindoll"
    },
    {
        text: "The future belongs to those who believe in the beauty of their dreams.",
        author: "Eleanor Roosevelt"
    },
    {
        text: "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        author: "Winston Churchill"
    },
    {
        text: "Believe you can and you're halfway there.",
        author: "Theodore Roosevelt"
    },
    {
        text: "The only limit to our realization of tomorrow is our doubts of today.",
        author: "Franklin D. Roosevelt"
    },
    {
        text: "It does not matter how slowly you go as long as you do not stop.",
        author: "Confucius"
    },
    {
        text: "The journey of a thousand miles begins with one step.",
        author: "Lao Tzu"
    },
    {
        text: "What you get by achieving your goals is not as important as what you become by achieving your goals.",
        author: "Zig Ziglar"
    },
    {
        text: "The mind is everything. What you think you become.",
        author: "Buddha"
    },
    {
        text: "Don't watch the clock; do what it does. Keep going.",
        author: "Sam Levenson"
    },
    {
        text: "The best way to predict the future is to create it.",
        author: "Peter Drucker"
    },
    {
        text: "Your time is limited, don't waste it living someone else's life.",
        author: "Steve Jobs"
    }
];

// DOM Elements
const moodCards = document.querySelectorAll('.mood-card');
const submitMoodBtn = document.getElementById('submit-mood');
const feelingTextarea = document.getElementById('feeling-text');
const submitTextBtn = document.getElementById('submit-text');
const quoteText = document.getElementById('quote-text');
const quoteAuthor = document.getElementById('quote-author');
const teamSelect = document.getElementById('team-select');

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    loadRandomQuote();
    setupEventListeners();
    setupLogout();
    updateNavigation();
});

// Setup event listeners
function setupEventListeners() {
    // Mood card selection
    moodCards.forEach(card => {
        card.addEventListener('click', function() {
            const mood = parseInt(this.dataset.mood);
            selectMood(mood);
        });
    });

    // Text area input
    feelingTextarea.addEventListener('input', function() {
        submitTextBtn.disabled = this.value.trim().length === 0;
    });
}

// Setup logout functionality
function setupLogout() {
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            logout();
        });
    }
}

// Update navigation based on user role
function updateNavigation() {
    const userRole = localStorage.getItem('userRole');
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    const adminLink = document.getElementById('admin-link');
    const logoutBtn = document.getElementById('logout-btn');
    const signinLink = document.getElementById('signin-link');
    
    if (userRole === 'admin' && isLoggedIn) {
        if (adminLink) adminLink.style.display = 'inline-block';
        if (logoutBtn) logoutBtn.style.display = 'inline-block';
        if (signinLink) signinLink.style.display = 'none';
    } else if (userRole === 'user' && isLoggedIn) {
        if (adminLink) adminLink.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'inline-block';
        if (signinLink) signinLink.style.display = 'none';
    } else {
        if (adminLink) adminLink.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'none';
        if (signinLink) signinLink.style.display = 'inline-block';
    }
}

// Logout function
function logout() {
    auth.signOut().then(() => {
        localStorage.removeItem('userRole');
        localStorage.removeItem('isLoggedIn');
        window.location.reload();
    }).catch((error) => {
        console.error('Logout error:', error);
        // Fallback logout
        localStorage.removeItem('userRole');
        localStorage.removeItem('isLoggedIn');
        window.location.reload();
    });
}

// Mood selection function
function selectMood(mood) {
    selectedMood = mood;
    
    // Remove selected class from all cards
    moodCards.forEach(card => card.classList.remove('selected'));
    
    // Add selected class to clicked card
    const selectedCard = document.querySelector(`[data-mood="${mood}"]`);
    selectedCard.classList.add('selected');
    
    // Enable submit button
    submitMoodBtn.disabled = false;
    
    // Add animation effect
    selectedCard.style.transform = 'scale(1.1)';
    setTimeout(() => {
        selectedCard.style.transform = 'scale(1.05)';
    }, 200);
}

// Submit mood to Firebase
function submitMood() {
    if (!selectedMood) {
        showNotification('Please select a mood first!', 'error');
        return;
    }

    if (!teamSelect.value) {
        showNotification('Please select your team/class first!', 'error');
        return;
    }

    const moodData = {
        mood: selectedMood,
        team: teamSelect.value,
        timestamp: Date.now(),
        date: new Date().toISOString()
    };

    // Save to Firebase
    db.ref('mood_entries').push(moodData)
        .then(() => {
            showNotification('Mood submitted successfully! 😊', 'success');
            
            // Reset selection
            moodCards.forEach(card => card.classList.remove('selected'));
            selectedMood = null;
            submitMoodBtn.disabled = true;
            
            // Scroll to next section
            setTimeout(() => {
                scrollToSection('text-section');
            }, 1000);
        })
        .catch(error => {
            console.error('Error submitting mood:', error);
            showNotification('Error submitting mood. Please try again.', 'error');
        });
}

// Submit text to Firebase
function submitText() {
    const text = feelingTextarea.value.trim();
    
    if (!text) {
        showNotification('Please write something about your feelings!', 'error');
        return;
    }

    if (!teamSelect.value) {
        showNotification('Please select your team/class first!', 'error');
        return;
    }

    const textData = {
        text: text,
        team: teamSelect.value,
        timestamp: Date.now(),
        date: new Date().toISOString()
    };

    // Save to Firebase
    db.ref('text_entries').push(textData)
        .then(() => {
            showNotification('Your feelings have been shared! 💌', 'success');
            
            // Clear textarea
            feelingTextarea.value = '';
            submitTextBtn.disabled = true;
            
            // Scroll to quotes section
            setTimeout(() => {
                scrollToSection('quotes-section');
            }, 1000);
        })
        .catch(error => {
            console.error('Error submitting text:', error);
            showNotification('Error submitting text. Please try again.', 'error');
        });
}

// Load random quote
function loadRandomQuote() {
    const randomIndex = Math.floor(Math.random() * quotes.length);
    const quote = quotes[randomIndex];
    
    // Add fade out effect
    quoteText.style.opacity = '0';
    quoteAuthor.style.opacity = '0';
    
    setTimeout(() => {
        quoteText.textContent = `"${quote.text}"`;
        quoteAuthor.textContent = `- ${quote.author}`;
        
        // Add fade in effect
        quoteText.style.opacity = '1';
        quoteAuthor.style.opacity = '1';
    }, 300);
}

// Smooth scroll to section
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        z-index: 10000;
        transform: translateX(400px);
        transition: transform 0.3s ease;
        max-width: 300px;
        font-weight: 500;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add some interactive effects
document.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const navbar = document.querySelector('.navbar');
    
    if (scrolled > 100) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
    }
});

// Add loading animation for buttons
function addLoadingState(button) {
    const originalText = button.textContent;
    button.textContent = 'Loading...';
    button.disabled = true;
    
    return () => {
        button.textContent = originalText;
        button.disabled = false;
    };
}

// Export functions for global access
window.selectMood = selectMood;
window.submitMood = submitMood;
window.submitText = submitText;
window.loadRandomQuote = loadRandomQuote;
window.scrollToSection = scrollToSection; 