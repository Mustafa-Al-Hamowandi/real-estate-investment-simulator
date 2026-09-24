# Real Estate Investment Simulator

A full-stack Flask web application that lets users buy, sell, and manage a simulated real estate investment portfolio. Features AI-powered property valuations, real-time weather impact analysis, and an interactive market crash simulator.

This is a portfolio piece built as a class project. Market comparables and trend data are simulated for demonstration purposes rather than pulled from a live third-party source.

Claude AI was used throughout development to help guide implementation decisions and detect/debug errors, in line with the course's AI usage policy for this entry-level class.

---

## Features

- **User Authentication** — separate investor and admin roles with secure login/registration (Flask-Login)
- **Property Marketplace** — browse and purchase available properties
- **AI-Powered Valuations** — property price predictions generated via NVIDIA's LLM API, including a Buy/Sell/Hold recommendation and confidence score
- **Portfolio Management** — track owned properties, purchase history, and return on investment (ROI)
- **Portfolio Optimizer** — AI-driven suggestions for optimizing an investor's holdings
- **Weather Impact Analysis** — shows how local weather conditions may affect a property's market value
- **Market Analytics Dashboard** — interactive charts (Chart.js) showing price trends, interest rate history, and top-performing cities
- **Market Crisis Simulator** — run economic crash scenarios against your portfolio and see projected impact over time
- **Admin Dashboard** — manage properties, users, and market configuration
- **Video Tutorials** — upload and view training videos

## Tech Stack

- **Backend:** Python, Flask, Flask-Login, Flask-SQLAlchemy
- **Database:** SQLite
- **AI Integration:** NVIDIA API (LLM-based property valuation and recommendations)
- **Frontend:** HTML5, Bootstrap 5, JavaScript, Chart.js
- **Other:** python-dotenv for environment variable management

## Screenshots

Login Page
<img width="1346" height="586" alt="image" src="https://github.com/user-attachments/assets/617e15fd-7a09-41d7-a0f9-d868ee5227a6" />
Admin Dashboard
<img width="1343" height="583" alt="image" src="https://github.com/user-attachments/assets/71309d3d-1a7d-4565-813e-6947f29babd8" />
Admin Dashboard 2
<img width="1339" height="597" alt="image" src="https://github.com/user-attachments/assets/87198f92-3047-4983-908b-87053f70eb37" />
Manage Properties
<img width="1342" height="590" alt="image" src="https://github.com/user-attachments/assets/a5a33338-2765-4a49-ba15-f177ed8aa27f" />
Add New Property
<img width="1340" height="581" alt="image" src="https://github.com/user-attachments/assets/491500e4-dc39-4dd2-abd3-9b26db874786" />
Manage Users
<img width="1338" height="582" alt="image" src="https://github.com/user-attachments/assets/1a8f5337-526d-4e53-88d2-1b43cb3c4782" />
Tutorials Page
<img width="1352" height="589" alt="image" src="https://github.com/user-attachments/assets/af968336-87a1-43de-bdf2-38a0f04aec25" />
Tutorials Page 2
<img width="1312" height="585" alt="image" src="https://github.com/user-attachments/assets/0e7da49a-5663-4e83-a1b6-a283a7499152" />
Upload Video
<img width="1339" height="592" alt="image" src="https://github.com/user-attachments/assets/415b0aca-7c2b-4f92-b975-136a5ecea9b5" />
Investor Dashboard
<img width="1334" height="584" alt="image" src="https://github.com/user-attachments/assets/39f400ec-47a8-472c-a891-1fd492041c21" />
Investor Dashboard 2
<img width="1348" height="589" alt="image" src="https://github.com/user-attachments/assets/f74297ce-f392-4cf1-b754-7f0b503a5a6a" />
Property Marketplace
<img width="1348" height="591" alt="image" src="https://github.com/user-attachments/assets/546ac20a-ed2e-4874-a2a2-5296e3f832b8" />
Property Marketplace 2
<img width="1336" height="590" alt="image" src="https://github.com/user-attachments/assets/bd6b91cc-e343-49fb-88c6-65ae9a147ec4" />
Property Analysis
<img width="1347" height="580" alt="image" src="https://github.com/user-attachments/assets/cbc0653b-ab9e-4491-862e-f50a423dce41" />
Property Analysis 2
<img width="1334" height="585" alt="image" src="https://github.com/user-attachments/assets/ed602960-f94a-4284-9041-c14826ba9655" />
My Portfolio
<img width="1347" height="584" alt="image" src="https://github.com/user-attachments/assets/884eeaee-ad5d-4040-b2aa-0d377d856b98" />
AI Advisor
<img width="1351" height="586" alt="image" src="https://github.com/user-attachments/assets/e489c4fe-f637-45a0-be68-02d951646b90" />
AI Advisor 2
<img width="1306" height="597" alt="image" src="https://github.com/user-attachments/assets/eef70c42-852e-40b1-998f-ffb7f53676da" />
AI Advisor 3
<img width="1246" height="521" alt="image" src="https://github.com/user-attachments/assets/9079e510-c35e-4cb6-824a-e0f4d3164c08" />
AI Portfolio Optimizer
<img width="1344" height="590" alt="image" src="https://github.com/user-attachments/assets/5fa81fe8-539a-4b37-97d4-54e40d3fb002" />
AI Portfolio Optimizer 2
<img width="1304" height="581" alt="image" src="https://github.com/user-attachments/assets/e9ab04d3-d15c-4dcc-8477-041d92e11d2e" />
AI Portfolio Optimizer 3
<img width="1197" height="486" alt="image" src="https://github.com/user-attachments/assets/3910d6a1-da8c-47d1-b26d-56f0be51435b" />
Market Analytics
<img width="1320" height="597" alt="image" src="https://github.com/user-attachments/assets/657d42c4-6902-49a1-9657-90151197d7fe" />
Market Analytics 2
<img width="1255" height="598" alt="image" src="https://github.com/user-attachments/assets/f6dc3c45-2d36-4421-834e-a2b16895206f" />
Market Analytics 3
<img width="1224" height="557" alt="image" src="https://github.com/user-attachments/assets/03713515-1563-42e6-b3cf-ce8c606913c5" />
Market Crisis Simulator
<img width="1333" height="572" alt="image" src="https://github.com/user-attachments/assets/19ec034e-ddfd-46e8-b8d2-4e8fd88f3a30" />
Market Crisis Simulator 2
<img width="1237" height="594" alt="image" src="https://github.com/user-attachments/assets/a7945ece-04c9-433d-8274-fcefc7675973" />
Simulation Results
<img width="1220" height="598" alt="image" src="https://github.com/user-attachments/assets/a6586a77-ae84-43dd-8c2c-76dbc76aa73d" />
Simulation Results 2
<img width="1197" height="570" alt="image" src="https://github.com/user-attachments/assets/2827cb38-a50f-437c-b37a-b7142a756f7d" />






## Setup Instructions

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it and install dependencies: `pip install -r requirements.txt`
4. Create a `.env` file in the project root with:
   ```
   NVIDIA_API_KEY=your_nvidia_api_key_here
   WEATHER_API_KEY=your_weather_api_key_here
   SECRET_KEY=any_random_string
   ```
5. Run the app: `python app.py`
6. Open `http://localhost:5000` in your browser

## Disclaimer

This is an educational project built for a Python web development course. It is not a real financial tool and should not be used to make actual investment decisions.
