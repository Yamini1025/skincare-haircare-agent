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

(Add screenshots here)

### AI Recommendation Chat
Personalized recommendations generated based on user information.

### User Dashboard
Dynamic profile and routine tracking.

### Ingredient Conflict Checker
AI-powered ingredient compatibility analysis.

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
