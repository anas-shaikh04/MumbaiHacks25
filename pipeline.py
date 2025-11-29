"""
Veritas Guardian Pipeline Controller
Orchestrates the 6-agent verification pipeline
"""

from typing import Dict, Any, Optional
from loguru import logger

from agents.agent1_ingestion import IngestionAgent
from agents.agent2_claims import ClaimsAgent
from agents.agent3_evidence import EvidenceAgent
from agents.agent4_verification import VerificationAgent
from agents.agent5_virality import ViralityAgent
from agents.agent6_synthesis import SynthesisAgent


class VeritasGuardianPipeline:
    """
    Main pipeline controller for Veritas Guardian
    Coordinates all 6 agents in sequence
    """
    
    def __init__(self):
        logger.info("Initializing Veritas Guardian Pipeline...")
        
        self.agent1 = IngestionAgent()
        self.agent2 = ClaimsAgent()
        self.agent3 = EvidenceAgent()
        self.agent4 = VerificationAgent()
        self.agent5 = ViralityAgent()
        self.agent6 = SynthesisAgent()
        
        logger.info("All agents initialized successfully")
        
    def process(
        self, 
        user_input: Any, 
        input_type: str = "text",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute full verification pipeline
        
        Args:
            user_input: Content to verify (text string, file path, or URL)
            input_type: One of: "text", "url", "image", "video", "pdf"
            metadata: Optional social metrics (views, likes, shares, comments)
            
        Returns:
            Complete verification results with all agent outputs
        """
        logger.info("=" * 80)
        logger.info("STARTING VERIFICATION PIPELINE")
        logger.info(f"Input type: {input_type}")
        logger.info("=" * 80)
        
        try:
            # AGENT 1: Ingestion & Multimodal Processing
            logger.info("\n[AGENT 1] Starting ingestion...")
            step1 = self.agent1.ingest(user_input, input_type)
            logger.info(f"[AGENT 1] Complete. Media type: {step1['media_type']}")
            
            # AGENT 2: Language Detection & Claim Extraction
            logger.info("\n[AGENT 2] Starting claim extraction...")
            step2 = self.agent2.extract_claims(step1)
            logger.info(f"[AGENT 2] Complete. Extracted {len(step2['claims'])} claims")
            
            # AGENT 3: Evidence Retrieval
            logger.info("\n[AGENT 3] Starting evidence retrieval...")
            step3 = self.agent3.get_evidence(step2)
            logger.info(f"[AGENT 3] Complete. Retrieved evidence for {len(step3['claims_with_evidence'])} claims")
            
            # AGENT 4: Verification & Labeling
            logger.info("\n[AGENT 4] Starting verification...")
            step4 = self.agent4.verify(step3)
            logger.info(f"[AGENT 4] Complete. Verified {len(step4['verified_claims'])} claims")
            
            # AGENT 5: Virality & Risk Analysis
            logger.info("\n[AGENT 5] Starting virality analysis...")
            step5 = self.agent5.compute_virality(step4, metadata)
            logger.info(f"[AGENT 5] Complete. Computed virality for {len(step5['claims_with_virality'])} claims")
            
            # AGENT 6: Response Synthesis & PDF Generation
            logger.info("\n[AGENT 6] Starting response synthesis...")
            step6 = self.agent6.build_response(step5)
            logger.info(f"[AGENT 6] Complete. Generated {len(step6['results'])} results")
            
            logger.info("\n" + "=" * 80)
            logger.info("PIPELINE COMPLETE")
            logger.info("=" * 80)
            
            return step6
            
        except Exception as e:
            logger.error(f"Pipeline error: {e}")
            raise
    
    def get_agent_workflow(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate agent workflow summary for transparency
        
        Args:
            results: Final pipeline results
            
        Returns:
            Workflow summary with agent actions
        """
        return {
            "workflow": [
                {
                    "agent": "Agent 1 - Ingestion",
                    "action": "Extracted text and performed visual forensics",
                    "status": "complete"
                },
                {
                    "agent": "Agent 2 - Claims",
                    "action": f"Detected language and extracted {results['summary']['total_claims']} claims",
                    "status": "complete"
                },
                {
                    "agent": "Agent 3 - Evidence",
                    "action": "Retrieved evidence from web sources",
                    "status": "complete"
                },
                {
                    "agent": "Agent 4 - Verification",
                    "action": "Verified claims using LLM reasoning",
                    "status": "complete"
                },
                {
                    "agent": "Agent 5 - Virality",
                    "action": "Computed virality scores and risk levels",
                    "status": "complete"
                },
                {
                    "agent": "Agent 6 - Synthesis",
                    "action": "Generated multilingual explanations and PDF receipts",
                    "status": "complete"
                }
            ],
            "timestamp": results['results'][0]['timestamp'] if results['results'] else None
        }


if __name__ == "__main__":
    # Test the pipeline
    pipeline = VeritasGuardianPipeline()
    
    # Test with simple text
    test_input = "5G towers are spreading coronavirus and causing health issues."
    
    result = pipeline.process(test_input, "text")
    
    import json
    print("\n" + "=" * 80)
    print("PIPELINE TEST RESULTS")
    print("=" * 80)
    print(json.dumps(result, indent=2, default=str))
    
    # Get workflow
    workflow = pipeline.get_agent_workflow(result)
    print("\n" + "=" * 80)
    print("AGENT WORKFLOW")
    print("=" * 80)
    print(json.dumps(workflow, indent=2))
