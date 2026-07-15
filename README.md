# ✨ Skincare & Haircare Advisor Agent

An **agentic AI-powered skincare and haircare advisor** that delivers personalized routines and product recommendations through intelligent multi-agent reasoning.

Built with **React, FastAPI, and Google's Gemini API**, this application uses AI agents and tool integrations to analyze user preferences, recommend products, and generate customized skincare and haircare routines.

---

## 🌟 Overview

Finding the right skincare and haircare products can be overwhelming. With thousands of products available, users often struggle to identify products that match their skin type, hair type, concerns, allergies, and preferences.

The Skincare & Haircare Advisor Agent solves this by providing a conversational AI experience that learns about the user and creates personalized recommendations.

Instead of relying on a single chatbot prompt, this project uses an **agentic AI architecture** where specialized agents collaborate to complete different tasks.

---

## 🚀 Features

### 💬 Personalized AI Consultation
- Conversational interface powered by Gemini API
- Extracts user information from natural language
- Maintains user context throughout interactions

### 🧴 Product Recommendations
- Recommends skincare and haircare products based on:
  - Skin type
  - Hair type
  - Concerns
  - Allergies
  - Preferences

### 🌞 Personalized Routines
Generates customized:
- Morning skincare routines
- Evening skincare routines
- Morning haircare routine
- Evening haircare routine

### 🔍 Ingredient Conflict Checker
- Checks ingredient compatibility
- Helps users identify potential ingredient conflicts before using products together

### 📊 User Profile Dashboard
Displays:
- Skin profile
- Hair profile
- Recommended products
- Personalized routines

---

# 🤖 Agent Architecture

## Intake Agent
Responsible for understanding the user's needs and extracting structured information.

Tasks:
- Identify skin type
- Identify hair type
- Extract concerns
- Store allergies/preferences
- Update user profile

---

## Recommendation Agent
Responsible for generating personalized recommendations.

Tasks:
- Search product database
- Perform ingredient safety checks
- Recommend products
- Generate skincare and haircare routines

---

# 🛠️ Tech Stack

## Frontend
- React
- Vite
- Tailwind CSS
- JavaScript

## Backend
- Python
- FastAPI

## AI
- Google Gemini API
- Agentic AI workflows
- Prompt engineering
- Tool calling

## Other Tools
- Git
- REST APIs
- JSON-based product database

---

# 📸 Screenshots

### AI Recommendation Chat
Personalized recommendations generated based on user information.
<img width="1710" height="843" alt="Screenshot 2026-07-14 at 11 11 26 PM" src="https://github.com/user-attachments/assets/e2e0711e-7ae0-4a00-9dd1-eb4342126dac" />

### User Dashboard
Dynamic profile and routine tracking.
<img width="1710" height="836" alt="Screenshot 2026-07-14 at 11 11 39 PM" src="https://github.com/user-attachments/assets/f149e487-d077-4721-b4d0-8efd3413b2ef" />

### Ingredient Conflict Checker
AI-powered ingredient compatibility analysis.
<img width="1710" height="844" alt="Screenshot 2026-07-14 at 11 11 55 PM" src="https://github.com/user-attachments/assets/150db260-13c6-490c-bb10-5681a14c15f4" />

---

# 🔮 Future Improvements

## Improved User Experience
- More visually structured AI responses
- Ingredient highlights and explanations
- Better product recommendation cards
- More interactive routine displays

## Enhanced Dashboard
Future dashboard improvements include:
- Routine tracking
- Saved products
- Progress monitoring
- Ingredient information

## E-Commerce Integration
A future goal is transforming the application into an end-to-end skincare and haircare platform where users can:
- Discover products
- Receive AI recommendations
- Purchase products directly through the platform

---

## How to Run

1. Clone this repository.

2. Create a Gemini API key from Google AI Studio.

3. Create a `.env` file in the project root and add your API key:

   GEMINI_API_KEY=your_api_key_here

4. Start the backend by navigating to the `backend` directory and running:

   ../venv/bin/python -m uvicorn main:app --reload

5. In a new terminal, navigate to the `frontend` directory and start the React app:

   npm run dev

6. Open the local URL shown in the terminal to use the application.
   
