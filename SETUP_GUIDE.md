# 🛠️ MediaMind AI - Setup & Installation Guide

This guide will walk you through setting up the MediaMind AI platform on your local machine.

## ✅ Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.9+**: [Download Python](https://www.python.org/downloads/)
*   **Git**: [Download Git](https://git-scm.com/downloads)
*   **Google Gemini API Key**: Get one from [Google AI Studio](https://aistudio.google.com/)

---

## 📥 Installation Steps

### 1. Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/Rasheduzzaman-Rochi/AI-Media-Platform.git
cd AI-Media-Platform
```

### 2. Backend Setup

It is recommended to use a virtual environment to manage dependencies.

**Create and Activate Virtual Environment:**

*   **macOS/Linux:**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
*   **Windows:**
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

**Install Dependencies:**

Navigate to the backend folder and install the required packages:

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configuration (.env)

You need to configure your API key for the AI features to work.

1.  Create a file named `.env` in the **root** directory (or inside `backend/` depending on where you run the command, but usually root is best if using `python-dotenv`).
    *   *Note: The current setup loads from the environment. Ensure the variable is set.*
2.  Add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
```

### 4. Run the Backend Server

From the `backend/` directory, start the FastAPI server:

```bash
uvicorn main:app --reload
```

You should see output indicating the server is running at `http://127.0.0.1:8000`.

**⚠️ Important:** Keep this terminal window **OPEN**. If you close it, the backend will stop, and the AI features will not work.

### 5. Verify Backend Connection

Before starting the frontend, ensure the backend is reachable:

1.  Open your browser and visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)
    *   ✅ You should see: `{"status": "MediaMind Backend Running"}`
2.  (Optional) Visit the Interactive API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    *   This allows you to test endpoints directly from the browser.

---

## 🖥️ Running the Frontend

The frontend is built with standard HTML/JS and uses React via CDN, so no build step is required.

### Option A: Direct File Open (Simplest)
Simply navigate to the `frontend/` folder in your file explorer and double-click `index.html`.

### Option B: Live Server (Recommended)
If you use VS Code, install the **Live Server** extension.
1.  Right-click `frontend/index.html`.
2.  Select **"Open with Live Server"**.

This provides hot-reloading and a better development experience.

---

## 🧪 Verification

To verify everything is working:

1.  Open the dashboard (`index.html`).
2.  Click on **"Translate"** in the sidebar.
3.  Enter "Hello World" and select "Spanish".
4.  Click **Translate**.
5.  If you see "Hola Mundo", your backend and AI connection are working perfectly! 🎉

---

## ❓ Troubleshooting

**Issue: "Fetch error" or "Network Error"**
*   Ensure the backend server is running (`uvicorn main:app --reload`).
*   Check if the backend URL in the frontend files matches your local server (default: `http://127.0.0.1:8000`).

**Issue: "Quota exceeded"**
*   This means you've hit the rate limit for the Gemini API. Wait a minute and try again, or check your Google AI Studio quota.

**Issue: Database errors**
*   Delete the `.mediamind.db` (or `mediamind.db`) file in the `backend/` folder and restart the server. It will be recreated automatically.

