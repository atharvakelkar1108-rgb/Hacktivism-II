# 🌐 CivicTwin X — AI-Powered Digital Twin for Smart Cities

> "AI-Powered Digital Twin • Blockchain-Verified • Real-Time Urban Intelligence"

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20App-lightgrey?logo=flask)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 📌 About the Project

**CivicTwin X** is an AI-powered smart city digital twin platform built for the **Hacktivism Hackathon**. It simulates and analyzes real-time urban health metrics — traffic, pollution, power usage, water consumption, and citizen complaints — to help city administrators make data-driven decisions.

The platform combines machine learning predictions, blockchain-inspired data integrity, real-time environmental APIs, and citizen reporting into a single unified dashboard.

---

## ✨ Features

- 🏙️ **City Health Analysis** — Input urban metrics and get AI-powered civic stress scores
- 📍 **Location Intelligence** — Real-time air quality and weather data via Open-Meteo API
- 📝 **Citizen Reporting** — Submit civic issues with urgency levels
- 🔗 **Blockchain Data Integrity** — Tamper-proof snapshot logging (simulated)
- 📊 **Historical Data** — View past 50 city snapshots and trends
- 🤖 **AI Trend Prediction** — CNN-based predictor forecasts future urban stress
- 🌐 Real-time environmental data (PM2.5, ozone, CO, temperature, humidity)

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.13, Flask |
| Database | SQLite3 |
| ML Model | scikit-learn (`model.pkl`) |
| Frontend | HTML, CSS, JavaScript |
| APIs | Open-Meteo Air Quality API, Open-Meteo Weather API |
| Data Integrity | Blockchain-inspired hashing (simulated) |
| Utilities | `utils.py`, `contextlib`, `datetime`, `sqlite3` |

---

## 📁 Project Structure

```
Hacktivism-II/
│
└── CivicTwinX/
    ├── app.py                  # Flask app — main entry point
    ├── utils.py                # Helper functions and utilities
    ├── model.pkl               # Trained ML model
    │
    ├── static/
    │   ├── city.json           # City data configuration
    │   ├── script.js           # Frontend JavaScript
    │   ├── style.css           # Styling
    │   └── voice.js            # Voice interaction support
    │
    └── templates/
        └── index.html          # Main frontend template
```

---

## 🚀 How to Run

### Step 1 — Clone the Repository
```bash
git clone https://github.com/atharvakelkar1108-rgb/Hacktivism-II.git
cd Hacktivism-II/CivicTwinX
```

### Step 2 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Set Environment Variable (optional but recommended)
```bash
# Windows
set SECRET_KEY=your_secret_key_here

# Mac/Linux
export SECRET_KEY=your_secret_key_here
```

### Step 4 — Run the App
```bash
python app.py
```

### Step 5 — Open in Browser
```
http://127.0.0.1:5000
```

---

## 🧠 How It Works

1. **City Health Input** — User enters traffic, pollution, power usage, water use, and complaints (0–100 scale)
2. **AI Analysis** — Weighted civic stress score is calculated and AI predicts future trends
3. **Status Verdict** — System returns one of 5 alert levels: Optimal, Low, Medium, High, Critical
4. **Location Scan** — Real-time environmental data fetched based on user's GPS coordinates
5. **Data Storage** — Every analysis is stored in SQLite and logged to the blockchain-inspired chain
6. **Citizen Reports** — Users can submit local civic issues with urgency ratings

---

## 📊 Alert Levels

| Civic Stress Score | Status |
|-------------------|--------|
| 0 – 25 | 🌿 Excellent — City is thriving |
| 25 – 45 | 🔵 Stable — Maintain current policies |
| 45 – 65 | 🟡 Moderate — Take corrective actions |
| 65 – 80 | 🔴 High Stress — Immediate intervention needed |
| 80+ | 🚨 Critical — Emergency response required |

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙋 Author

Built with ❤️ for the **Hacktivism Hackathon** to reimagine smart city management using AI.

Feel free to ⭐ star the repo if you found it useful!
