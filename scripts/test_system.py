"""
Test script for Veritas Guardian
Quick tests for all components
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_imports():
    """Test all imports work"""
    print("🧪 Testing imports...")
    try:
        from agents.agent1_ingestion import IngestionAgent
        from agents.agent2_claims import ClaimsAgent
        from agents.agent3_evidence import EvidenceAgent
        from agents.agent4_verification import VerificationAgent
        from agents.agent5_virality import ViralityAgent
        from agents.agent6_synthesis import SynthesisAgent
        from utils.llm_provider import get_llm_response
        from utils.translator import translate_to_english
        from utils.visual_forensics import perform_ela
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_pipeline():
    """Test basic pipeline"""
    print("\n🧪 Testing pipeline...")
    try:
        from pipeline import VeritasGuardianPipeline
        
        pipeline = VeritasGuardianPipeline()
        print("✅ Pipeline initialized")
        
        # Test with simple text
        test_text = "The Earth is round."
        print(f"   Testing with: '{test_text}'")
        
        result = pipeline.process(test_text, "text")
        
        if result and 'results' in result:
            print(f"✅ Pipeline executed successfully")
            print(f"   Found {len(result['results'])} claims")
            return True
        else:
            print("❌ Pipeline returned invalid result")
            return False
            
    except Exception as e:
        print(f"❌ Pipeline test failed: {e}")
        return False

def test_agents():
    """Test individual agents"""
    print("\n🧪 Testing individual agents...")
    
    try:
        # Agent 1
        from agents.agent1_ingestion import IngestionAgent
        agent1 = IngestionAgent()
        result1 = agent1.ingest("Test text", "text")
        assert result1['media_type'] == 'text'
        print("✅ Agent 1 (Ingestion) working")
        
        # Agent 2
        from agents.agent2_claims import ClaimsAgent
        agent2 = ClaimsAgent()
        result2 = agent2.extract_claims(result1)
        assert 'claims' in result2
        print("✅ Agent 2 (Claims) working")
        
        # Agent 3
        from agents.agent3_evidence import EvidenceAgent
        agent3 = EvidenceAgent()
        result3 = agent3.get_evidence(result2)
        assert 'claims_with_evidence' in result3
        print("✅ Agent 3 (Evidence) working")
        
        # Agent 4
        from agents.agent4_verification import VerificationAgent
        agent4 = VerificationAgent()
        result4 = agent4.verify(result3)
        assert 'verified_claims' in result4
        print("✅ Agent 4 (Verification) working")
        
        # Agent 5
        from agents.agent5_virality import ViralityAgent
        agent5 = ViralityAgent()
        result5 = agent5.compute_virality(result4)
        assert 'claims_with_virality' in result5
        print("✅ Agent 5 (Virality) working")
        
        # Agent 6
        from agents.agent6_synthesis import SynthesisAgent
        agent6 = SynthesisAgent()
        result6 = agent6.build_response(result5)
        assert 'results' in result6
        print("✅ Agent 6 (Synthesis) working")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False

def test_utilities():
    """Test utility functions"""
    print("\n🧪 Testing utilities...")
    
    try:
        # Translation
        from utils.translator import get_language_name, is_fully_supported
        assert get_language_name("en") == "English"
        assert is_fully_supported("hi") == True
        print("✅ Translator utilities working")
        
        # Credibility DB
        from agents.agent3_evidence import EvidenceAgent
        agent = EvidenceAgent()
        cred = agent._get_credibility("pib.gov.in")
        assert cred['score'] == 100
        print("✅ Credibility database working")
        
        return True
        
    except Exception as e:
        print(f"❌ Utility test failed: {e}")
        return False

def test_api_key():
    """Test if API key is configured"""
    print("\n🧪 Testing API configuration...")
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "your_gemini_api_key_here":
            print("⚠️  GEMINI_API_KEY not configured in .env")
            return False
        
        print("✅ API key configured")
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 80)
    print("🛡️  VERITAS GUARDIAN - Component Tests")
    print("=" * 80)
    
    results = {
        "Imports": test_imports(),
        "API Key": test_api_key(),
        "Utilities": test_utilities(),
        "Agents": test_agents(),
        "Pipeline": test_pipeline()
    }
    
    print("\n" + "=" * 80)
    print("📊 Test Results Summary")
    print("=" * 80)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20s} {status}")
    
    total = len(results)
    passed = sum(results.values())
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! System is ready.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please check configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
