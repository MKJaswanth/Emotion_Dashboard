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

firebase.initializeApp(firebaseConfig);
const db = firebase.database();

// Backend URL
const BACKEND_URL = 'https://emotion-dashboard-1-6kn0.onrender.com';

// Global variables
let moodCounts = [0, 0, 0, 0, 0];
let textEntries = [];
let allMoodEntries = [];
let allTextEntries = [];
let selectedTeam = 'all';

// Chart Setup with better configuration
const ctx = document.getElementById("moodChart").getContext("2d");
const moodChart = new Chart(ctx, {
    type: "bar",
    data: {
        labels: ["😞", "😐", "🙂", "😊", "😁"],
        datasets: [{
            label: "Mood Count",
            data: moodCounts,
            backgroundColor: ["#f44336", "#ff9800", "#ffc107", "#4caf50", "#2196f3"],
            borderRadius: 8,
            borderSkipped: false,
            borderWidth: 0,
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                backgroundColor: 'rgba(0,0,0,0.8)',
                titleColor: 'white',
                bodyColor: 'white',
                borderColor: '#667eea',
                borderWidth: 1,
                cornerRadius: 8,
                displayColors: false,
                callbacks: {
                    label: function(context) {
                        return `Count: ${context.parsed.y}`;
                    }
                }
            }
        },
        scales: {
            y: { 
                beginAtZero: true,
                grid: {
                    color: 'rgba(0,0,0,0.1)',
                    drawBorder: false
                },
                ticks: {
                    color: '#666',
                    font: {
                        size: 12
                    }
                }
            },
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    color: '#666',
                    font: {
                        size: 16
                    }
                }
            }
        },
        animation: {
            duration: 1000,
            easing: 'easeInOutQuart'
        }
    }
});

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    checkAdminAuth();
    setupLogout();
});

