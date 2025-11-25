"""LLM Configuration for Multi-Provider Support (Mistral AI or OpenAI)"""
import os
from dotenv import load_dotenv

# Force reload environment variables
load_dotenv(override=True)

def get_llm_config():
    """
    Get LLM configuration based on available API keys.
    Supports both Mistral AI and OpenAI.
    
    Returns:
        CrewAI LLM object or default model string
    """
    try:
        from crewai import LLM
    except ImportError:
        return "gpt-4o-mini"
    
    # Check for Mistral API key first
    mistral_key = os.getenv('MISTRAL_API_KEY', '').strip()
    print(f"Debug: Mistral key starts with: {mistral_key[:10]}..." if mistral_key else "Debug: No Mistral key")
    
    if mistral_key and len(mistral_key) > 20 and mistral_key not in ['your-mistral-api-key-here']:
        model = os.getenv('MISTRAL_MODEL', 'mistral-small-latest')
        print(f"✓ Using Mistral AI: {model}")
        try:
            return LLM(
                model=f"mistral/{model}",
                api_key=mistral_key
            )
        except Exception as e:
            print(f"⚠️  Mistral LLM initialization failed: {e}")
            print(f"   Falling back to pure Python mode")
            return None
    
    # Fallback to OpenAI
    openai_key = os.getenv('OPENAI_API_KEY', '').strip()
    if openai_key and len(openai_key) > 20 and not openai_key.startswith('YOUR'):
        model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        print(f"✓ Using OpenAI: {model}")
        try:
            return LLM(
                model=f"openai/{model}",
                api_key=openai_key
            )
        except Exception as e:
            print(f"⚠️  OpenAI LLM initialization failed: {e}")
            return None
    
    # No valid API key found - return None to skip CrewAI agents
    print("⚠️  No valid API key found. Using pure Python fallback mode (no LLM).")
    print("   Get Mistral key (recommended): https://console.mistral.ai/api-keys/")
    print("   Get OpenAI key: https://platform.openai.com/account/api-keys")
    return None
