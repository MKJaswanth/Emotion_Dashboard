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

// Global variables
let allTextEntries = [];
let selectedTeam = 'all';
let sentimentChart = null;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    checkAdminAuth();
    setupTeamFilter();
    setupSentimentChart();
    setupLogout();
    loadTextEntries();
});

// Check admin authentication
function checkAdminAuth() {
    const userRole = localStorage.getItem('userRole');
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    
    if (userRole !== 'admin' || !isLoggedIn) {
        window.location.href = 'login.html';
        return;
    }
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

// Logout function
function logout() {
    localStorage.removeItem('userRole');
    localStorage.removeItem('isLoggedIn');
    window.location.href = 'index.html';
}

// Setup team filter
function setupTeamFilter() {
    const teamFilter = document.getElementById('team-filter');
    teamFilter.addEventListener('change', function() {
        selectedTeam = this.value;
        updateTextEntries();
    });
}

// Setup sentiment chart
function setupSentimentChart() {
    const ctx = document.getElementById("sentimentChart").getContext("2d");
    sentimentChart = new Chart(ctx, {
        type: "doughnut",
        data: {
            labels: ["Positive", "Neutral", "Negative"],
            datasets: [{
                data: [0, 0, 0],
                backgroundColor: ["#4CAF50", "#ff9800", "#f44336"],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0,0,0,0.8)',
                    titleColor: 'white',
                    bodyColor: 'white',
                    borderColor: '#667eea',
                    borderWidth: 1,
                    cornerRadius: 8
                }
            }
        }
    });
}

// Load text entries from Firebase
function loadTextEntries() {
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
        updateTextEntries();
    });
}

// Update text entries based on selected team
function updateTextEntries() {
    const filteredEntries = selectedTeam === 'all'
        ? allTextEntries
        : allTextEntries.filter(entry => entry.team === selectedTeam);
    
    // Enable analyze button if there are entries
    const analyzeBtn = document.getElementById('analyze-btn');
    analyzeBtn.disabled = filteredEntries.length === 0;
    
    if (filteredEntries.length === 0) {
        showNoDataMessage();
    }
}

// Show no data message
function showNoDataMessage() {
    document.getElementById('insights-container').innerHTML = `
        <div class="loading">
            <div style="font-size: 3rem; margin-bottom: 20px;">📝</div>
            <p>No text entries found for the selected team.</p>
            <p style="font-size: 0.9rem; opacity: 0.7;">Submit some text entries to analyze sentiment!</p>
        </div>
    `;
}

// Analyze team sentiment
async function analyzeTeamSentiment() {
    const filteredEntries = selectedTeam === 'all'
        ? allTextEntries
        : allTextEntries.filter(entry => entry.team === selectedTeam);
    
    if (filteredEntries.length === 0) {
        showNoDataMessage();
        return;
    }
    
    // Show loading state
    showLoadingState();
    
    try {
        // Prepare data for analysis
        const entriesForAnalysis = filteredEntries.map(entry => ({
            text: entry.text
        }));
        
        // Call backend NLP service
        const response = await fetch('https://emotion-dashboard-1-6kn0.onrender.com/nlp-insights', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                entries: entriesForAnalysis,
                team: selectedTeam
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to analyze sentiment');
        }
        
        const data = await response.json();
        
        if (data.status === 'success') {
            displayNLPResults(data);
        } else {
            throw new Error(data.message || 'Analysis failed');
        }
        
    } catch (error) {
        console.error('Error analyzing sentiment:', error);
        showErrorState(error.message);
    }
}

// Show loading state
function showLoadingState() {
    document.getElementById('insights-container').innerHTML = `
        <div class="loading">
            <div class="loading-spinner"></div>
            <p>Analyzing sentiment and generating insights...</p>
        </div>
    `;
}

// Show error state
function showErrorState(message) {
    document.getElementById('insights-container').innerHTML = `
        <div class="loading">
            <div style="font-size: 3rem; margin-bottom: 20px;">❌</div>
            <p>Error: ${message}</p>
            <p style="font-size: 0.9rem; opacity: 0.7;">Please try again or check if the backend is running.</p>
        </div>
    `;
}

// Display NLP results
function displayNLPResults(data) {
    const { team_analysis, summary_insights } = data;
    
    // Update sentiment chart
    updateSentimentChart(team_analysis);
    
    // Update sentiment meter
    updateSentimentMeter(team_analysis);
    
    // Update emotion grid
    updateEmotionGrid(team_analysis);
    
    // Display insights
    displayInsights(summary_insights);
}

// Update sentiment chart
function updateSentimentChart(teamAnalysis) {
    const sentiment = teamAnalysis.team_sentiment;
    const polarity = sentiment.average_polarity;
    
    let positiveCount = 0, neutralCount = 0, negativeCount = 0;
    
    // This is a simplified approach - in a real implementation, you'd have individual sentiment data
    if (polarity > 0.1) {
        positiveCount = 70;
        neutralCount = 20;
        negativeCount = 10;
    } else if (polarity < -0.1) {
        positiveCount = 10;
        neutralCount = 20;
        negativeCount = 70;
    } else {
        positiveCount = 30;
        neutralCount = 50;
        negativeCount = 20;
    }
    
    sentimentChart.data.datasets[0].data = [positiveCount, neutralCount, negativeCount];
    sentimentChart.update('active');
}

// Update sentiment meter
function updateSentimentMeter(teamAnalysis) {
    const sentiment = teamAnalysis.team_sentiment;
    const polarity = sentiment.average_polarity;
    const overallMood = sentiment.overall_mood;
    
    document.getElementById('polarity-score').textContent = polarity.toFixed(3);
    
    const overallElement = document.getElementById('overall-sentiment');
    overallElement.textContent = overallMood.charAt(0).toUpperCase() + overallMood.slice(1);
    
    // Update color based on sentiment
    overallElement.className = 'sentiment-value';
    if (overallMood === 'positive') {
        overallElement.classList.add('sentiment-positive');
    } else if (overallMood === 'negative') {
        overallElement.classList.add('sentiment-negative');
    } else {
        overallElement.classList.add('sentiment-neutral');
    }
}

// Update emotion grid
function updateEmotionGrid(teamAnalysis) {
    const emotionGrid = document.getElementById('emotion-grid');
    const commonEmotions = teamAnalysis.common_emotions;
    
    if (commonEmotions.length === 0) {
        emotionGrid.innerHTML = '<div class="loading">No specific emotions detected</div>';
        return;
    }
    
    const emotionHTML = commonEmotions.map(([emotion, count]) => `
        <div class="emotion-card">
            <div class="emotion-name">${emotion.charAt(0).toUpperCase() + emotion.slice(1)}</div>
            <div class="emotion-count">${count}</div>
        </div>
    `).join('');
    
    emotionGrid.innerHTML = emotionHTML;
}

// Display insights
function displayInsights(insights) {
    const insightsContainer = document.getElementById('insights-container');
    
    if (insights.length === 0) {
        insightsContainer.innerHTML = `
            <div class="loading">
                <div style="font-size: 3rem; margin-bottom: 20px;">💡</div>
                <p>No specific insights available.</p>
            </div>
        `;
        return;
    }
    
    const insightsHTML = insights.map((insight, index) => `
        <div class="insight-item">
            <div class="insight-title">Insight ${index + 1}</div>
            <div class="insight-description">${insight}</div>
        </div>
    `).join('');
    
    insightsContainer.innerHTML = insightsHTML;
}

// Export functions for global access
window.analyzeTeamSentiment = analyzeTeamSentiment;