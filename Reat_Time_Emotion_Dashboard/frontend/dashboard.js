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

// Initial mood counts
let moodCounts = [0, 0, 0, 0, 0];

// Chart Setup
const ctx = document.getElementById("moodChart").getContext("2d");
const moodChart = new Chart(ctx, {
  type: "bar",
  data: {
    labels: ["😞", "😐", "🙂", "😊", "😁"],
    datasets: [{
      label: "Mood Count",
      data: moodCounts,
      backgroundColor: ["#f44336", "#ff9800", "#ffc107", "#4caf50", "#2196f3"]
    }]
  },
  options: {
    scales: {
      y: { beginAtZero: true }
    }
  }
});

// Listen to mood_entries in real-time
db.ref("mood_entries").on("value", (snapshot) => {
  let moodCounts = [0, 0, 0, 0, 0];
  let total = 0;
  let count = 0;

  snapshot.forEach((child) => {
    const mood = child.val().mood;
    if (mood >= 1 && mood <= 5) {
      moodCounts[mood - 1]++;
      total += mood;
      count++;
    }
  });

  const avgMood = count > 0 ? (total / count).toFixed(2) : 0;

  // Chart update code here

  // 🔔 Discord Alert
  if (avgMood < 2.5) {
    alert("⚠️ Team morale is low! Average mood: " + avgMood);

    fetch("https://discord.com/api/webhooks/1387057201931223110/zjX1FEcTkiErkZwAKKcANFmwgoFhnT2fov1qu9u9EFnu_sMp2CuFB83Z1_ygcOGDWolr", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        content: `⚠️ **Mood Alert**: Team morale is low!\nAverage mood is ${avgMood}`
      })
    })
    .then(res => console.log("📤 Alert sent to Discord"))
    .catch(err => console.error("❌ Discord error:", err));
  }
});