// Check admin authentication using Firebase Auth
function checkAdminAuth() {
    const auth = firebase.auth();
    
    auth.onAuthStateChanged(function(user) {
        if (!user) {
            console.log('No user logged in, redirecting to login...');
            window.location.href = 'login.html';
            return;
        }
        
        console.log('User authenticated:', user.email);
        // Continue with dashboard initialization
        initializeDashboard();
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

// Logout function using Firebase Auth
function logout() {
    const auth = firebase.auth();
    auth.signOut().then(function() {
        console.log('User signed out successfully');
        window.location.href = 'login.html';
    }).catch(function(error) {
        console.error('Logout error:', error);
    });
}

// Initialize dashboard after authentication
function initializeDashboard() {
    setupTeamFilter();
    updateLastUpdated();
    // Start listening to Firebase data
    startDataListeners();
}

// Setup team filter
function setupTeamFilter() {
    const teamFilter = document.getElementById('team-filter');
    teamFilter.addEventListener('change', function() {
        selectedTeam = this.value;
        updateDashboard();
    });
}

// Update last updated timestamp
function updateLastUpdated() {
    const now = new Date();
    const timeString = now.toLocaleTimeString();
    document.getElementById('last-updated').textContent = timeString;
}

// Start Firebase data listeners
function startDataListeners() {
    // Listen to mood_entries in real-time
    db.ref("mood_entries").on("value", (snapshot) => {
        allMoodEntries = [];
        snapshot.forEach((child) => {
            const entry = child.val();
            allMoodEntries.push(entry);
        });
        updateDashboard();
    });

    // Listen to text_entries in real-time
    db.ref("text_entries").on("value", (snapshot) => {
        allTextEntries = [];
        snapshot.forEach((child) => {
            const entry = child.val();
            allTextEntries.push({
                text: entry.text,
                team: entry.team,
                date: new Date(entry.timestamp).toLocaleString(),
                timestamp: entry.timestamp
            });
        });
        updateDashboard();
    });
}

// Update dashboard based on selected team
function updateDashboard() {
    // Filter mood entries by selected team
    const filteredMoodEntries = selectedTeam === 'all' 
        ? allMoodEntries 
        : allMoodEntries.filter(entry => entry.team === selectedTeam);

    // Filter text entries by selected team
    const filteredTextEntries = selectedTeam === 'all'
        ? allTextEntries
        : allTextEntries.filter(entry => entry.team === selectedTeam);

    // Calculate mood statistics
    let moodCounts = [0, 0, 0, 0, 0];
    let total = 0;
    let count = 0;
    let happyCount = 0;
    let neutralCount = 0;
    let sadCount = 0;

    filteredMoodEntries.forEach(entry => {
        const mood = entry.mood;
        if (mood >= 1 && mood <= 5) {
            moodCounts[mood - 1]++;
            total += mood;
            count++;
            
            // Categorize moods
            if (mood >= 4) happyCount++;
            else if (mood === 3) neutralCount++;
            else sadCount++;
        }
    });

    const avgMood = count > 0 ? (total / count).toFixed(1) : 0;

    // Update the chart with smooth animation
    moodChart.data.datasets[0].data = moodCounts;
    moodChart.update('active');

    // Update all stats
    document.getElementById('total-entries').textContent = count;
    document.getElementById('avg-mood').textContent = avgMood;
    document.getElementById('text-entries-count').textContent = filteredTextEntries.length;
    document.getElementById('happy-count').textContent = happyCount;
    document.getElementById('neutral-count').textContent = neutralCount;
    document.getElementById('sad-count').textContent = sadCount;

    // Update text entries display
    displayTextEntries(filteredTextEntries);

    // Update timestamp
    updateLastUpdated();

    // Show team-specific alert
    if (avgMood < 2.5 && count > 0) {
        const teamName = selectedTeam === 'all' ? 'Overall Team' : getTeamDisplayName(selectedTeam);
        showLowMoraleAlert(avgMood, teamName);
    }
}

// Get team display name
function getTeamDisplayName(teamValue) {
    const teamNames = {
        '1st-year': '1st Year Students',
        '2nd-year': '2nd Year Students',
        '3rd-year': '3rd Year Students',
        '4th-year': '4th Year Students',
        'faculty': 'Faculty/Staff',
        'other': 'Other'
    };
    return teamNames[teamValue] || teamValue;
}

// Display text entries
function displayTextEntries(entries) {
    const container = document.getElementById('text-entries-list');
    
    if (entries.length === 0) {
        const teamName = selectedTeam === 'all' ? 'any team' : getTeamDisplayName(selectedTeam);
        container.innerHTML = `
            <div style="text-align: center; color: #666; padding: 40px;">
                <div style="font-size: 3rem; margin-bottom: 20px;">📝</div>
                <p>No text entries from ${teamName} yet.</p>
                <p style="font-size: 0.9rem; opacity: 0.7;">Encourage them to share their feelings!</p>
            </div>
        `;
        return;
    }

    // Sort by timestamp (newest first)
    entries.sort((a, b) => b.timestamp - a.timestamp);

    // Show only the 10 most recent entries
    const recentEntries = entries.slice(0, 10);
    
    container.innerHTML = recentEntries.map(entry => `
        <div class="entry-item">
            <div class="entry-text">"${entry.text}"</div>
            <div class="entry-date">
                ${entry.date} 
                <span class="team-badge">${getTeamDisplayName(entry.team)}</span>
            </div>
        </div>
    `).join('');
}

// Show low morale alert
function showLowMoraleAlert(avgMood, teamName) {
    // Create alert element
    const alert = document.createElement('div');
    alert.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        z-index: 10000;
        max-width: 350px;
        animation: slideIn 0.5s ease;
    `;
    
    alert.innerHTML = `
        <h3 style="margin: 0 0 10px 0; font-size: 1.2rem;">⚠️ Low Morale Alert</h3>
        <p style="margin: 0; font-size: 0.9rem;">${teamName} average mood is ${avgMood}/5. Consider checking in with them!</p>
    `;
    
    document.body.appendChild(alert);
    
    // Remove after 5 seconds
    setTimeout(() => {
        alert.style.animation = 'slideOut 0.5s ease';
        setTimeout(() => {
            if (document.body.contains(alert)) {
                document.body.removeChild(alert);
            }
        }, 500);
    }, 5000);

    // Send Discord notification via backend
    sendDiscordAlert(avgMood, teamName);
}

// Send Discord alert via backend
function sendDiscordAlert(avgMood, teamName) {
    fetch(`${BACKEND_URL}/alert`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            avgMood: avgMood,
            team: selectedTeam
        })
    })
    .then(res => res.json())
    .then(data => console.log("📤 Alert sent via backend:", data))
    .catch(err => console.error("❌ Backend alert error:", err));
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);