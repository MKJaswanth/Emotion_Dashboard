import re
import nltk
from textblob import TextBlob
from collections import Counter
import json
from datetime import datetime, timedelta

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

class NLPService:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.emotion_keywords = {
            'happy': ['happy', 'joy', 'excited', 'great', 'wonderful', 'amazing', 'fantastic', 'love', 'enjoy', 'pleased'],
            'sad': ['sad', 'depressed', 'unhappy', 'miserable', 'upset', 'disappointed', 'heartbroken', 'lonely'],
            'angry': ['angry', 'furious', 'mad', 'irritated', 'annoyed', 'frustrated', 'rage', 'hate'],
            'anxious': ['anxious', 'worried', 'nervous', 'stressed', 'tense', 'afraid', 'scared', 'fear'],
            'tired': ['tired', 'exhausted', 'fatigued', 'drained', 'burned out', 'overwhelmed'],
            'confident': ['confident', 'proud', 'accomplished', 'successful', 'achieved', 'capable'],
            'confused': ['confused', 'uncertain', 'unsure', 'doubtful', 'puzzled', 'lost']
        }
        
        self.theme_keywords = {
            'work': ['work', 'project', 'deadline', 'meeting', 'boss', 'colleague', 'office', 'job'],
            'study': ['study', 'exam', 'test', 'assignment', 'homework', 'class', 'lecture', 'course'],
            'health': ['health', 'sick', 'pain', 'doctor', 'medicine', 'exercise', 'diet', 'sleep'],
            'relationship': ['friend', 'family', 'partner', 'relationship', 'love', 'breakup', 'marriage'],
            'money': ['money', 'finance', 'budget', 'expense', 'salary', 'payment', 'bills'],
            'technology': ['computer', 'phone', 'internet', 'software', 'app', 'device', 'tech'],
            'weather': ['weather', 'rain', 'sunny', 'cold', 'hot', 'temperature', 'climate']
        }

    def analyze_text(self, text):
        """Comprehensive text analysis"""
        if not text or len(text.strip()) < 3:
            return self._empty_analysis()
        
        # Clean text
        cleaned_text = self._clean_text(text)
        
        # Basic sentiment analysis
        sentiment = self._analyze_sentiment(cleaned_text)
        
        # Emotion detection
        emotions = self._detect_emotions(cleaned_text)
        
        # Theme detection
        themes = self._detect_themes(cleaned_text)
        
        # Key insights
        insights = self._generate_insights(cleaned_text, sentiment, emotions, themes)
        
        # Word frequency
        word_freq = self._analyze_word_frequency(cleaned_text)
        
        return {
            'sentiment': sentiment,
            'emotions': emotions,
            'themes': themes,
            'insights': insights,
            'word_frequency': word_freq,
            'text_length': len(text),
            'word_count': len(cleaned_text.split()),
            'timestamp': datetime.now().isoformat()
        }

    def _clean_text(self, text):
        """Clean and normalize text"""
        text = text.lower()
        text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def _analyze_sentiment(self, text):
        """Analyze sentiment using TextBlob"""
        blob = TextBlob(text)
        sentiment = blob.sentiment
        polarity = sentiment.polarity  # type: ignore
        subjectivity = sentiment.subjectivity  # type: ignore
        
        if polarity > 0.3:
            sentiment_category = 'positive'
        elif polarity < -0.3:
            sentiment_category = 'negative'
        else:
            sentiment_category = 'neutral'
        
        if abs(polarity) > 0.7:
            intensity = 'strong'
        elif abs(polarity) > 0.3:
            intensity = 'moderate'
        else:
            intensity = 'weak'
        
        return {
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3),
            'category': sentiment_category,
            'intensity': intensity,
            'description': self._get_sentiment_description(polarity, subjectivity)
        }

    def _get_sentiment_description(self, polarity, subjectivity):
        if polarity > 0.7:
            return "Very positive and enthusiastic"
        elif polarity > 0.3:
            return "Generally positive"
        elif polarity > -0.1:
            return "Neutral or slightly positive"
        elif polarity > -0.3:
            return "Slightly negative"
        elif polarity > -0.7:
            return "Generally negative"
        else:
            return "Very negative or distressed"

    def _detect_emotions(self, text):
        words = word_tokenize(text)
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for word in words if word in keywords)
            if score > 0:
                emotion_scores[emotion] = score
        
        sorted_emotions = sorted(emotion_scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'primary_emotion': sorted_emotions[0][0] if sorted_emotions else 'neutral',
            'emotion_scores': emotion_scores,
            'top_emotions': [emotion for emotion, score in sorted_emotions[:3]]
        }

    def _detect_themes(self, text):
        words = word_tokenize(text)
        theme_scores = {}
        
        for theme, keywords in self.theme_keywords.items():
            score = sum(1 for word in words if word in keywords)
            if score > 0:
                theme_scores[theme] = score
        
        sorted_themes = sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'primary_theme': sorted_themes[0][0] if sorted_themes else 'general',
            'theme_scores': theme_scores,
            'top_themes': [theme for theme, score in sorted_themes[:3]]
        }

    def _generate_insights(self, text, sentiment, emotions, themes):
        insights = []
        
        if sentiment['category'] == 'negative' and sentiment['intensity'] == 'strong':
            insights.append("This person may need immediate support or intervention")
        elif sentiment['category'] == 'negative':
            insights.append("Consider checking in with this person")
        elif sentiment['category'] == 'positive' and sentiment['intensity'] == 'strong':
            insights.append("This person is in a great mood - great time for collaboration")
        
        if 'anxious' in emotions['top_emotions']:
            insights.append("Shows signs of anxiety - may need stress management support")
        if 'tired' in emotions['top_emotions']:
            insights.append("Appears to be experiencing fatigue - consider workload review")
        if 'confident' in emotions['top_emotions']:
            insights.append("Shows confidence - good time for challenging tasks")
        
        if 'work' in themes['top_themes']:
            insights.append("Work-related concerns detected")
        if 'study' in themes['top_themes']:
            insights.append("Academic stress may be present")
        if 'health' in themes['top_themes']:
            insights.append("Health-related issues mentioned")
        
        word_count = len(text.split())
        if word_count > 100:
            insights.append("Detailed response - person is engaged and expressive")
        elif word_count < 20:
            insights.append("Brief response - may need encouragement to share more")
        
        return insights

    def _analyze_word_frequency(self, text):
        words = word_tokenize(text)
        filtered_words = [word for word in words if word not in self.stop_words and len(word) > 2]
        word_freq = Counter(filtered_words)
        top_words = word_freq.most_common(10)
        
        return {
            'top_words': [{'word': word, 'count': count} for word, count in top_words],
            'total_unique_words': len(word_freq)
        }

    def _empty_analysis(self):
        return {
            'sentiment': {
                'polarity': 0,
                'subjectivity': 0,
                'category': 'neutral',
                'intensity': 'weak',
                'description': 'No text to analyze'
            },
            'emotions': {
                'primary_emotion': 'neutral',
                'emotion_scores': {},
                'top_emotions': []
            },
            'themes': {
                'primary_theme': 'general',
                'theme_scores': {},
                'top_themes': []
            },
            'insights': ['No text provided for analysis'],
            'word_frequency': {
                'top_words': [],
                'total_unique_words': 0
            },
            'text_length': 0,
            'word_count': 0,
            'timestamp': datetime.now().isoformat()
        }

    def analyze_team_sentiment(self, text_entries):
        if not text_entries:
            return self._empty_team_analysis()
        
        all_analyses = []
        total_polarity = 0
        total_subjectivity = 0
        
        for entry in text_entries:
            analysis = self.analyze_text(entry.get('text', ''))
            all_analyses.append(analysis)
            total_polarity += analysis['sentiment']['polarity']
            total_subjectivity += analysis['sentiment']['subjectivity']
        
        avg_polarity = total_polarity / len(text_entries)
        avg_subjectivity = total_subjectivity / len(text_entries)
        
        all_emotions = []
        all_themes = []
        all_insights = []
        
        for analysis in all_analyses:
            all_emotions.extend(analysis['emotions']['top_emotions'])
            all_themes.extend(analysis['themes']['top_themes'])
            all_insights.extend(analysis['insights'])
        
        emotion_freq = Counter(all_emotions)
        theme_freq = Counter(all_themes)
        
        return {
            'team_sentiment': {
                'average_polarity': round(avg_polarity, 3),
                'average_subjectivity': round(avg_subjectivity, 3),
                'overall_mood': 'positive' if avg_polarity > 0.1 else 'negative' if avg_polarity < -0.1 else 'neutral'
            },
            'common_emotions': emotion_freq.most_common(5),
            'common_themes': theme_freq.most_common(5),
            'key_insights': list(set(all_insights))[:10],
            'total_entries': len(text_entries),
            'timestamp': datetime.now().isoformat()
        }

    def _empty_team_analysis(self):
        return {
            'team_sentiment': {
                'average_polarity': 0,
                'average_subjectivity': 0,
                'overall_mood': 'neutral'
            },
            'common_emotions': [],
            'common_themes': [],
            'key_insights': ['No text entries to analyze'],
            'total_entries': 0,
            'timestamp': datetime.now().isoformat()
        } 