# NSRIT Academic Intelligence & Visual Dashboard

> **Top-Tier Academic Operations Engine & AI-Powered Student Console**  
> Built with Flask, Playwright, SQLite, HTML5 2D Canvas, and Google Gemini 2.5 Flash.

---

## Key Features

- **Cosmic Astrophysics Intro Canvas Engine**: 60 FPS HTML5 2D Canvas intro sequence simulating planetary orbits, core supernova explosions, particle disintegrations, and golden perimeter border convergence.
- **Resilient Multi-User Session Scraper**: Headless Playwright integration supporting automatic ASP.NET portal login, fail-safe menu locator fallbacks, and multi-user database session isolation.
- **SQLite Academic Record Caching**: Single-source-of-truth local storage for student profiles, subject attendance ledgers, SGPA history, and internal marks.
- **Gemini 2.5 Flash AI Assistant**: Context-aware academic chat engine supporting attendance leave impact simulation, course code resolution, and formatted markdown timetable grid responses.
- **Veloretti Luxury UI Design System**: Sleek `#0D0E12` slate canvas, Champagne Gold `#D4AF37` accents, interactive dual-tone progress bars, and Chart.js SGPA trend lines.

---

## System Architecture

```
+-------------------------------------------------------------------+
|                        FRONTEND DASHBOARD                         |
|  - HTML5 2D Canvas Supernova Intro                                |
|  - Veloretti Luxury Dark Theme (#0D0E12 / #D4AF37)                |
|  - Chart.js SGPA Trend & Marked.js Timetable Render               |
+---------------------------------+---------------------------------+
                                  | HTTP / JSON API
+---------------------------------v---------------------------------+
|                       FLASK BACKEND ENGINE                        |
|  - Auth & Multi-User Session Router (/api/login, /api/data)       |
|  - AI Assistant Handler (/api/chat)                               |
|  - Data Synchronization Controller (/api/sync)                    |
+-------------------+-----------------------------+-----------------+
                    |                             |
+-------------------v----------+       +----------v------------------+
|    PLAYWRIGHT SCRAPER        |       |   GOOGLE GEMINI 2.5 FLASH   |
| - Headless Chromium          |       | - System Instruction Context|
| - ASP.NET Navigation         |       | - Attendance Leave Model    |
| - Attendance & Marks Parser  |       | - Timetable Markdown Matrix |
+-------------------+----------+       +-----------------------------+
                    |
+-------------------v-----------------------------------------------+
|                      SQLITE CACHE DATABASE                        |
| - Student Records, Subject Attendance, SGPA, & Internal Ledger    |
+-------------------------------------------------------------------+
```

---

## Project Structure

```text
Smart_Attendance/
├── app.py                      # Flask Application Server & API Routes
├── requirements.txt            # Python Dependencies
├── .env.example                # Environment Variable Template
├── .gitignore                  # Production Build & Secret Exclusion Rules
├── data/
│   ├── student_cache.db        # SQLite Student Profile & Attendance Store
│   └── timetable.json          # Master Department Timetable Schedule
├── src/
│   ├── auth.py                 # Playwright Portal Authentication Handler
│   ├── scraper.py              # Full Scrape Workflow Coordinator
│   ├── parser.py                # HTML Report BeautifulSoup Parser
│   ├── db.py                    # SQLite Database CRUD & Schema Manager
│   ├── ai_service.py           # Gemini 2.5 Flash Academic Assistant
│   └── scrapers/
│       ├── attendance.py       # Attendance Ledger Scraper
│       └── marks.py            # Internal & External Marks Scraper
└── templates/
    └── index.html              # Single-Page App (Canvas Intro, Dashboard, Chat)
```

---

## Installation & Setup Guide

### 1. Clone Repository & Setup Virtual Environment

```bash
git clone https://github.com/your-username/Smart_Attendance.git
cd Smart_Attendance

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 2. Install Dependencies & Playwright Browsers

```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Set the values inside `.env`:
```env
COLLEGE_URL=https://webprosindia.com/nsrit/Default.aspx?ReturnUrl=%2Fnsrit%2Fmain.aspx
COLLEGE_USERNAME=your_roll_number
COLLEGE_PASSWORD=your_portal_password
GEMINI_API_KEY=your_google_gemini_api_key
PORT=5000
```

### 4. Run Application Server

```bash
python app.py
```

Access the dashboard at `http://127.0.0.1:5000/`.

---

## API Endpoints Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/login` | Authenticates credentials with ASP.NET portal and scrapes profile data. |
| `GET` | `/api/data` | Returns current cached student record from SQLite. |
| `POST` | `/api/chat` | Queries Gemini 2.5 Flash for leave impact analysis and timetable grids. |
| `POST` | `/api/sync` | Force-resynchronizes student attendance & marks ledger with portal. |

---

## License

MIT License. Designed for student productivity and visual academic analytics.
