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
const database = firebase.database();

function submitMood(score) {
  const moodData = {
    mood: score,
    timestamp: Date.now()
  };

  database.ref("mood_entries").push(moodData)
    .then(() => {
      document.getElementById("status").innerText = "✅ Mood submitted!";
    })
    .catch((error) => {
      console.error("Error submitting mood:", error);
      document.getElementById("status").innerText = "❌ Error submitting mood.";
    });
}
