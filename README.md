# 🚀 MediaMind AI - Enterprise Media Intelligence Suite

MediaMind AI is a comprehensive, full-stack platform designed to revolutionize media content creation and analysis. Powered by **Google Gemini 2.5 Flash**, it offers a suite of intelligent tools for sentiment analysis, content recommendation, real-time translation, safety moderation, trend forecasting, and automated summarization.

## ✨ Key Features

### 1. **Sentiment Analysis** 📊
*   **Real-time Emotion Detection:** Instantly analyzes text to determine sentiment (Positive, Negative, Neutral).
*   **Deep Insights:** Provides confidence scores and tone analysis (e.g., Enthusiastic, Critical).
*   **UI:** Interactive dashboard with visual feedback.

### 2. **Smart Feed Recommendations** 📰
*   **AI-Curated Content:** Generates personalized content strategies and tag suggestions.
*   **Category Filtering:** Tailored recommendations for Tech, Sports, Politics, Finance, and more.
*   **Visual Previews:** engaging card-based layout.

### 3. **Live Translator** 🌍
*   **Multi-Language Support:** Seamlessly translates between English and 7+ languages including Bengali, Spanish, French, Hindi, German, Japanese, and Arabic.
*   **Context-Aware:** Preserves the original tone and meaning of the message.
*   **Instant Results:** Low-latency translation for real-time workflows.

### 4. **Safety Shield** 🛡️
*   **Content Moderation:** Automatically flags hate speech, harassment, and policy violations.
*   **Fact-Checking:** Cross-references claims to identify potential misinformation.
*   **Safety Scores:** Provides a clear safety rating for reviewed content.

### 5. **Trend Analytics** 📈
*   **Viral Prediction:** Forecasts potential viral topics using historical data.
*   **Engagement Velocity:** Visualizes growth trends over time with interactive charts.
*   **Demographic Insights:** Breaks down audience segments (e.g., Gen Z, Tech Professionals).

### 6. **Auto Summarizer** 📝
*   **Smart Compression:** Condenses long articles and documents into concise executive summaries.
*   **Key Point Extraction:** Automatically identifies and lists the most important bullet points.
*   **Efficiency:** Drastically reduces reading time while retaining core information.

## 🛠️ Tech Stack

### Backend
*   **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Python) - High-performance, easy-to-use web framework.
*   **AI Engine:** Google Gemini 1.5/2.5 Flash - State-of-the-art generative AI.
*   **Database:** SQLite (via SQLAlchemy) - Lightweight, serverless database for activity logging.
*   **Server:** Uvicorn - ASGI web server implementation.

### Frontend
*   **Core:** HTML5, JavaScript (ES6+)
*   **Library:** React 18 (via CDN) - For building interactive user interfaces.
*   **Styling:** Tailwind CSS (via CDN) - Utility-first CSS framework for rapid UI development.
*   **Icons:** Custom SVG & Emoji-based icons.

## 📂 Project Structure

```
AI-Media-Platform/
├── backend/
│   ├── routers/          # API endpoints for each feature (f1-f6)
│   ├── database.py       # SQLite database connection & models
│   ├── main.py           # FastAPI entry point & CORS configuration
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── index.html        # Main Dashboard
│   ├── f1_sentiment.html # Sentiment Analysis UI
│   ├── f2_recommend.html # Smart Feed UI
│   ├── f3_translate.html # Live Translator UI
│   ├── f4_safety.html    # Safety Shield UI
│   ├── f5_insights.html  # Trend Analytics UI
│   └── f6_summary.html   # Auto Summarizer UI
├── .env                  # Environment variables (API Keys)
├── README.md             # Project documentation
└── SETUP_GUIDE.md        # Detailed setup instructions
```

## 🚀 Quick Start

1.  **Backend:** Navigate to `backend/`, install requirements, and run `uvicorn main:app --reload`.
2.  **Frontend:** Open `frontend/index.html` in your browser.

For detailed step-by-step instructions, please refer to the [SETUP_GUIDE.md](SETUP_GUIDE.md).

## 📄 License

This project is open-source and available under the MIT License.
