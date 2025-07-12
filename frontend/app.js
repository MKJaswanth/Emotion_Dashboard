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
let db = null;
let auth = null;

try {
    firebase.initializeApp(firebaseConfig);
    db = firebase.database();
    auth = firebase.auth();
} catch (error) {
    // Fallback for when Firebase is not available
}

// Backend URL
const BACKEND_URL = 'https://emotion-dashboard-1-6kn0.onrender.com';

// Global variables
let selectedMood = null;
let selectedTeam = 'all';

// Inspirational quotes
const quotes = [
    { text: "Every day is a new beginning. Take a deep breath and start again.", author: "Anonymous" },
    { text: "You are stronger than you think and more capable than you imagine.", author: "Anonymous" },
    { text: "The only way to do great work is to love what you do.", author: "Steve Jobs" },
    { text: "Success is not final, failure is not fatal: it is the courage to continue that counts.", author: "Winston Churchill" },
    { text: "Believe you can and you're halfway there.", author: "Theodore Roosevelt" },
    { text: "The future belongs to those who believe in the beauty of their dreams.", author: "Eleanor Roosevelt" },
    { text: "Don't watch the clock; do what it does. Keep going.", author: "Sam Levenson" },
    { text: "The only limit to our realization of tomorrow is our doubts of today.", author: "Franklin D. Roosevelt" },
    { text: "It always seems impossible until it's done.", author: "Nelson Mandela" },
    { text: "Your time is limited, don't waste it living someone else's life.", author: "Steve Jobs" }
];

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const moodCards = document.querySelectorAll('.mood-card');
    const submitMoodBtn = document.getElementById('submit-mood');
    const textarea = document.getElementById('text-input');
    const submitTextBtn = document.getElementById('submit-text');
    const teamSelect = document.getElementById('team-select');
    const quoteText = document.getElementById('quote-text');
    const quoteAuthor = document.getElementById('quote-author');
    
    // Debug: Log element findings
    console.log('DOM Elements found:', {
        moodCards: moodCards.length,
        submitMoodBtn: !!submitMoodBtn,
        textarea: !!textarea,
        submitTextBtn: !!submitTextBtn,
        teamSelect: !!teamSelect,
        quoteText: !!quoteText,
        quoteAuthor: !!quoteAuthor
    });
    
    // Setup event listeners
    setupEventListeners();
    setupLogout();
    updateNavigation();
    
    // Load inspirational quotes
    loadRandomQuote();
    
    // Setup smooth scrolling
    setupSmoothScrolling();
    
    // Setup mobile navigation
    setupMobileNavigation();
    
    function setupEventListeners() {
        // Mood card selection
        if (moodCards && moodCards.length > 0) {
            moodCards.forEach((card, index) => {
                card.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    const mood = parseInt(this.dataset.mood);
                    selectMood(mood);
                });
            });
        }

        // Text area input
        if (textarea) {
            textarea.addEventListener('input', function() {
                const hasText = this.value.trim().length > 0;
                submitTextBtn.disabled = !hasText;
            });
        } else {
            console.error('Textarea not found!');
        }

        // Initially disable text submit button
        if (submitTextBtn) {
            submitTextBtn.disabled = true;
        } else {
            console.error('Submit text button not found!');
        }

        // Submit mood button
        if (submitMoodBtn) {
            submitMoodBtn.addEventListener('click', function(e) {
                e.preventDefault();
                submitMood();
            });
        }

        // Submit text button
        if (submitTextBtn) {
            submitTextBtn.addEventListener('click', function(e) {
                console.log('Submit text button clicked');
                e.preventDefault();
                submitText();
            });
        } else {
            console.error('Submit text button not found!');
        }

        // Start journey button
        const startJourneyBtn = document.getElementById('start-journey-btn');
        if (startJourneyBtn) {
            startJourneyBtn.addEventListener('click', function() {
                scrollToSection('mood-section');
            });
        }

        // New quote button
        const newQuoteBtn = document.getElementById('new-quote-btn');
        if (newQuoteBtn) {
            newQuoteBtn.addEventListener('click', function() {
                loadRandomQuote();
            });
        }
    }
});

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
    if (auth) {
        auth.signOut().then(() => {
            localStorage.removeItem('userRole');
            localStorage.removeItem('isLoggedIn');
            window.location.reload();
        }).catch((error) => {
            // Fallback logout
            localStorage.removeItem('userRole');
            localStorage.removeItem('isLoggedIn');
            window.location.reload();
        });
    } else {
        // Fallback logout without Firebase Auth
        localStorage.removeItem('userRole');
        localStorage.removeItem('isLoggedIn');
        window.location.reload();
    }
}

