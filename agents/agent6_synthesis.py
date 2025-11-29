"""
Agent 6: Response Synthesis & PDF Generation
Generates final results with multilingual translations and PDF receipts
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from loguru import logger

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors

from utils.translator import translate_from_english, get_language_name, is_fully_supported


class SynthesisAgent:
    """
    Agent 6: Synthesizes final results
    Generates multilingual explanations and PDF verification receipts
    """
    
    def __init__(self, receipts_dir: str = "./receipts"):
        self.receipts_dir = Path(receipts_dir)
        self.receipts_dir.mkdir(exist_ok=True)
        
    def build_response(self, virality_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build final response with translations and PDFs
        
        Args:
            virality_output: Output from Agent 5
            
        Returns:
            {
                "primary_language": str,
                "language_support": "full" | "partial",
                "results": [
                    {
                        ...all previous fields...,
                        "short_explain_local": str,
                        "receipt_pdf_path": str,
                        "timestamp": str
                    }
                ],
                "visual_forensics": dict,
                "summary": {
                    "total_claims": int,
                    "true_count": int,
                    "false_count": int,
                    "neutral_count": int,
                    "highest_risk": str
                }
            }
        """
        logger.info("Starting response synthesis")
        
        primary_language = virality_output["primary_language"]
        claims = virality_output["claims_with_virality"]
        
        results = []
        
        for claim_data in claims:
            # Translate explanation to original language
            local_explain = self._translate_explanation(
                claim_data["short_explain_en"],
                primary_language
            )
            
            # Generate PDF receipt
            pdf_path = self._generate_pdf_receipt(claim_data, primary_language)
            
            # Build result
            result = {
                **claim_data,
                "short_explain_local": local_explain,
                "receipt_pdf_path": pdf_path,
                "timestamp": datetime.now().isoformat()
            }
            
            results.append(result)
        
        # Generate summary
        summary = self._generate_summary(results)
        
        # Check language support
        language_support = "full" if is_fully_supported(primary_language) else "partial"
        
        logger.info("Response synthesis complete")
        
        return {
            "primary_language": primary_language,
            "language_name": get_language_name(primary_language),
            "language_support": language_support,
            "results": results,
            "visual_forensics": virality_output.get("visual_forensics", {}),
            "summary": summary
        }
    
    def _translate_explanation(self, english_text: str, target_lang: str) -> str:
        """
        Translate explanation to target language
        
        Args:
            english_text: English explanation
            target_lang: Target language code
            
        Returns:
            Translated text (or English if not supported)
        """
        if target_lang == "en":
            return english_text
        
        try:
            translated = translate_from_english(english_text, target_lang)
            return translated
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            return english_text
    
    def _generate_pdf_receipt(
        self, 
        claim_data: Dict[str, Any],
        language: str
    ) -> str:
        """
        Generate PDF verification receipt
        
        Args:
            claim_data: Claim with all verification data
            language: Primary language code
            
        Returns:
            Path to generated PDF file
        """
        filename = f"{claim_data['claim_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = self.receipts_dir / filename
        
        try:
            # Create PDF
            doc = SimpleDocTemplate(
                str(filepath),
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )
            
            # Container for elements
            elements = []
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor('#1a73e8'),
                spaceAfter=30,
                alignment=TA_CENTER
            )
            
            heading_style = ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontSize=14,
                textColor=colors.HexColor('#333333'),
                spaceAfter=12
            )
            
            # Title
            elements.append(Paragraph("🛡️ VERITAS GUARDIAN", title_style))
            elements.append(Paragraph("Verification Receipt", styles['Heading2']))
            elements.append(Spacer(1, 20))
            
            # Claim ID and timestamp
            elements.append(Paragraph(f"<b>Claim ID:</b> {claim_data['claim_id']}", styles['Normal']))
            elements.append(Paragraph(f"<b>Timestamp:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
            elements.append(Spacer(1, 20))
            
            # Verdict box
            verdict_color = self._get_verdict_color(claim_data['user_label'])
            elements.append(Paragraph("<b>VERDICT</b>", heading_style))
            
            verdict_data = [
                ['Label', claim_data['user_label']],
                ['Confidence', f"{claim_data['confidence']}%"],
                ['Risk Level', claim_data['combined_risk_level'].upper()]
            ]
            
            verdict_table = Table(verdict_data, colWidths=[2*inch, 3.5*inch])
            verdict_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8f9fa')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            elements.append(verdict_table)
            elements.append(Spacer(1, 20))
            
            # Claim text
            elements.append(Paragraph("<b>CLAIM</b>", heading_style))
            elements.append(Paragraph(claim_data['claim'], styles['Normal']))
            elements.append(Spacer(1, 20))
            
            # Explanation
            elements.append(Paragraph("<b>EXPLANATION</b>", heading_style))
            elements.append(Paragraph(claim_data['short_explain_en'], styles['Normal']))
            elements.append(Spacer(1, 20))
            
            # Evidence summary
            elements.append(Paragraph("<b>EVIDENCE SOURCES</b>", heading_style))
            evidence_list = claim_data.get('evidence', [])[:5]  # Top 5
            for idx, ev in enumerate(evidence_list, 1):
                source_name = ev.get('source_name', ev.get('domain', 'Unknown'))
                elements.append(Paragraph(
                    f"{idx}. <b>{source_name}</b> [{ev['source_type']}] - Credibility: {ev['credibility_score']}/100<br/>"
                    f"   {ev['title']}<br/>"
                    f"   <i>{ev['url']}</i>",
                    styles['Normal']
                ))
            elements.append(Spacer(1, 20))
            
            # Virality & Risk
            elements.append(Paragraph("<b>VIRALITY ANALYSIS</b>", heading_style))
            virality_data = [
                ['Virality Score', f"{claim_data['virality_score']}/100"],
                ['Risk Level', claim_data['combined_risk_level'].upper()]
            ]
            virality_table = Table(virality_data, colWidths=[2*inch, 3.5*inch])
            virality_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff3cd')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey)
            ]))
            elements.append(virality_table)
            elements.append(Spacer(1, 30))
            
            # Footer
            elements.append(Paragraph(
                "<i>This verification was performed by Veritas Guardian AI system. "
                "For questions, contact your administrator.</i>",
                styles['Normal']
            ))
            
            # Build PDF
            doc.build(elements)
            
            logger.info(f"PDF receipt generated: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            return ""
    
    def _get_verdict_color(self, label: str) -> str:
        """Get color for verdict label"""
        colors_map = {
            "True": "#28a745",
            "False": "#dc3545",
            "Neutral": "#ffc107"
        }
        return colors_map.get(label, "#6c757d")
    
    def _generate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate summary statistics
        
        Args:
            results: List of all results
            
        Returns:
            Summary dictionary
        """
        total = len(results)
        true_count = sum(1 for r in results if r['user_label'] == 'True')
        false_count = sum(1 for r in results if r['user_label'] == 'False')
        neutral_count = sum(1 for r in results if r['user_label'] == 'Neutral')
        
        # Find highest risk
        risk_levels = ['critical', 'high', 'medium', 'low']
        highest_risk = 'low'
        for risk in risk_levels:
            if any(r['combined_risk_level'] == risk for r in results):
                highest_risk = risk
                break
        
        return {
            "total_claims": total,
            "true_count": true_count,
            "false_count": false_count,
            "neutral_count": neutral_count,
            "highest_risk": highest_risk,
            "needs_review_count": sum(1 for r in results if r.get('needs_human_review', False))
        }


if __name__ == "__main__":
    # Test
    agent = SynthesisAgent()
    
    test_input = {
        "primary_language": "en",
        "claims_with_virality": [{
            "claim_id": "clm_001",
            "claim": "5G towers cause COVID-19",
            "original_text": "5G towers spreading virus",
            "language": "en",
            "user_label": "False",
            "confidence": 95,
            "short_explain_en": "This claim has been debunked by health authorities.",
            "needs_human_review": False,
            "evidence": [{
                "url": "https://who.int",
                "title": "WHO debunks 5G myth",
                "source_type": "health_authority",
                "credibility_score": 100
            }],
            "virality_score": 75,
            "combined_risk_level": "high"
        }],
        "visual_forensics": {"suspicion_level": "none"}
    }
    
    result = agent.build_response(test_input)
    
    import json
    print(json.dumps(result, indent=2, default=str))
