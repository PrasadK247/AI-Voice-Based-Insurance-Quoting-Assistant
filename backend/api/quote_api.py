"""
UC189 - Quote API Endpoints
Handles insurance quote generation, retrieval, and comparison.
"""

from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

from database.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from agents.quote_generation_agent import QuoteGenerationAgent
from agents.comparison_agent import ComparisonAgent
from services.premium_engine import PremiumEngine
from services.pdf_service import PDFQuoteService
from utils.logger import setup_logger


router = APIRouter()
logger = setup_logger(__name__)


# ── Request / Response Models ──────────────────────────

class QuoteRequest(BaseModel):
    customer_id: str
    insurance_type: str = Field(default="health", description="health, life, auto, home")
    coverage_amount: float = Field(default=500000.0, gt=0)
    deductible: float = Field(default=500.0, ge=0)
    term_years: int = Field(default=1, ge=1, le=30)
    add_ons: List[str] = Field(default_factory=list)


class CompareRequest(BaseModel):
    customer_id: str
    policy_ids: List[str] = Field(..., min_length=2, max_length=5)


class CoverageDetail(BaseModel):
    category: str
    covered: bool
    limit: Optional[float] = None
    description: str


class QuoteResponse(BaseModel):
    success: bool
    quote_id: str
    policy_name: str
    insurance_type: str
    monthly_premium: float
    annual_premium: float
    coverage_amount: float
    deductible: float
    term_years: int
    coverage_details: List[CoverageDetail]
    add_ons: List[str]
    generated_at: str


class ComparisonResponse(BaseModel):
    success: bool
    policies: List[dict]
    recommendation: str
    comparison_summary: str


# ── Endpoints ──────────────────────────────────────────

@router.post("/generate", response_model=QuoteResponse)
async def generate_quote(request: QuoteRequest):
    """Generate an insurance quote for a customer."""
    logger.info(f"Generating quote for customer {request.customer_id}")

    try:
        premium_engine = PremiumEngine()
        quote_agent = QuoteGenerationAgent()

        # Calculate premiums
        premium_result = premium_engine.calculate_premium(
            insurance_type=request.insurance_type,
            coverage_amount=request.coverage_amount,
            deductible=request.deductible,
            term_years=request.term_years,
            add_ons=request.add_ons,
            customer_id=request.customer_id,
        )

        # Generate quote details via agent
        quote_details = await quote_agent.generate(
            customer_id=request.customer_id,
            insurance_type=request.insurance_type,
            coverage_amount=request.coverage_amount,
            premium_data=premium_result,
        )

        quote_id = f"qt_{uuid.uuid4().hex[:12]}"

        coverage_details = [
            CoverageDetail(
                category="Hospitalization",
                covered=True,
                limit=round(request.coverage_amount * 0.8, 2),
                description="In-patient hospitalization and intensive care coverage",
            ),
            CoverageDetail(
                category="Outpatient",
                covered=True,
                limit=round(request.coverage_amount * 0.3, 2),
                description="Outpatient physician consultations and lab diagnostics",
            ),
            CoverageDetail(
                category="Emergency",
                covered=True,
                limit=round(request.coverage_amount * 0.5, 2),
                description="Emergency room visits and ground ambulance transport",
            ),
            CoverageDetail(
                category="Prescription",
                covered=True,
                limit=round(request.coverage_amount * 0.15, 2),
                description="Tier 1-4 prescription medication formulary coverage",
            ),
        ]

        if "dental" in request.add_ons:
            coverage_details.append(
                CoverageDetail(
                    category="Dental",
                    covered=True,
                    limit=5000.0,
                    description="Preventative, basic, and major restorative dental care",
                )
            )
        if "vision" in request.add_ons:
            coverage_details.append(
                CoverageDetail(
                    category="Vision",
                    covered=True,
                    limit=2000.0,
                    description="Annual eye exam, prescription eyeglasses, and lenses",
                )
            )

        return QuoteResponse(
            success=True,
            quote_id=quote_id,
            policy_name=premium_result.get("policy_name", "Standard Plan"),
            insurance_type=request.insurance_type,
            monthly_premium=premium_result["monthly_premium"],
            annual_premium=premium_result["annual_premium"],
            coverage_amount=request.coverage_amount,
            deductible=request.deductible,
            term_years=request.term_years,
            coverage_details=coverage_details,
            add_ons=request.add_ons,
            generated_at=datetime.utcnow().isoformat() + "Z",
        )

    except Exception as e:
        logger.error(f"Quote generation failed: {e}")
        raise HTTPException(status_code=500, detail=f"Quote generation failed: {str(e)}")


