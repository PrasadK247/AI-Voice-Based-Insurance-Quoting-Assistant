# Architecture – UC189 AI Voice-Based Insurance Quoting Assistant

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       FRONTEND (React)                          │
│ ┌──────────┐ ┌──────────────┐ ┌────────────┐ ┌──────────┐       │
│ │ Dashboard│ │InsuranceQuote│ │ PolicyComp │ │ Profile  │       │
│ └─────┬────┘ └──────┬───────┘ └─────┬──────┘ └────┬─────┘       │
│       └─────────────┼───────────────┼─────────────┘             │
│                     │ REST / WebSocket                          │
└─────────────────────┼───────────────────────────────────────────┘
                      │
┌─────────────────────┼───────────────────────────────────────────┐
│                     ▼               BACKEND (FastAPI)           │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │                        API Gateway                          │ │
│ │   voice_api  │  quote_api  │  customer_api  │ recom_api     │ │
│ └─────────────────────────┬───────────────────────────────────┘ │
│                           │                                     │
│ ┌─────────────────────────▼───────────────────────────────────┐ │
│ │                 LangGraph Workflow Engine                   │ │
│ │    Voice Input → Intent → Profile → Risk → Quote            │ │
│ └─────────────────────────┬───────────────────────────────────┘ │
│                           │                                     │
│ ┌─────────────────────────▼───────────────────────────────────┐ │
│ │                 LangChain Agents Layer                      │ │
│ │   Profile  │  Recommendation  │  Quote  │  Comparison       │ │
│ └─────────────────────────┬───────────────────────────────────┘ │
│                           │                                     │
│ ┌─────────────────────────▼───────────────────────────────────┐ │
│ │                     Services Layer                          │ │
│ │   OpenAI  │  Uniphore  │  Whisper  │  ElevenLabs  │ Premium │ │
│ └─────────────────────────┬───────────────────────────────────┘ │
│                           │                                     │
│ ┌─────────────────────────▼───────────────────────────────────┐ │
│ │  PostgreSQL / SQLite  │    Azure Blob    │      Redis       │ │
│ └───────────────────────┴──────────────────┴──────────────────┘ │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                          │
│    Azure OpenAI  │  Uniphore Platform  │  ElevenLabs  │ Whisper │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Voice Layer
- **Whisper STT:** Converts customer speech audio to text with high confidence.
- **ElevenLabs TTS:** Converts AI responses to natural, realistic speech.
- **Uniphore:** Biometrics, sentiment analysis, tonal emotion, and conversation intelligence.

### AI Layer
- **LangChain Agents:** Specialized agents for profiling, quoting, comparison, and policy recommendation.
- **LangGraph:** Orchestrates the multi-step workflow as an explicit state machine.
- **Azure OpenAI:** LLM backend (GPT-4) for intent reasoning, entity extraction, and conversational generation.

### Data Layer
- **PostgreSQL / Azure SQL:** Relational storage for customers, policies, quotes, and conversation interactions (with SQLite local fallback).
- **Azure Blob:** Audio recordings and generated quote documents.
- **Redis:** Session caching and rate limiting.

## Data Flow
1. Customer speaks into microphone or inputs text.
2. Audio sent to Whisper STT → transcribed text.
3. Uniphore analyzes sentiment + conversational biometrics.
4. LangGraph workflow processes intent and extracts profiling entities.
5. Appropriate LangChain agent handles customer risk assessment and policy matching.
6. Actuarial Premium Engine calculates quotes and coverage tiers.
7. Explanatory response generated via Azure OpenAI.
8. ElevenLabs converts response to speech.
9. Audio streamed and played back to customer with live UI update.
