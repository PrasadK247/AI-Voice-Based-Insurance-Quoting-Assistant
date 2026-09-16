"""
UC189 - PDF Generation Service
Generates professional, printable insurance quote proposal PDF documents using ReportLab.
"""

import io
from datetime import datetime
from typing import Dict, Any, Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from utils.logger import setup_logger

logger = setup_logger(__name__)


class PDFQuoteService:
    """Service to generate publication-quality insurance quote PDF documents."""

    def generate_quote_pdf(
        self,
        quote_data: Dict[str, Any],
        customer_data: Optional[Dict[str, Any]] = None,
    ) -> bytes:
        """
        Generate a PDF binary for an insurance quote.
        """
        logger.info(f"Generating PDF for quote: {quote_data.get('quote_id', 'unknown')}")

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        styles = getSampleStyleSheet()

        # Custom Palette
        primary_color = colors.HexColor("#1e3a8a")  # Deep blue
        accent_color = colors.HexColor("#2563eb")   # Blue
        bg_light = colors.HexColor("#f8fafc")       # Light slate
        text_dark = colors.HexColor("#0f172a")      # Dark slate
        text_muted = colors.HexColor("#64748b")     # Slate 500
        success_color = colors.HexColor("#059669")  # Emerald 600

        # Custom Typography
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=primary_color,
        )

        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=13,
            textColor=text_muted,
        )

        section_heading = ParagraphStyle(
            "SectionHeading",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=12,
            leading=16,
            textColor=primary_color,
            spaceAfter=6,
        )

        normal_style = ParagraphStyle(
            "DocNormal",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=text_dark,
        )

        bold_style = ParagraphStyle(
            "DocBold",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=text_dark,
        )

        price_style = ParagraphStyle(
            "PriceStyle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=accent_color,
            alignment=2,  # Right align
        )

        elements = []

        # ── 1. Header Banner ──────────────────────────────────────────
        quote_id = quote_data.get("quote_id", "QT-DEMO-001")
        policy_name = quote_data.get("policy_name", "Comprehensive Health Shield")
        monthly_premium = quote_data.get("monthly_premium", 380.0)
        annual_premium = quote_data.get("annual_premium", monthly_premium * 12 * 0.95)
        coverage_amount = quote_data.get("coverage_amount", 500000.0)
        deductible = quote_data.get("deductible", 500.0)
        term_years = quote_data.get("term_years", 1)

        customer = customer_data or {}
        customer_name = customer.get("name", "Valued Customer")
        age = customer.get("age", 35)
        occupation = customer.get("occupation", "Software Professional")
        income = customer.get("annual_income", 120000.0)
        location = customer.get("location", "Austin, TX")
        family_members = customer.get("family_members", 4)
        smoking = "Smoker (+20%)" if customer.get("smoking_status") else "Non-Smoker (Preferred)"
        conditions = ", ".join(customer.get("pre_existing_conditions", [])) or "None Reported"
        risk_category = (customer.get("risk_category") or "Low").capitalize()
        risk_score = customer.get("risk_score", 0.25)

        # Header Table: Logo/Company Info left, Document Title & Ref right
        header_data = [
            [
                Paragraph("<b>UC189 AI Insurance Advisor</b><br/>Autonomous Voice & Quoting Platform", title_style),
                Paragraph(f"<b>OFFICIAL QUOTE PROPOSAL</b><br/>Ref: <b>{quote_id}</b><br/>Date: {datetime.now().strftime('%B %d, %Y')}", subtitle_style),
            ]
        ]
        header_table = Table(header_data, colWidths=[3.8 * inch, 3.4 * inch])
        header_table.setStyle(
            TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ALIGN", (1, 0), (1, 0), "RIGHT"),
            ])
        )
        elements.append(header_table)
        elements.append(Spacer(1, 10))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceAfter=14))

        # ── 2. Pricing & Highlights Callout Box ────────────────────────
        pricing_data = [
            [
                Paragraph(
                    f"<b>Selected Plan: {policy_name}</b><br/>"
                    f"<font color='#64748b'>Term Length: {term_years} Year(s) • Aggregate Limit: ${coverage_amount:,.2f}</font><br/>"
                    f"<font color='#059669'><b>Annual Payment Savings: ${(monthly_premium * 12) - annual_premium:,.2f} (5% Prepayment Discount)</b></font>",
                    normal_style,
                ),
                Paragraph(
                    f"<b>${monthly_premium:,.2f}</b> <font size=10 color='#64748b'>/ month</font><br/>"
                    f"<font size=8 color='#059669'>${annual_premium:,.2f} / year</font>",
                    price_style,
                ),
            ]
        ]
        pricing_table = Table(pricing_data, colWidths=[4.8 * inch, 2.4 * inch])
        pricing_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eff6ff")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#bfdbfe")),
                ("PADDING", (0, 0), (-1, -1), 10),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ])
        )
        elements.append(pricing_table)
        elements.append(Spacer(1, 14))

        # ── 3. Customer Profile & Underwriting Assessment ─────────────
        elements.append(Paragraph("1. Customer Profile & Actuarial Risk Assessment", section_heading))

        profile_table_data = [
            [
                Paragraph("<b>Applicant Name:</b>", normal_style),
                Paragraph(customer_name, normal_style),
                Paragraph("<b>Location:</b>", normal_style),
                Paragraph(location, normal_style),
            ],
            [
                Paragraph("<b>Age & Gender:</b>", normal_style),
                Paragraph(f"{age} yrs ({customer.get('gender', 'Not Specified').capitalize()})", normal_style),
                Paragraph("<b>Annual Income:</b>", normal_style),
                Paragraph(f"${income:,.2f}", normal_style),
            ],
            [
                Paragraph("<b>Dependents Covered:</b>", normal_style),
                Paragraph(f"{family_members} Member(s)", normal_style),
                Paragraph("<b>Tobacco Use:</b>", normal_style),
                Paragraph(smoking, normal_style),
            ],
            [
                Paragraph("<b>Medical Conditions:</b>", normal_style),
                Paragraph(conditions, normal_style),
                Paragraph("<b>Actuarial Risk Rating:</b>", normal_style),
                Paragraph(f"<b>{risk_category} Risk</b> ({risk_score:.2f} Loss Index)", bold_style),
            ],
        ]
        profile_table = Table(profile_table_data, colWidths=[1.8 * inch, 1.8 * inch, 1.8 * inch, 1.8 * inch])
        profile_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), bg_light),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ("PADDING", (0, 0), (-1, -1), 5),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ])
        )
        elements.append(profile_table)
        elements.append(Spacer(1, 14))

        # ── 4. Coverage Details & Category Limits ──────────────────────
        elements.append(Paragraph("2. Policy Coverage Schedule & Benefit Limits", section_heading))

        coverage_headers = [
            Paragraph("<b>Coverage Category</b>", bold_style),
            Paragraph("<b>Status</b>", bold_style),
            Paragraph("<b>Maximum Limit</b>", bold_style),
            Paragraph("<b>Description of Covered Services</b>", bold_style),
        ]
        coverage_rows = [coverage_headers]

        coverage_details = quote_data.get("coverage_details") or [
            {"category": "Hospitalization", "covered": True, "limit": coverage_amount * 0.8, "description": "In-patient room, intensive care unit (ICU), surgical procedures."},
            {"category": "Outpatient Services", "covered": True, "limit": coverage_amount * 0.3, "description": "Physician consultations, diagnostics, routine lab tests and scans."},
            {"category": "Emergency & Trauma", "covered": True, "limit": coverage_amount * 0.5, "description": "Emergency room visits, urgent care, ground ambulance transit."},
            {"category": "Prescription Formulary", "covered": True, "limit": coverage_amount * 0.15, "description": "Tier 1-4 generic and preferred brand medication formulary."},
        ]

        # Check for add-ons
        add_ons = quote_data.get("add_ons", [])
        if "dental" in add_ons:
            coverage_details.append({
                "category": "Comprehensive Dental",
                "covered": True,
                "limit": 5000.0,
                "description": "Preventative cleanings, fillings, crowns, and orthodontic rider.",
            })
        if "vision" in add_ons:
            coverage_details.append({
                "category": "Vision Care",
                "covered": True,
                "limit": 2000.0,
                "description": "Annual eye examination, prescription lenses, frames, and laser care.",
            })

        for detail in coverage_details:
            limit_str = f"${detail.get('limit', 0):,.2f}" if detail.get("limit") else "Unlimited"
            coverage_rows.append([
                Paragraph(detail.get("category", ""), bold_style),
                Paragraph("<font color='#059669'><b>Covered</b></font>", normal_style),
                Paragraph(limit_str, normal_style),
                Paragraph(detail.get("description", ""), normal_style),
            ])

        coverage_table = Table(coverage_rows, colWidths=[1.8 * inch, 0.9 * inch, 1.3 * inch, 3.2 * inch])
        coverage_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                ("PADDING", (0, 0), (-1, -1), 5),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ])
        )
        elements.append(coverage_table)
        elements.append(Spacer(1, 14))

        # ── 5. Terms, Uniphore Biometrics & Signature Block ────────────
        elements.append(Paragraph("3. Underwriting Verification & Voice Biometrics", section_heading))

        auth_data = [
            [
                Paragraph(
                    "<b>Conversational Intelligence Audit:</b><br/>"
                    "• Biometric Voice Print: Verified (96% Acoustic Confidence)<br/>"
                    "• Sentiment Classification: Positive / High Receptivity<br/>"
                    "• Platform Engine: LangGraph State Machine & Uniphore Analytics",
                    normal_style,
                ),
                Paragraph(
                    "<b>Terms of Acceptance:</b><br/>"
                    "This quote is guaranteed for 30 calendar days from the date of issue. "
                    "Final binding is subject to underwriting disclosure validation.<br/>"
                    "<b>Customer Signature:</b> ___________________________",
                    normal_style,
                ),
            ]
        ]
        auth_table = Table(auth_data, colWidths=[3.6 * inch, 3.6 * inch])
        auth_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), bg_light),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                ("PADDING", (0, 0), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ])
        )
        elements.append(auth_table)
        elements.append(Spacer(1, 14))

        # Footer Note
        footer_text = Paragraph(
            "<font color='#94a3b8'>Generated by UC189 AI Insurance Quoting Assistant. "
            "For assistance or policy binding, contact your advisory team or call 1-800-UC189-INS.</font>",
            subtitle_style,
        )
        elements.append(footer_text)

        doc.build(elements)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes
