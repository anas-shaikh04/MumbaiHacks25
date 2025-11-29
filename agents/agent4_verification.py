"""
Agent 4: Verification & Label Mapping
Uses LLM reasoning with evidence to verify claims
Maps internal labels to user-friendly verdicts
"""

import json
from typing import Dict, Any, List
from loguru import logger

from utils.llm_provider import get_llm_json, get_llm_response


class VerificationAgent:
    """
    Agent 4: Verifies claims using LLM reasoning
    Maps to user-friendly labels with confidence scores
    """
    
    def __init__(self, confidence_threshold: int = 80):
        self.confidence_threshold = confidence_threshold
        self.sensitive_keywords = [
            "covid", "vaccine", "vaccination", "corona",
            "election", "voting", "ballot", "vote",
            "riot", "violence", "attack", "terror",
            "disaster", "earthquake", "flood", "cyclone",
            "medicine", "drug", "treatment", "cure"
        ]
        
    def verify(self, evidence_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verify claims using evidence and LLM reasoning
        
        Args:
            evidence_output: Output from Agent 3
            
        Returns:
            {
                "primary_language": str,
                "verified_claims": [
                    {
                        "claim_id": str,
                        "claim": str,
                        "original_text": str,
                        "user_label": "True" | "False" | "Neutral",
                        "confidence": int (0-100),
                        "short_explain_en": str,
                        "needs_human_review": bool,
                        "evidence": list,
                        "internal_label": str
                    }
                ]
            }
        """
        logger.info("Starting claim verification")
        
        claims_with_evidence = evidence_output["claims_with_evidence"]
        verified_claims = []
        
        for item in claims_with_evidence:
            logger.info(f"Verifying claim: {item['claim'][:50]}...")
            
            verification_result = self._verify_single_claim(
                item["claim"],
                item["evidence"]
            )
            
            # Apply safety rules
            needs_review = self._check_needs_review(
                item["claim"],
                verification_result["confidence"],
                verification_result["internal_label"]
            )
            
            verified_claims.append({
                "claim_id": item["claim_id"],
                "claim": item["claim"],
                "original_text": item["original_text"],
                "language": item["language"],
                "user_label": verification_result["user_label"],
                "confidence": verification_result["confidence"],
                "short_explain_en": verification_result["explanation"],
                "needs_human_review": needs_review,
                "evidence": item["evidence"],
                "internal_label": verification_result["internal_label"]
            })
        
        logger.info(f"Verification complete for {len(verified_claims)} claims")
        
        return {
            "primary_language": evidence_output["primary_language"],
            "verified_claims": verified_claims,
            "visual_forensics": evidence_output.get("visual_forensics", {})
        }
    
    def _verify_single_claim(
        self, 
        claim: str, 
        evidence: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Verify a single claim using LLM
        
        Args:
            claim: Claim text
            evidence: List of evidence items
            
        Returns:
            {
                "internal_label": str,
                "user_label": str,
                "confidence": int,
                "explanation": str
            }
        """
        # Build evidence context
        evidence_text = self._format_evidence(evidence[:5])  # Top 5
        
        # Compute evidence scores
        support_score = self._compute_support_score(evidence)
        refute_score = self._compute_refute_score(evidence)
        
        prompt = f"""You are a fact-checking expert. Analyze the claim and evidence, then provide a clear verdict in simple language.

CLAIM: {claim}

EVIDENCE FROM CREDIBLE SOURCES:
{evidence_text}

CREDIBILITY METRICS:
- Support score: {support_score}/100 (based on authoritative sources)
- Refutation score: {refute_score}/100

INSTRUCTIONS:
1. If evidence clearly supports the claim with high credibility sources → "Supported" with 70-95 confidence
2. If evidence clearly contradicts or debunks the claim → "Refuted" with 70-95 confidence
3. If claim is partially true, exaggerated, or lacks context → "Misleading" with 60-85 confidence
4. Only use "Insufficient" if there's truly no relevant evidence found

Be decisive - avoid "Insufficient" unless absolutely necessary. Most claims can be evaluated.

For the explanation:
- Use simple, easy-to-understand language (avoid technical jargon)
- Keep it concise (2-3 sentences maximum)
- If the claim is FALSE or MISLEADING, include what the TRUE facts are
- Explain WHY the claim is true/false/misleading based on evidence

Return ONLY this JSON (no markdown, no explanation):
{{
    "internal_label": "Supported" or "Refuted" or "Misleading" or "Insufficient",
    "confidence": <number 50-95>,
    "explanation": "<simple 2-3 sentence explanation. If false/misleading, include the true facts>"
}}"""

        try:
            response = get_llm_json(prompt, temperature=0.3)
            
            internal_label = response.get("internal_label", "Insufficient")
            confidence = int(response.get("confidence", 50))
            rationale = response.get("explanation", response.get("rationale", "Unable to verify"))
            
            # Log the raw response for debugging
            logger.debug(f"LLM Response - Label: {internal_label}, Confidence: {confidence}")
            
            # Map to user label
            user_label = self._map_label(internal_label, confidence)
            
            logger.info(f"Verification result: {internal_label} ({confidence}%) → {user_label}")
            
            return {
                "internal_label": internal_label,
                "user_label": user_label,
                "confidence": confidence,
                "explanation": rationale
            }
            
        except Exception as e:
            logger.error(f"Verification failed: {e}")
            return {
                "internal_label": "Insufficient",
                "user_label": "Neutral",
                "confidence": 0,
                "explanation": "Verification system error"
            }
    
    def _format_evidence(self, evidence: List[Dict[str, Any]]) -> str:
        """Format evidence for LLM prompt"""
        if not evidence:
            return "No evidence found."
        
        formatted = []
        for idx, ev in enumerate(evidence, 1):
            source_name = ev.get('source_name', ev.get('domain', 'Unknown'))
            formatted.append(
                f"{idx}. [{ev['source_type'].upper()}] {source_name}\n"
                f"   {ev['title']}\n"
                f"   Credibility: {ev['credibility_score']}/100\n"
                f"   Content: {ev['snippet'][:200]}..."
            )
        
        return "\n\n".join(formatted)
    
    def _compute_support_score(self, evidence: List[Dict[str, Any]]) -> int:
        """Compute support score from evidence credibility"""
        if not evidence:
            return 0
        
        # Weight by credibility
        total = sum(ev["credibility_score"] for ev in evidence[:3])
        return min(100, total // 3)
    
    def _compute_refute_score(self, evidence: List[Dict[str, Any]]) -> int:
        """Compute refutation score from fact-check sources"""
        factcheck_count = sum(
            1 for ev in evidence[:5] 
            if ev["source_type"] == "factcheck"
        )
        return min(100, factcheck_count * 30)
    
    def _map_label(self, internal_label: str, confidence: int) -> str:
        """
        Map internal label to user-friendly label
        
        Internal -> User mapping:
        - Supported + conf >= 60 -> True
        - Refuted + conf >= 60 -> False  
        - Misleading + conf >= 50 -> Neutral (but lean towards False if high conf)
        - Insufficient -> Neutral
        """
        if internal_label == "Supported":
            return "True" if confidence >= 60 else "Neutral"
        elif internal_label == "Refuted":
            return "False" if confidence >= 60 else "Neutral"
        elif internal_label == "Misleading":
            # Misleading with high confidence leans False
            if confidence >= 75:
                return "False"
            else:
                return "Neutral"
        else:  # Insufficient
            return "Neutral"
    
    def _check_needs_review(
        self, 
        claim: str, 
        confidence: int, 
        internal_label: str
    ) -> bool:
        """
        Determine if claim needs human review
        
        Rules:
        - Sensitive topics + low confidence -> review
        - High-impact false claims + medium confidence -> review
        """
        is_sensitive = any(
            keyword in claim.lower() 
            for keyword in self.sensitive_keywords
        )
        
        if is_sensitive and confidence < self.confidence_threshold:
            return True
        
        if internal_label == "Refuted" and confidence < 90:
            return True
        
        return False


if __name__ == "__main__":
    # Test
    agent = VerificationAgent()
    
    test_input = {
        "primary_language": "en",
        "claims_with_evidence": [{
            "claim_id": "clm_001",
            "claim": "5G towers cause COVID-19",
            "original_text": "5G towers spreading virus",
            "language": "en",
            "evidence": [
                {
                    "url": "https://www.who.int/fact-check",
                    "title": "WHO: No link between 5G and COVID-19",
                    "snippet": "There is no evidence linking 5G to coronavirus",
                    "source_type": "health_authority",
                    "credibility_score": 100
                }
            ]
        }],
        "visual_forensics": {"suspicion_level": "none"}
    }
    
    result = agent.verify(test_input)
    print(json.dumps(result, indent=2))
