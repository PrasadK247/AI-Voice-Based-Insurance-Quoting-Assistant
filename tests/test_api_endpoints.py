"""
UC189 - End-to-End API Test Suite
Validates all voice, customer, quote, and recommendation endpoints.
"""

import sys
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    print("[PASS] /health passed")


def test_voice_transcribe_and_synthesize():
    # 1. Transcribe
    trans_resp = client.post(
        "/api/voice/transcribe",
        json={"audio_base64": "UklGRiQAAABXQVZFZm10IBAAAAABAAEARKwAAIhYAQACABAAZGF0YQAAAAA=", "language": "en"},
    )
    assert trans_resp.status_code == 200
    trans_data = trans_resp.json()
    assert trans_data["success"] is True
    assert "transcript" in trans_data
    print("[PASS] /api/voice/transcribe passed")

    # 2. Synthesize
    synth_resp = client.post(
        "/api/voice/synthesize",
        json={"text": "Your quote is $380 per month.", "voice_id": "default"},
    )
    assert synth_resp.status_code == 200
    synth_data = synth_resp.json()
    assert synth_data["success"] is True
    assert "audio_base64" in synth_data
    print("[PASS] /api/voice/synthesize passed")


def test_voice_conversation_turn():
    conv_resp = client.post(
        "/api/voice/conversation",
        json={
            "session_id": "test_sess_001",
            "text_input": "I need health insurance for my family of 4",
        },
    )
    assert conv_resp.status_code == 200
    data = conv_resp.json()
    assert data["success"] is True
    assert len(data["assistant_message"]) > 0
    assert data["intent"] in ["customer_profiling", "quote_generation", "general_inquiry"]
    print("[PASS] /api/voice/conversation passed")


def test_customer_profile():
    prof_resp = client.post(
        "/api/customers/profile",
        json={
            "name": "David Miller",
            "age": 35,
            "gender": "male",
            "occupation": "Architect",
            "annual_income": 120000.0,
            "location": "Austin, TX",
            "smoking_status": False,
            "pre_existing_conditions": [],
            "family_members": 4,
            "insurance_type": "health",
        },
    )
    assert prof_resp.status_code == 200
    data = prof_resp.json()
    assert data["success"] is True
    assert "customer_id" in data
    assert data["risk_profile"]["risk_category"] == "low"
    assert data["recommended_coverage"] == 1200000.0
    print("[PASS] /api/customers/profile passed")


def test_quote_generate_and_compare():
    # 1. Generate Quote
    q_resp = client.post(
        "/api/quotes/generate",
        json={
            "customer_id": "cust_test_123",
            "insurance_type": "health",
            "coverage_amount": 500000.0,
            "deductible": 500.0,
            "term_years": 1,
            "add_ons": ["dental", "vision"],
        },
    )
    assert q_resp.status_code == 200
    q_data = q_resp.json()
    assert q_data["success"] is True
    assert q_data["monthly_premium"] > 0
    assert q_data["annual_premium"] > 0
    assert len(q_data["coverage_details"]) >= 4
    print("[PASS] /api/quotes/generate passed")

    # 2. Compare Policies
    comp_resp = client.post(
        "/api/quotes/compare",
        json={
            "customer_id": "cust_test_123",
            "policy_ids": ["pol_003", "pol_001"],
        },
    )
    assert comp_resp.status_code == 200
    comp_data = comp_resp.json()
    assert comp_data["success"] is True
    assert len(comp_data["policies"]) == 2
    assert len(comp_data["recommendation"]) > 0
    print("[PASS] /api/quotes/compare passed")


def test_recommendations():
    rec_resp = client.post(
        "/api/recommendations",
        json={
            "customer_id": "cust_test_123",
            "budget_monthly": 500.0,
            "priorities": ["coverage", "premium", "network"],
            "insurance_type": "health",
        },
    )
    assert rec_resp.status_code == 200
    rec_data = rec_resp.json()
    assert rec_data["success"] is True
    assert len(rec_data["recommendations"]) > 0
    assert len(rec_data["ai_summary"]) > 0
    print("[PASS] /api/recommendations passed")


def test_export_pdf():
    pdf_resp = client.post(
        "/api/quotes/export-pdf",
        json={
            "quote_data": {
                "quote_id": "qt_test_pdf_01",
                "policy_name": "Family Care Plus",
                "monthly_premium": 380.0,
                "annual_premium": 4332.0,
                "coverage_amount": 500000.0,
                "deductible": 500.0,
                "term_years": 1,
                "add_ons": ["dental", "vision"],
            },
            "customer_data": {
                "name": "Sarah Miller",
                "age": 35,
                "annual_income": 120000.0,
                "location": "Austin, TX",
                "family_members": 4,
                "risk_category": "low",
                "risk_score": 0.25,
            },
        },
    )
    assert pdf_resp.status_code == 200
    assert pdf_resp.headers["content-type"] == "application/pdf"
    assert pdf_resp.content[:4] == b"%PDF"
    print("[PASS] /api/quotes/export-pdf passed (Valid PDF binary generated)")


if __name__ == "__main__":
    print("Running UC189 API Test Suite...")
    test_health_endpoint()
    test_voice_transcribe_and_synthesize()
    test_voice_conversation_turn()
    test_customer_profile()
    test_quote_generate_and_compare()
    test_recommendations()
    test_export_pdf()
    print("\nALL API ENDPOINTS TESTED AND VERIFIED SUCCESSFULLY!")

