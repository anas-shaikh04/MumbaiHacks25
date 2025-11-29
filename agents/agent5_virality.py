"""
Agent 5: Virality & Risk Analysis
Computes virality score and risk level based on social metrics and content
"""

import math
from typing import Dict, Any, Optional
from loguru import logger


class ViralityAgent:
    """
    Agent 5: Analyzes virality potential and risk level
    Combines social metrics with content analysis
    """
    
    def __init__(self):
        self.viral_keywords = [
            "breaking", "urgent", "alert", "warning", "shocking",
            "exposed", "revealed", "truth", "scandal", "secret",
            "share", "forward", "spread", "viral", "must watch"
        ]
        
    def compute_virality(
        self, 
        verification_output: Dict[str, Any], 
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Compute virality and risk for each claim
        
        Args:
            verification_output: Output from Agent 4
            metadata: Optional social metrics (views, likes, shares, comments)
            
        Returns:
            {
                "primary_language": str,
                "claims_with_virality": [
                    {
                        ...all previous fields...,
                        "virality_score": int (0-100),
                        "reach_score": int,
                        "engagement_score": int,
                        "content_boost_score": float,
                        "combined_risk_level": "low" | "medium" | "high" | "critical"
                    }
                ]
            }
        """
        logger.info("Computing virality and risk scores")
        
        if metadata is None:
            metadata = {}
        
        verified_claims = verification_output["verified_claims"]
        claims_with_virality = []
        
        for claim in verified_claims:
            virality_data = self._compute_claim_virality(
                claim,
                metadata
            )
            
            # Merge with existing claim data
            claim_with_virality = {**claim, **virality_data}
            claims_with_virality.append(claim_with_virality)
        
        logger.info(f"Virality analysis complete for {len(claims_with_virality)} claims")
        
        return {
            "primary_language": verification_output["primary_language"],
            "claims_with_virality": claims_with_virality,
            "visual_forensics": verification_output.get("visual_forensics", {})
        }
    
    def _compute_claim_virality(
        self, 
        claim: Dict[str, Any], 
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Compute virality metrics for a single claim
        
        Returns:
            {
                "virality_score": int,
                "reach_score": int,
                "engagement_score": int,
                "content_boost_score": float,
                "combined_risk_level": str
            }
        """
        # 1. Reach Score (based on views)
        views = metadata.get("views", 1000)
        reach_score = self._compute_reach_score(views)
        
        # 2. Engagement Score (based on likes, shares, comments)
        likes = metadata.get("likes", 50)
        shares = metadata.get("shares", 10)
        comments = metadata.get("comments", 20)
        engagement_score = self._compute_engagement_score(
            views, likes, shares, comments
        )
        
        # 3. Content Boost Score (based on keywords and media type)
        content_boost = self._compute_content_boost(
            claim["claim"],
            claim["original_text"]
        )
        
        # 4. Combined Virality Score
        virality_score = self._compute_virality_score(
            reach_score,
            engagement_score,
            content_boost
        )
        
        # 5. Risk Level
        risk_level = self._determine_risk_level(
            virality_score,
            claim["user_label"],
            claim["confidence"],
            claim["needs_human_review"]
        )
        
        return {
            "virality_score": virality_score,
            "reach_score": reach_score,
            "engagement_score": engagement_score,
            "content_boost_score": round(content_boost, 2),
            "combined_risk_level": risk_level
        }
    
    def _compute_reach_score(self, views: int) -> int:
        """
        Compute reach score from view count
        
        Logarithmic scale:
        - 1K views -> 20
        - 10K views -> 40
        - 100K views -> 60
        - 1M views -> 80
        - 10M+ views -> 100
        """
        if views < 100:
            return 10
        
        score = 20 + (math.log10(views) - 2) * 20
        return min(100, max(0, int(score)))
    
    def _compute_engagement_score(
        self, 
        views: int, 
        likes: int, 
        shares: int, 
        comments: int
    ) -> int:
        """
        Compute engagement score from interaction metrics
        
        Engagement rate = (likes + shares*2 + comments) / views * 100
        """
        if views == 0:
            return 0
        
        total_engagement = likes + (shares * 2) + comments
        engagement_rate = (total_engagement / views) * 100
        
        # Scale to 0-100
        score = min(100, int(engagement_rate * 10))
        return score
    
    def _compute_content_boost(
        self, 
        claim: str, 
        original_text: str
    ) -> float:
        """
        Compute content boost score from text analysis
        
        Factors:
        - Viral keywords (BREAKING, URGENT, etc.)
        - ALL CAPS usage
        - Exclamation marks
        - Sensational language
        """
        combined_text = (claim + " " + original_text).lower()
        boost = 1.0
        
        # Check for viral keywords
        keyword_count = sum(
            1 for keyword in self.viral_keywords 
            if keyword in combined_text
        )
        boost += keyword_count * 0.2
        
        # Check for ALL CAPS
        if any(word.isupper() and len(word) > 3 for word in original_text.split()):
            boost += 0.3
        
        # Check for excessive exclamation marks
        exclamation_count = original_text.count("!")
        if exclamation_count > 2:
            boost += 0.2
        
        return min(2.5, boost)
    
    def _compute_virality_score(
        self, 
        reach: int, 
        engagement: int, 
        boost: float
    ) -> int:
        """
        Compute final virality score
        
        Formula: (0.4 * reach + 0.3 * engagement + 0.3 * boost_normalized) * boost
        """
        boost_normalized = (boost - 1.0) * 100  # Convert to 0-150 scale
        
        base_score = (0.4 * reach) + (0.3 * engagement) + (0.3 * boost_normalized)
        final_score = base_score * (boost / 1.5)  # Apply boost multiplier
        
        return min(100, max(0, int(final_score)))
    
    def _determine_risk_level(
        self, 
        virality: int, 
        user_label: str, 
        confidence: int,
        needs_review: bool
    ) -> str:
        """
        Determine combined risk level
        
        Risk matrix:
        - Critical: False claim + high virality (>70)
        - High: False claim OR (Neutral + needs review + high virality)
        - Medium: Neutral + medium virality OR False + low virality
        - Low: True claim OR low virality
        """
        if user_label == "False":
            if virality > 70:
                return "critical"
            elif virality > 40:
                return "high"
            else:
                return "medium"
        
        elif user_label == "Neutral":
            if needs_review and virality > 60:
                return "high"
            elif virality > 50:
                return "medium"
            else:
                return "low"
        
        else:  # True
            if virality > 80:
                return "medium"  # High virality even for true claims
            else:
                return "low"


if __name__ == "__main__":
    # Test
    agent = ViralityAgent()
    
    test_input = {
        "primary_language": "en",
        "verified_claims": [{
            "claim_id": "clm_001",
            "claim": "BREAKING: 5G towers cause COVID-19!!!",
            "original_text": "URGENT: Share this TRUTH",
            "user_label": "False",
            "confidence": 95,
            "short_explain_en": "This is false",
            "needs_human_review": False,
            "evidence": []
        }],
        "visual_forensics": {"suspicion_level": "none"}
    }
    
    result = agent.compute_virality(
        test_input,
        metadata={"views": 50000, "likes": 2000, "shares": 500, "comments": 300}
    )
    
    import json
    print(json.dumps(result, indent=2))
