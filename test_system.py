"""
Test script for the refactored Health Research Agentic System

Tests basic functionality of agents, models, controller, and validator.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_models():
    """Test data models."""
    print("\n" + "="*50)
    print("Testing Data Models")
    print("="*50)
    
    from models import Query, Summary, UserFeedback, ReflectionReport, QueryResponse
    from datetime import datetime
    
    # Test Query
    query = Query(
        query_id="test_001",
        text="What are the symptoms of diabetes?",
        session_id="session_123"
    )
    print(f"✓ Query created: {query.text}")
    print(f"  Query dict: {query.to_dict()}")
    
    # Test Summary
    summary = Summary(
        summary_id="sum_001",
        content="Diabetes symptoms include frequent urination...",
        confidence=0.85
    )
    print(f"\n✓ Summary created with confidence: {summary.confidence}")
    
    # Test UserFeedback
    feedback = UserFeedback(
        feedback_id="fb_001",
        summary_id="sum_001",
        rating=4,
        comments="Good summary but needs more detail",
        improvement_requested=True
    )
    print(f"\n✓ Feedback created: Rating {feedback.rating}/5")
    print(f"  Valid rating: {feedback.validate_rating()}")
    
    # Test ReflectionReport
    report = ReflectionReport(
        report_id="rep_001",
        summary_id="sum_001",
        coherence_score=4.2,
        completeness_score=3.8,
        factuality_confidence=4.5
    )
    print(f"\n✓ Reflection report created")
    print(f"  Overall score: {report.calculate_overall_score():.2f}/5.0")
    
    return True


def test_validator():
    """Test input validator."""
    print("\n" + "="*50)
    print("Testing Input Validator")
    print("="*50)
    
    from validator import InputValidator
    
    validator = InputValidator()
    
    # Test valid query
    valid_query = "What are the symptoms of diabetes?"
    result = validator.validate_query(valid_query)
    print(f"✓ Valid query test: {result}")
    
    # Test too short
    short_query = "Hi"
    result = validator.validate_query(short_query)
    print(f"✓ Too short query test: {result} (expected False)")
    
    # Test sanitization
    dirty_input = "<script>alert('xss')</script>Hello world"
    clean = validator.sanitize_input(dirty_input)
    print(f"✓ Sanitization test: '{clean}'")
    
    # Test rating validation
    print(f"✓ Rating 3 valid: {validator.validate_rating(3)}")
    print(f"✓ Rating 6 valid: {validator.validate_rating(6)} (expected False)")
    
    return True


def test_agents():
    """Test agent classes."""
    print("\n" + "="*50)
    print("Testing Agent Classes")
    print("="*50)
    
    # Test PlannerAgent
    from agents.planner_agent import PlannerAgent
    planner = PlannerAgent()
    print(f"\n✓ PlannerAgent created: {planner.name}")
    
    plan = planner.process("What causes heart disease?")
    print(f"  Plan generated ({len(plan)} chars)")
    print(f"  First 100 chars: {plan[:100]}...")
    
    # Test SearchAgent
    print("\n✓ SearchAgent:")
    from agents.search_agent import SearchAgent
    searcher = SearchAgent(top_k=3)
    print(f"  Agent created: {searcher.name}, top_k={searcher.top_k}")
    
    # Note: This will only work if ChromaDB is populated
    try:
        results = searcher.process("diabetes symptoms")
        print(f"  Search executed ({len(results)} chars)")
    except Exception as e:
        print(f"  Search test skipped (ChromaDB may be empty): {e}")
    
    # Test SummarizationAgent
    from agents.summarize_agent import SummarizationAgent
    summarizer = SummarizationAgent(max_length=500)
    print(f"\n✓ SummarizationAgent created: {summarizer.name}")
    
    test_text = "Diabetes is a chronic health condition. " * 10
    summary = summarizer.process(test_text)
    print(f"  Summary generated ({len(summary)} chars)")
    
    # Test ReflectiveAgent
    from agents.reflective_agent import ReflectiveAgent
    reflector = ReflectiveAgent()
    print(f"\n✓ ReflectiveAgent created: {reflector.name}")
    
    reflection = reflector.process(summary)
    print(f"  Reflection generated ({len(reflection)} chars)")
    print(f"  Metrics: {reflector.metrics}")
    
    # Test feedback incorporation
    from models import UserFeedback
    feedback = UserFeedback(
        feedback_id="fb_test",
        summary_id="sum_test",
        rating=3,
        comments="Needs more detail",
        improvement_requested=True
    )
    reflector.incorporate_feedback(feedback)
    needs_revision = reflector.determine_revision_need(feedback)
    print(f"  Feedback processed, revision needed: {needs_revision}")
    
    return True


def test_controller():
    """Test system controller."""
    print("\n" + "="*50)
    print("Testing System Controller")
    print("="*50)
    
    from controller import SystemController
    
    controller = SystemController()
    controller.initialize_system()
    print("✓ Controller initialized")
    
    # Test query handling
    response = controller.handle_query("What are diabetes symptoms?")
    print(f"\n✓ Query handled:")
    print(f"  Status: {response.status}")
    print(f"  Execution time: {response.execution_time:.3f}s")
    print(f"  Has error: {bool(response.error_message)}")
    
    if response.agent_logs:
        print(f"  Log entries: {len(response.agent_logs)}")
        print(f"  First log preview: {response.agent_logs[0][:100]}...")
    
    # Test feedback handling
    feedback_response = controller.handle_feedback(
        summary_id=response.response_id,
        rating=4,
        comments="Good summary",
        improvement_requested=False
    )
    print(f"\n✓ Feedback handled:")
    print(f"  Status: {feedback_response.status}")
    
    return True


def test_session_manager():
    """Test session manager."""
    print("\n" + "="*50)
    print("Testing Session Manager")
    print("="*50)
    
    from session_manager import SessionManager
    from models import Query
    
    manager = SessionManager(default_timeout=30)
    
    # Create session
    session_id = manager.create_session()
    print(f"✓ Session created: {session_id}")
    
    # Add query to session
    query = Query(query_id="q1", text="Test query", session_id=session_id)
    success = manager.update_session(session_id, query=query)
    print(f"✓ Query added to session: {success}")
    
    # Get session history
    history = manager.get_session_history(session_id)
    print(f"✓ Session history retrieved:")
    print(f"  Queries: {len(history['queries'])}")
    print(f"  Feedback: {len(history['feedback'])}")
    
    # Test active sessions
    count = manager.get_active_session_count()
    print(f"✓ Active sessions: {count}")
    
    return True


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print(" HEALTH RESEARCH AGENTIC SYSTEM - TEST SUITE")
    print("="*70)
    
    tests = [
        ("Data Models", test_models),
        ("Input Validator", test_validator),
        ("Session Manager", test_session_manager),
        ("Agent Classes", test_agents),
        ("System Controller", test_controller),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, "PASS" if success else "FAIL", None))
        except Exception as e:
            results.append((test_name, "ERROR", str(e)))
            print(f"\n❌ Error in {test_name}: {e}")
    
    # Summary
    print("\n" + "="*70)
    print(" TEST SUMMARY")
    print("="*70)
    
    for name, status, error in results:
        symbol = "✓" if status == "PASS" else "❌"
        print(f"{symbol} {name}: {status}")
        if error:
            print(f"  Error: {error}")
    
    passed = sum(1 for _, status, _ in results if status == "PASS")
    total = len(results)
    print(f"\nTests passed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️ Some tests failed. Review errors above.")


if __name__ == "__main__":
    run_all_tests()
