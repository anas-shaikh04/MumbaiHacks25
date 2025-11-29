"""
Agent 3: Evidence Retrieval
Searches web for reliable evidence and tags source credibility
Integrates Google Fact Check Tools API for verified fact-checks
"""

import os
import csv
import requests
from typing import Dict, Any, List
from urllib.parse import urlparse
from loguru import logger
from dotenv import load_dotenv
import pandas as pd

# Search
from duckduckgo_search import DDGS

load_dotenv()


class EvidenceAgent:
    """
    Agent 3: Retrieves evidence from the web
    Filters and scores sources by credibility
    """
    
    def __init__(self, credibility_csv_path: str = "./data/credibility.csv"):
        self.credibility_csv_path = credibility_csv_path
        self.credibility_db = self._load_credibility_db()
        self.factcheck_api_key = os.getenv("FACTCHECK_API_KEY")
        
        if self.factcheck_api_key and self.factcheck_api_key != "optional_factcheck_api_key":
            logger.info("Google Fact Check Tools API enabled")
        else:
            logger.info("Google Fact Check Tools API not configured")
        
    def _load_credibility_db(self) -> pd.DataFrame:
        """Load credibility database from CSV"""
        try:
            if os.path.exists(self.credibility_csv_path):
                df = pd.read_csv(self.credibility_csv_path)
                logger.info(f"Loaded credibility database with {len(df)} entries")
                return df
            else:
                logger.warning(f"Credibility database not found at {self.credibility_csv_path}")
                return pd.DataFrame(columns=["domain", "type", "score"])
        except Exception as e:
            logger.error(f"Failed to load credibility database: {e}")
            return pd.DataFrame(columns=["domain", "type", "score"])
    
    def get_evidence(self, claims_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Search for evidence for each claim
        
        Args:
            claims_output: Output from Agent 2
            
        Returns:
            {
                "primary_language": str,
                "claims_with_evidence": [
                    {
                        "claim_id": str,
                        "claim": str,
                        "original_text": str,
                        "language": str,
                        "evidence": [
                            {
                                "url": str,
                                "title": str,
                                "snippet": str,
                                "source_type": str,
                                "credibility_score": int
                            }
                        ]
                    }
                ]
            }
        """
        logger.info("Starting evidence retrieval")
        
        claims = claims_output["claims"]
        claims_with_evidence = []
        
        for claim in claims:
            logger.info(f"Searching evidence for: {claim['canonical_claim'][:50]}...")
            
            evidence_list = self._search_and_filter(claim["canonical_claim"])
            
            claims_with_evidence.append({
                "claim_id": claim["claim_id"],
                "claim": claim["canonical_claim"],
                "original_text": claim["original_text"],
                "language": claim["language"],
                "timestamp": claim.get("timestamp"),
                "evidence": evidence_list
            })
        
        logger.info(f"Evidence retrieval complete for {len(claims_with_evidence)} claims")
        
        return {
            "primary_language": claims_output["primary_language"],
            "claims_with_evidence": claims_with_evidence,
            "visual_forensics": claims_output.get("visual_forensics", {})
        }
    
    def _search_and_filter(
        self, 
        query: str, 
        max_results: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search multiple sources and filter by credibility:
        1. Google Fact Check Tools API (if available)
        2. DuckDuckGo web search
        
        Args:
            query: Search query (claim text)
            max_results: Maximum results to fetch
            
        Returns:
            List of evidence items with credibility scores
        """
        evidence = []
        
        # 1. Try Google Fact Check Tools API first
        if self.factcheck_api_key and self.factcheck_api_key != "optional_factcheck_api_key":
            factcheck_results = self._search_factcheck_api(query)
            evidence.extend(factcheck_results)
            logger.info(f"Found {len(factcheck_results)} fact-check results")
        
        # 2. Search using DuckDuckGo
        try:
            results = DDGS().text(query, max_results=max_results)
            
            for result in results:
                url = result.get("href", "")
                title = result.get("title", "")
                snippet = result.get("body", "")
                
                # Extract domain
                domain = self._extract_domain(url)
                
                # Get credibility info
                cred_info = self._get_credibility(domain)
                
                evidence.append({
                    "url": url,
                    "title": title,
                    "snippet": snippet,
                    "source_type": cred_info["type"],
                    "credibility_score": cred_info["score"],
                    "domain": domain,
                    "source_name": self._get_source_name(domain)
                })
            
            # Sort by credibility score (highest first)
            evidence.sort(key=lambda x: x["credibility_score"], reverse=True)
            
            # Return top 5 most credible sources
            return evidence[:5]
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []
    
    def _search_factcheck_api(self, query: str) -> List[Dict[str, Any]]:
        """
        Search Google Fact Check Tools API
        
        Args:
            query: Claim text to search
            
        Returns:
            List of fact-check evidence items
        """
        try:
            url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
            params = {
                "key": self.factcheck_api_key,
                "query": query,
                "languageCode": "en",
                "pageSize": 5
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            evidence = []
            claims = data.get("claims", [])
            
            for claim_data in claims:
                # Get the claim review (fact-check)
                claim_reviews = claim_data.get("claimReview", [])
                if not claim_reviews:
                    continue
                
                # Use the first review
                review = claim_reviews[0]
                
                # Extract rating
                rating = review.get("textualRating", "Unknown")
                title = review.get("title", claim_data.get("text", "Fact Check"))
                url_link = review.get("url", "")
                publisher = review.get("publisher", {}).get("name", "Fact Checker")
                
                # Create snippet with rating
                snippet = f"Fact Check Rating: {rating}. {title}"
                
                evidence.append({
                    "url": url_link,
                    "title": f"[FACT CHECK] {title}",
                    "snippet": snippet,
                    "source_type": "factcheck",
                    "credibility_score": 100,  # Highest priority
                    "rating": rating,
                    "publisher": publisher,
                    "domain": self._extract_domain(url_link),
                    "source_name": publisher
                })
            
            return evidence
            
        except requests.Timeout:
            logger.warning("Fact Check API request timed out")
            return []
        except requests.RequestException as e:
            logger.warning(f"Fact Check API request failed: {e}")
            return []
        except Exception as e:
            logger.error(f"Fact Check API error: {e}")
            return []
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc
            # Remove www. prefix
            if domain.startswith("www."):
                domain = domain[4:]
            return domain
        except:
            return ""
    
    def _get_credibility(self, domain: str) -> Dict[str, Any]:
        """
        Get credibility information for a domain
        
        Args:
            domain: Domain name
            
        Returns:
            {"type": str, "score": int}
        """
        # Check database
        if not self.credibility_db.empty:
            match = self.credibility_db[self.credibility_db["domain"] == domain]
            if not match.empty:
                return {
                    "type": match.iloc[0]["type"],
                    "score": int(match.iloc[0]["score"])
                }
        
        # Default heuristic scoring
        domain_lower = domain.lower()
        
        # Government sources
        if any(x in domain_lower for x in [
            "gov.in", "gov.", "who.int", "cdc.gov", 
            "eci.gov", "pib.gov", "mygov"
        ]):
            return {"type": "govt", "score": 100}
        
        # Fact-checking sites
        if any(x in domain_lower for x in [
            "factcheck", "snopes", "afp.com", "altnews", 
            "boomlive", "thequint", "vishvasnews"
        ]):
            return {"type": "factcheck", "score": 95}
        
        # Health authorities
        if any(x in domain_lower for x in [
            "who.int", "cdc", "mohfw", "nih.gov"
        ]):
            return {"type": "health_authority", "score": 100}
        
        # Reputable news
        if any(x in domain_lower for x in [
            "bbc", "reuters", "thehindu", "indianexpress",
            "apnews", "npr", "theguardian"
        ]):
            return {"type": "news", "score": 85}
        
        # Other news
        if any(x in domain_lower for x in [
            "news", "times", "tribune", "ndtv", "livemint"
        ]):
            return {"type": "news", "score": 70}
        
        # Default
        return {"type": "other", "score": 50}
    
    def _get_source_name(self, domain: str) -> str:
        """Get friendly source name from domain"""
        domain_lower = domain.lower()
        
        # Map common domains to friendly names
        source_map = {
            "bbc.com": "BBC News",
            "bbc.co.uk": "BBC News",
            "reuters.com": "Reuters",
            "thehindu.com": "The Hindu",
            "indianexpress.com": "Indian Express",
            "apnews.com": "Associated Press",
            "npr.org": "NPR",
            "theguardian.com": "The Guardian",
            "nytimes.com": "New York Times",
            "washingtonpost.com": "Washington Post",
            "cnn.com": "CNN",
            "ndtv.com": "NDTV",
            "livemint.com": "Livemint",
            "thequint.com": "The Quint",
            "altnews.in": "Alt News",
            "boomlive.in": "BOOM Live",
            "factcheck.org": "FactCheck.org",
            "snopes.com": "Snopes",
            "afp.com": "AFP Fact Check",
            "vishvasnews.com": "Vishvas News",
            "who.int": "World Health Organization",
            "cdc.gov": "CDC",
            "mohfw.gov.in": "Ministry of Health & Family Welfare",
            "pib.gov.in": "Press Information Bureau",
            "eci.gov.in": "Election Commission of India",
        }
        
        # Check exact match
        for key, name in source_map.items():
            if key in domain_lower:
                return name
        
        # Format domain as title case fallback
        if domain:
            # Remove common TLDs and format
            name = domain.replace('.com', '').replace('.org', '').replace('.in', '')
            name = name.replace('.co.uk', '').replace('.gov', '').replace('.net', '')
            return name.replace('.', ' ').title()
        
        return domain


if __name__ == "__main__":
    # Test
    agent = EvidenceAgent()
    
    test_input = {
        "primary_language": "en",
        "claims": [{
            "claim_id": "clm_001",
            "canonical_claim": "5G towers cause COVID-19",
            "original_text": "5G towers are spreading coronavirus",
            "language": "en",
            "timestamp": None
        }],
        "visual_forensics": {"suspicion_level": "none"}
    }
    
    result = agent.get_evidence(test_input)
    print(f"Evidence result: {result}")