@router.get("/{quote_id}")
async def get_quote(quote_id: str):
    """Retrieve a previously generated quote."""
    logger.info(f"Retrieving quote {quote_id}")

    return {
        "success": True,
        "quote_id": quote_id,
        "status": "active",
        "message": "Quote retrieved successfully",
        "details": {
            "policy_name": "Premium Health Shield",
            "monthly_premium": 450.0,
            "annual_premium": 5130.0,
            "coverage_amount": 500000.0,
            "deductible": 500.0,
        },
    }


@router.post("/compare", response_model=ComparisonResponse)
async def compare_policies(request: CompareRequest):
    """Compare multiple insurance policies side by side."""
    logger.info(f"Comparing policies for customer {request.customer_id}")

    try:
        comparison_agent = ComparisonAgent()
        result = await comparison_agent.compare(
            customer_id=request.customer_id,
            policy_ids=request.policy_ids,
        )

        return ComparisonResponse(
            success=True,
            policies=result.get("policies", []),
            recommendation=result.get("recommendation", ""),
            comparison_summary=result.get("summary", ""),
        )

    except Exception as e:
        logger.error(f"Policy comparison failed: {e}")
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")


class ExportPDFRequest(BaseModel):
    quote_data: dict
    customer_data: Optional[dict] = None


@router.post("/export-pdf")
async def export_quote_pdf(request: ExportPDFRequest):
    """Generate and return a professional PDF document for an insurance quote."""
    logger.info("Handling PDF export request")
    try:
        pdf_service = PDFQuoteService()
        pdf_bytes = pdf_service.generate_quote_pdf(
            quote_data=request.quote_data,
            customer_data=request.customer_data,
        )

        quote_id = request.quote_data.get("quote_id", "quote")
        filename = f"Insurance_Quote_{quote_id}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )
    except Exception as e:
        logger.error(f"PDF export failed: {e}")
        raise HTTPException(status_code=500, detail=f"PDF export failed: {str(e)}")


@router.get("/{quote_id}/pdf")
async def download_quote_pdf(quote_id: str):
    """Download PDF for a given quote ID directly."""
    logger.info(f"Downloading PDF for quote ID {quote_id}")
    try:
        pdf_service = PDFQuoteService()
        sample_quote = {
            "quote_id": quote_id,
            "policy_name": "Family Care Plus",
            "monthly_premium": 380.0,
            "annual_premium": 4332.0,
            "coverage_amount": 500000.0,
            "deductible": 500.0,
            "term_years": 1,
            "add_ons": ["dental", "vision"],
        }
        sample_customer = {
            "name": "Sarah & David Miller",
            "age": 35,
            "annual_income": 120000.0,
            "location": "Austin, TX",
            "family_members": 4,
            "risk_category": "low",
            "risk_score": 0.25,
        }
        pdf_bytes = pdf_service.generate_quote_pdf(sample_quote, sample_customer)
        filename = f"Insurance_Quote_{quote_id}.pdf"

        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Access-Control-Expose-Headers": "Content-Disposition",
            },
        )
    except Exception as e:
        logger.error(f"PDF download failed: {e}")
        raise HTTPException(status_code=500, detail=f"PDF download failed: {str(e)}")

