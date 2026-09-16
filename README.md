# AI-Voice-Based-Insurance-Quoting-Assistant
The application is structured into a production-grade FastAPI backend with LangChain/LangGraph, full technical documentation, and a modern React + Tailwind CSS frontend supporting real-time voice, customer risk profiling, quote calculation, side-by-side policy comparison.

# UC189 - AI Voice-Based Insurance Quoting Assistant

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%2018-61DAFB.svg?style=flat&logo=react)](https://react.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS-38B2AC.svg?style=flat&logo=tailwind-css)](https://tailwindcss.com/)
[![LangGraph](https://img.shields.io/badge/AI%20Orchestration-LangGraph%20%26%20LangChain-orange.svg?style=flat)](https://www.langchain.com/)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB.svg?style=flat&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An enterprise-grade, voice-driven insurance assistant that enables customers to explore coverage plans, compare policies side-by-side, assess actuarial risk factors, calculate personalized premiums, and export official PDF quote proposals through natural spoken conversation.

---

## Table of Contents
- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Detailed Folder Structure](#detailed-folder-structure)
- [Key Features](#key-features)
- [API Endpoints Reference](#api-endpoints-reference)
- [Quick Start Guide](#quick-start-guide)
  - [Prerequisites](#prerequisites)
  - [Environment Configuration](#environment-configuration)
  - [Backend Setup](#backend-setup)
  - [Frontend Setup](#frontend-setup)
  - [Docker Compose Deployment](#docker-compose-deployment)
- [Testing and Verification](#testing-and-verification)
- [Documentation Index](#documentation-index)
- [4-Day Development Roadmap](#4-day-development-roadmap)

---

## Overview

Traditional insurance quoting can be slow, jargon-heavy, and confusing. **UC189** solves this by delivering an autonomous, conversational AI advisor:
- **Natural Voice Interaction**: Speak directly into the microphone or select pre-configured scenario prompts.
- **Dynamic Customer Profiling**: Extracts demographic and medical entities in real time from dialogue.
- **Actuarial Risk Assessment**: Calculates an instant loss probability score (0.00–1.00) and assigns a risk tier.
- **Smart Recommendations**: Evaluates and ranks matching policies based on budget, family size, and coverage goals.
- **Interactive Quoting & Official PDF Export**: Adjust deductibles, term lengths, and riders with live premium calculation, and download a publication-quality PDF proposal.
- **Uniphore Conversational Intelligence**: Continuously evaluates sentiment, acoustic tone, speaking pace (WPM), and biometric confidence.

---

## System Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 FRONTEND (React + Vite)                                │
│  ┌────────────────────┐  ┌─────────────────────┐  ┌─────────────────────────────────┐  │
│  │  Voice Assistant   │  │ Customer Profile &  │  │   Quote Engine & PDF Exporter   │  │
│  │ (Mic / Waveform)   │  │ Risk Assessment     │  │  (Coverage / Deductibles)       │  │
│  └─────────┬──────────┘  └──────────┬──────────┘  └────────────────┬────────────────┘  │
│            │                        │                              │                   │
│  ┌─────────┴──────────┐  ┌──────────┴──────────┐  ┌────────────────┴────────────────┐  │
│  │ Policy Comparison  │  │ AI Recommendations  │  │  Uniphore Analytics Dashboard   │  │
│  └────────────────────┘  └─────────────────────┘  └─────────────────────────────────┘  │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ HTTP REST / WebSockets / Blobs
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│                                BACKEND (FastAPI Gateway)                               │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   voice_api.py   │  │ customer_api.py  │  │  quote_api.py   │  │  recommend_api  │  │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬────────┘  └────────┬────────┘  │
│           └─────────────────────┼─────────────────────┴────────────────────┘           │
│                                 ▼                                                      │
│                   LangGraph Workflow State Machine                                     │
│  START ──> Voice Input ──> Intent Detection ──> Customer Profiling ──> Risk Scoring    │
│    ──> Policy Matching ──> Premium Calculation ──> Quote Output ──> Voice Reply ──> END│
│                                 │                                                      │
│  ┌──────────────────────────────┼──────────────────────────────┐                       │
│  │ LangChain Agents Layer       │ Actuarial & Media Services   │                       │
│  │ • CustomerProfileAgent       │ • PremiumEngine              │                       │
│  │ • QuoteGenerationAgent       │ • WhisperService (STT)       │                       │
│  │ • ComparisonAgent            │ • ElevenLabsService (TTS)    │                       │
│  │ • InsuranceRecomAgent        │ • UniphoreService            │                       │
│  │                              │ • PDFQuoteService (ReportLab)│                       │
│  └──────────────────────────────┴──────────────────────────────┘                       │
│                                 │                                                      │
│  ┌──────────────────────────────▼──────────────────────────────┐                       │
│  │ Data Layer: PostgreSQL / SQLite Auto-Fallback / Azure SQL   │                       │
│  └─────────────────────────────────────────────────────────────┘                       │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Folder Structure

Below is the complete tree layout of the UC189 project with descriptions of every file and directory:

```
UC189/
├── .env                              # Active environment configuration (local defaults)
├── .env.example                      # Template for cloud credentials (Azure, ElevenLabs, Uniphore)
├── .gitignore                        # Git ignore patterns for Python, Node, media, and DB
├── docker-compose.yml                # Multi-container orchestration (FastAPI, React, Postgres, Redis)
├── README.md                         # Complete project documentation & guide
│
├── docs/                             # Engineering and product documentation
│   ├── api-specification.md          # REST API contracts, payloads, and schema definitions
│   ├── architecture.md               # High-level architecture, subsystem details, and data flow
│   ├── demo-script.md                # 10-minute presentation demo script and talk track
│   ├── deployment-guide.md           # Deployment procedures for Azure App Service & Containers
│   └── user-flow.md                  # Customer conversational journey and alternate paths
│
├── backend/                          # FastAPI application, AI agents, and services
│   ├── Dockerfile                    # Containerization specification for backend service
│   ├── requirements.txt              # Pinned Python package dependencies
│   ├── config.py                     # Pydantic BaseSettings loader with environment parsing
│   ├── main.py                       # FastAPI application entrypoint, CORS, and router registration
│   │
│   ├── agents/                       # LangChain autonomous agent implementations
│   │   ├── __init__.py               # Agent module exports
│   │   ├── comparison_agent.py       # Multi-policy comparative analysis and trade-off agent
│   │   ├── customer_profile_agent.py # Entity extraction and risk classification agent
│   │   ├── insurance_recommendation_agent.py # Policy scoring and personalized summary agent
│   │   └── quote_generation_agent.py # Tailored quote proposal narrative generation agent
│   │
│   ├── api/                          # FastAPI route handlers
│   │   ├── __init__.py               # API router registry
│   │   ├── customer_api.py           # Endpoints for profile creation, retrieval, and risk scoring
│   │   ├── quote_api.py              # Endpoints for quote generation, comparison, and PDF export
│   │   ├── recommendation_api.py     # Endpoints for multi-criteria policy recommendations
│   │   └── voice_api.py              # Endpoints for STT transcribe, TTS synthesize, and voice turns
│   │
│   ├── database/                     # Relational persistence layer
│   │   ├── __init__.py               # Database module exports
│   │   ├── db.py                     # Async engine session manager with SQLite fallback
│   │   ├── models.py                 # SQLAlchemy ORM models (Customer, Policy, Quote, VoiceInteraction)
│   │   └── schema.sql                # Production DDL schema for PostgreSQL / Azure SQL
│   │
│   ├── prompts/                      # System prompts for LLM agents
│   │   ├── comparison_prompt.txt     # System prompt for policy trade-off analysis
│   │   ├── profiling_prompt.txt      # System prompt for customer entity extraction
│   │   ├── quote_prompt.txt          # System prompt for quote presentation narratives
│   │   └── recommendation_prompt.txt # System prompt for policy matching explanations
│   │
│   ├── services/                     # Business logic and external service integrations
│   │   ├── __init__.py               # Services module exports
│   │   ├── elevenlabs_service.py     # ElevenLabs text-to-speech integration with audio fallback
│   │   ├── pdf_service.py            # ReportLab publication-grade PDF quote proposal generator
│   │   ├── premium_engine.py         # Actuarial pricing calculations based on risk and riders
│   │   ├── uniphore_service.py       # Conversational analytics, sentiment, tone, and biometrics
│   │   └── whisper_service.py        # OpenAI/Azure Whisper speech-to-text service
│   │
│   ├── utils/                        # Shared utility modules
│   │   ├── __init__.py               # Utility exports
│   │   └── logger.py                 # Structured logging utility with Loguru / standard logging
│   │
│   └── workflows/                    # LangGraph orchestration state machine
│       ├── __init__.py               # Workflows module exports
│       └── insurance_workflow.py     # 8-step conversational state graph workflow
│
├── frontend/                         # Modern Single Page Application (SPA)
│   ├── Dockerfile                    # Multi-stage container build (Node.js -> Nginx)
│   ├── index.html                    # HTML document shell with Plus Jakarta Sans typography
│   ├── package.json                  # NPM dependencies (React 18, Vite, Tailwind CSS, Lucide)
│   ├── package-lock.json             # Pinned package lockfile
│   ├── postcss.config.js             # PostCSS plugins configuration
│   ├── tailwind.config.js            # Tailwind CSS theme styling configuration
│   ├── vite.config.js                # Vite build tool and API proxy configuration
│   │
│   └── src/                          # Frontend source code
│       ├── App.jsx                   # Primary state container, navigation tabs, and sync hub
│       ├── index.css                 # Global stylesheets and custom sound-wave animations
│       ├── main.jsx                  # React DOM client entrypoint
│       │
│       └── components/               # Modular UI component library
│           ├── CustomerProfile.jsx   # Profile editor with live actuarial risk gauge meter
│           ├── DemoWalkthrough.jsx   # 1-click persona scenario launcher for live demos
│           ├── Header.jsx            # Top navigation bar, backend health indicator, session badge
│           ├── PolicyComparison.jsx  # Side-by-side policy comparison matrix
│           ├── PolicyRecommendations.jsx # Recommended policy cards with match ratings
│           ├── QuoteGenerator.jsx    # Deductibles slider, add-on riders, and PDF exporter
│           ├── UniphoreAnalytics.jsx # Sentiment meter, speech tempo, tone, and biometrics
│           └── VoiceAssistant.jsx    # Voice mic controls, sound wave visualizer, audio chat
│
└── tests/                            # Automated test suites
    └── test_api_endpoints.py         # End-to-end test suite verifying all 9 backend endpoints
```

---

## Key Features

### 1. Conversational Voice Assistant
- **Dual Mode**: Use your real device microphone via the Web Speech API / Whisper STT or select 1-click demo prompts.
- **Audio Feedback**: Spoken AI audio responses via ElevenLabs TTS or native browser speech synthesis.
- **Real-Time Visualizer**: Animated sound wave bars indicate active listening and speaking states.

### 2. Actuarial Risk Engine & Profiling
- **Dynamic Entity Extraction**: Extracts age, income, dependents, tobacco use, and pre-existing medical conditions from voice or text.
- **Loss Probability Score**: Generates a continuous score ($0.00$ to $1.00$) categorizing applicants into **Low**, **Medium**, or **High** risk.
- **Income Multiplier**: Automatically recommends optimal coverage targets (e.g., $10\times$ annual income for life/health).

### 3. Actuarial Quote Engine & Deductible Customizer
- **Interactive Controls**: Adjust aggregate coverage ($100K–$1M), deductibles ($0–$1,500), and policy terms ($1–3$ years).
- **Add-on Riders**: Real-time pricing for Comprehensive Dental (+$25/mo), Vision & Eyewear (+$15/mo), Maternity (+$40/mo), and Critical Illness (+$35/mo).
- **Prepayment Incentive**: Highlights annual 5% prepayment savings.

### 4. Official PDF Quote Proposal Export
- **One-Click Download**: Automatically streams and downloads a formatted PDF to the user's `Downloads` folder as `Insurance_Quote_<ID>.pdf`.
- **In-Browser Document Preview**: On-screen preview modal displaying the exact layout with **Print** and **Download** actions.
- **Comprehensive Document Sections**:
  1. Header with branding and reference quote ID.
  2. Selected plan pricing, term, and annual discount summary.
  3. Applicant demographics and actuarial risk ratings.
  4. Full benefit schedule table (Hospitalization, Outpatient, Emergency, Prescriptions, Riders).
  5. Uniphore biometric verification stamp and underwriting signature block.

### 5. Multi-Policy Comparison Matrix
- Compare between 2 to 4 policies simultaneously.
- Evaluates monthly and annual costs, deductibles, coverage maximums, exclusions, and network constraints.
- Includes automated AI recommendation explaining the best value-to-cost choice.

### 6. Uniphore Conversation Intelligence
- Live customer sentiment detection (Positive, Neutral, Negative) with percentage index.
- Acoustic tone assessment (Enthusiastic, Inquisitive, Receptive, Concerned).
- Real-time speech tempo tracking in words per minute (WPM).
- Biometric verification confidence rating.

---

## API Endpoints Reference

Base URL: `http://localhost:8000` (Swagger documentation at `/docs`)

| Method | Path | Summary | Key Payload / Response |
|---|---|---|---|
| `GET` | `/health` | System health check | `{"status": "healthy", "service": "..."}` |
| `POST` | `/api/voice/transcribe` | Convert speech audio to text | Request: `audio_base64`<br>Response: `transcript, confidence, intent, sentiment` |
| `POST` | `/api/voice/synthesize` | Convert text to speech audio | Request: `text, voice_id`<br>Response: `audio_base64, duration_seconds` |
| `POST` | `/api/voice/conversation` | Full voice conversation turn | Request: `session_id, text_input / audio_base64`<br>Response: `assistant_message, intent, quote_data` |
| `POST` | `/api/customers/profile` | Create customer profile & risk score | Request: Customer demographic fields<br>Response: `customer_id, risk_profile, recommended_coverage` |
| `GET` | `/api/customers/{id}` | Retrieve customer profile | Response: Customer record |
| `POST` | `/api/customers/voice-profile`| Extract profile from voice transcript | Request: `transcript`<br>Response: `extracted_data, missing_fields` |
| `POST` | `/api/quotes/generate` | Calculate quote & coverage limits | Request: `coverage_amount, deductible, add_ons`<br>Response: `monthly_premium, annual_premium, coverage_details` |
| `GET` | `/api/quotes/{id}` | Retrieve quote details | Response: Active quote breakdown |
| `POST` | `/api/quotes/compare` | Compare 2–5 policies side by side | Request: `policy_ids`<br>Response: Comparative table and AI recommendation |
| `POST` | `/api/quotes/export-pdf` | Generate & download PDF proposal | Request: `quote_data, customer_data`<br>Response: `application/pdf` binary download stream |
| `GET` | `/api/quotes/{id}/pdf` | Direct download of quote PDF | Response: `application/pdf` binary download stream |
| `POST` | `/api/recommendations` | AI-ranked policy recommendations | Request: `budget_monthly, priorities`<br>Response: `recommendations, ai_summary` |

---

## Quick Start Guide

### Prerequisites
- **Python**: 3.11, 3.12, or 3.13 installed
- **Node.js**: 18.0.0 or higher
- **Package Managers**: `pip` and `npm`
- **Docker & Docker Compose** (optional, for containerized run)

---

### Environment Configuration

The application works out of the box with built-in SQLite auto-fallback and simulated AI heuristics. To customize or add real cloud API keys:

1. Copy the sample environment file:
   ```bash
   cp .env.example .env
   ```
2. (Optional) Provide your API credentials in `.env`:
   ```dotenv
   # Azure OpenAI (Optional - falls back to local heuristic reasoning if left blank)
   AZURE_OPENAI_API_KEY=your-azure-key
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

   # ElevenLabs TTS (Optional - falls back to synthetic audio & Web Speech API)
   ELEVENLABS_API_KEY=your-elevenlabs-key

   # Uniphore (Optional - falls back to built-in conversational analytics)
   UNIPHORE_API_KEY=your-uniphore-key

   # Database (Defaults to SQLite for local zero-setup execution)
   DATABASE_URL=sqlite+aiosqlite:///./insurance_advisor.db
   ```

---

### Backend Setup

1. Open a terminal in the project root:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI server:
   ```bash
   python main.py
   ```
   The backend will be live at `http://localhost:8000`. Test it by visiting `http://localhost:8000/docs` in your browser.

---

### Frontend Setup

1. Open a second terminal in the project root:
   ```bash
   cd frontend
   ```
2. Install npm dependencies:
   ```bash
   npm install
   ```
3. Start the Vite development server:
   ```bash
   npm run dev
   ```
4. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

---

### Docker Compose Deployment

To build and run the entire stack (FastAPI Backend, React Frontend, PostgreSQL 15, and Redis) in containers:

```bash
docker-compose up --build
```
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

---

## Testing and Verification

### Running Automated API Tests
A test suite covering all endpoints (including speech synthesis, LangGraph turns, actuarial quoting, and ReportLab PDF binary generation) is included in `tests/`:

```powershell
# From the project root with the backend virtual environment active:
backend\venv\Scripts\python.exe tests\test_api_endpoints.py
```

Expected output:
```
Running UC189 API Test Suite...
[PASS] /health passed
[PASS] /api/voice/transcribe passed
[PASS] /api/voice/synthesize passed
[PASS] /api/voice/conversation passed
[PASS] /api/customers/profile passed
[PASS] /api/quotes/generate passed
[PASS] /api/quotes/compare passed
[PASS] /api/recommendations passed
[PASS] /api/quotes/export-pdf passed (Valid PDF binary generated)

ALL API ENDPOINTS TESTED AND VERIFIED SUCCESSFULLY!
```

### Verifying Frontend Production Build
To verify that the frontend builds without TypeScript/JSX or bundling errors:

```bash
cd frontend
npm run build
```

---

## Documentation Index

Detailed engineering documentation is maintained in the [`docs/`](docs/) directory:
- [Architecture Specifications](docs/architecture.md): Deep dive into the LangGraph state machine, data models, and services.
- [API Specification](docs/api-specification.md): Request and response schemas for every endpoint.
- [Deployment Guide](docs/deployment-guide.md): Instructions for Azure App Service, Azure SQL, and Azure Static Web Apps.
- [User Journey Flows](docs/user-flow.md): Step-by-step visual flows of customer interactions.
- [Demo Script Guide](docs/demo-script.md): A 10-minute presentation guide with sample customer dialogues.

---

## 4-Day Development Roadmap

- [x] **Day 1: Foundation & Setup** — FastAPI gateway, SQLAlchemy models, database auto-fallback, and project layout.
- [x] **Day 2: Voice & AI Layer** — Whisper STT, ElevenLabs TTS, Uniphore conversational intelligence, and prompt engineering.
- [x] **Day 3: Quote Engine & LangGraph** — Actuarial pricing engine, LangGraph multi-turn workflow, and ReportLab PDF proposal generation.
- [x] **Day 4: Integration & Executive Demo** — React + Tailwind UI, live microphone controls, 1-click demo personas, and side-by-side comparison matrix.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