// Mood selection function
function selectMood(mood) {
    // Remove selected class from all cards
    const moodCards = document.querySelectorAll('.mood-card');
    if (moodCards) {
        moodCards.forEach(card => card.classList.remove('selected'));
    }
    
    // Add selected class to clicked card
    const selectedCard = document.querySelector(`[data-mood="${mood}"]`);
    if (selectedCard) {
        selectedCard.classList.add('selected');
        
        // Add animation effect
        selectedCard.style.transform = 'scale(1.1)';
        setTimeout(() => {
            selectedCard.style.transform = 'scale(1.05)';
        }, 200);
        selectedMood = mood;
    }
    
    // Enable submit button
    const submitMoodBtn = document.getElementById('submit-mood');
    if (submitMoodBtn) {
        submitMoodBtn.disabled = false;
    }
}

// Submit mood to Firebase
function submitMood() {
    if (!selectedMood) return;
    
    // Get selected team
    const teamSelect = document.getElementById('team-select');
    const team = teamSelect ? teamSelect.value : 'all';
    
    // Create mood entry
    const moodEntry = {
        mood: selectedMood,
        team: team,
        timestamp: Date.now()
    };
    
    // Save to Firebase
    if (db) {
        db.ref('mood_entries').push(moodEntry)
            .then(() => {
                showNotification('Mood submitted successfully! 😊', 'success');
                resetMoodSelection();
            })
            .catch(error => {
                showNotification('Error submitting mood. Please try again.', 'error');
            });
    } else {
        // Fallback: save to localStorage
        const entries = JSON.parse(localStorage.getItem('mood_entries') || '[]');
        entries.push(moodEntry);
        localStorage.setItem('mood_entries', JSON.stringify(entries));
        showNotification('Mood submitted successfully! 😊', 'success');
        resetMoodSelection();
    }
    
    // Send to backend
    sendMoodToBackend(moodEntry);
}

// Submit text to Firebase
function submitText() {
    console.log('Submit text function called');
    const textarea = document.getElementById('text-input');
    const text = textarea ? textarea.value.trim() : '';
    
    console.log('Textarea found:', !!textarea);
    console.log('Text content:', text);
    
    if (!text) {
        console.log('No text to submit');
        return;
    }
    
    // Get selected team
    const teamSelect = document.getElementById('team-select');
    const team = teamSelect ? teamSelect.value : 'all';
    
    // Create text entry
    const textEntry = {
        text: text,
        team: team,
        timestamp: Date.now()
    };
    
    // Save to Firebase
    if (db) {
        db.ref('text_entries').push(textEntry)
            .then(() => {
                showNotification('Your feelings have been shared! 💌', 'success');
                resetTextInput();
            })
            .catch(error => {
                showNotification('Error submitting text. Please try again.', 'error');
            });
    } else {
        // Fallback: save to localStorage
        const entries = JSON.parse(localStorage.getItem('text_entries') || '[]');
        entries.push(textEntry);
        localStorage.setItem('text_entries', JSON.stringify(entries));
        showNotification('Your feelings have been shared! 💌', 'success');
        resetTextInput();
    }
    
    // Send to backend
    sendTextToBackend(textEntry);
}

// Reset mood selection
function resetMoodSelection() {
    const moodCards = document.querySelectorAll('.mood-card');
    moodCards.forEach(card => card.classList.remove('selected'));
    selectedMood = null;
    
    const submitMoodBtn = document.getElementById('submit-mood');
    if (submitMoodBtn) {
        submitMoodBtn.disabled = true;
    }
}

// Reset text input
function resetTextInput() {
    const textarea = document.getElementById('text-input');
    if (textarea) {
        textarea.value = '';
    }
    
    const submitTextBtn = document.getElementById('submit-text');
    if (submitTextBtn) {
        submitTextBtn.disabled = true;
    }
}

// Send mood to backend
function sendMoodToBackend(moodEntry) {
    fetch(`${BACKEND_URL}/alert`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            avgMood: moodEntry.mood,
            team: moodEntry.team
        })
    }).catch(error => {
        // Silently fail - backend is optional
    });
}

// Send text to backend
function sendTextToBackend(textEntry) {
    fetch(`${BACKEND_URL}/analyze-text`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            text: textEntry.text
        })
    }).catch(error => {
        // Silently fail - backend is optional
    });
}

// Load random quote
function loadRandomQuote() {
    const quoteText = document.getElementById('quote-text');
    const quoteAuthor = document.getElementById('quote-author');
    
    if (!quoteText || !quoteAuthor) return;
    
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

// Setup mobile navigation
function setupMobileNavigation() {
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('nav-links');
    
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navLinks.classList.toggle('active');
        });
        
        // Close mobile menu when clicking on a link
        const mobileLinks = navLinks.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
            });
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
                hamburger.classList.remove('active');
                navLinks.classList.remove('active');
            }
        });
    }
}

// Setup smooth scrolling
function setupSmoothScrolling() {
    const links = document.querySelectorAll('a[href^="#"]');
    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
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
            if (document.body.contains(notification)) {
                document.body.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Add some interactive effects
document.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        if (scrolled > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        }
    }
});

// Export functions for global access
window.selectMood = selectMood;
window.submitMood = submitMood;
window.submitText = submitText;
window.loadRandomQuote = loadRandomQuote;
window.scrollToSection = scrollToSection;
window.updateNavigation = updateNavigation; 