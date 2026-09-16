# API Specification – UC189

## Base URL
`http://localhost:8000`

## Authentication
Bearer token in `Authorization` header (`Bearer <token>`) for production deployments.

---

## Voice Endpoints

### POST `/api/voice/transcribe`
Transcribe base64-encoded audio to text.

**Request:**
```json
{
  "audio_base64": "base64-encoded-audio",
  "language": "en",
  "format": "wav"
}
```

**Response:**
```json
{
  "success": true,
  "transcript": "I need health insurance for my family",
  "confidence": 0.95,
  "language": "en",
  "duration_seconds": 4.2,
  "sentiment": "positive"
}
```

### POST `/api/voice/synthesize`
Convert text to natural speech.

**Request:**
```json
{
  "text": "Based on your profile, I recommend Plan A.",
  "voice_id": "default",
  "speed": 1.0
}
```

**Response:**
```json
{
  "success": true,
  "audio_base64": "base64-encoded-audio",
  "duration_seconds": 3.1
}
```

### POST `/api/voice/conversation`
Full conversational turn handling voice transcription, agent reasoning, quote calculation, and voice generation.

---

## Customer Endpoints

### POST `/api/customers/profile`
Create or update customer profile with automated risk scoring.

**Request:**
```json
{
  "name": "John Doe",
  "age": 35,
  "gender": "male",
  "occupation": "software_engineer",
  "annual_income": 120000,
  "location": "New York",
  "smoking_status": false,
  "pre_existing_conditions": [],
  "family_members": 4,
  "insurance_type": "health"
}
```

**Response:**
```json
{
  "success": true,
  "customer_id": "cust_abc123",
  "name": "John Doe",
  "risk_profile": {
    "risk_score": 0.25,
    "risk_category": "low",
    "risk_factors": []
  },
  "profile_complete": true,
  "recommended_coverage": 1200000.0,
  "suggested_insurance_types": ["health", "life"]
}
```

### GET `/api/customers/{customer_id}`
Retrieve customer profile by ID.

---

## Quote Endpoints

### POST `/api/quotes/generate`
Generate an insurance quote.

**Request:**
```json
{
  "customer_id": "cust_abc123",
  "insurance_type": "health",
  "coverage_amount": 500000,
  "deductible": 1000,
  "term_years": 1,
  "add_ons": ["dental", "vision"]
}
```

**Response:**
```json
{
  "success": true,
  "quote_id": "qt_xyz789",
  "policy_name": "Premium Health Shield",
  "insurance_type": "health",
  "monthly_premium": 450.00,
  "annual_premium": 5130.00,
  "coverage_amount": 500000.0,
  "deductible": 1000.0,
  "term_years": 1,
  "coverage_details": [
    {
      "category": "Hospitalization",
      "covered": true,
      "limit": 400000.0,
      "description": "In-patient hospitalization coverage"
    }
  ],
  "add_ons": ["dental", "vision"],
  "generated_at": "2026-01-15T10:30:00Z"
}
```

### GET `/api/quotes/{quote_id}`
Retrieve quote details.

### POST `/api/quotes/compare`
Compare multiple policies side by side.

### POST `/api/quotes/export-pdf`
Generate and download a high-resolution, printable PDF proposal for an insurance quote.

**Request:**
```json
{
  "quote_data": {
    "quote_id": "qt_xyz789",
    "policy_name": "Family Care Plus",
    "monthly_premium": 380.00,
    "annual_premium": 4332.00,
    "coverage_amount": 500000.0,
    "deductible": 500.0,
    "term_years": 1,
    "add_ons": ["dental", "vision"]
  },
  "customer_data": {
    "name": "Sarah & David Miller",
    "age": 35,
    "annual_income": 120000,
    "location": "Austin, TX",
    "family_members": 4,
    "risk_category": "low",
    "risk_score": 0.25
  }
}
```

**Response:**
Binary stream (`application/pdf`) with `Content-Disposition: attachment; filename="Insurance_Quote_qt_xyz789.pdf"`.

### GET `/api/quotes/{quote_id}/pdf`
Directly download the official proposal PDF for a given quote ID.

---


## Recommendation Endpoints

### POST `/api/recommendations`
Get AI-powered policy recommendations ranked by user profile, budget, and priority weights.
